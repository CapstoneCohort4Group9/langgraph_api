import re
from src.state.state import State
from src.utils.tool_register import get_tool_prompt_for_intent
from src import logger
import json
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from src.config.settings import load_config
from jinja2 import Template

settings = load_config()


class CallingBedrockModelToolNode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        pass

    def get_bedrock_client_with_sts(self):
        try:
            # Priority: Use AWS_PROFILE if defined, otherwise default profile or env
            profile_name = (
                settings.AWS_PROFILE
                if hasattr(settings, "AWS_PROFILE") and settings.AWS_PROFILE
                else None
            )

            session = boto3.Session(profile_name=profile_name)

            # Optional: validate session identity
            caller = session.client("sts").get_caller_identity()
            print(f"Using credentials for: {caller['Arn']}")

            # Step 1: STS AssumeRole using the session
            sts = session.client("sts")

            response = sts.assume_role(
                RoleArn=settings.ASSUME_ROLE_ARN,
                RoleSessionName="LangGraphBedrockSession",
            )

            credentials = response["Credentials"]

            # Step 2: Create a Bedrock Runtime client with temporary session credentials
            bedrock = boto3.client(
                "bedrock-runtime",
                region_name=settings.BEDROCK_REGION,
                aws_access_key_id=credentials["AccessKeyId"],
                aws_secret_access_key=credentials["SecretAccessKey"],
                aws_session_token=credentials["SessionToken"],
            )

            return bedrock

        except ClientError as e:
            raise RuntimeError(f"AWS ClientError: {e}")
        except BotoCoreError as e:
            raise RuntimeError(f"STS AssumeRole failed: {e}")

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        client = self.get_bedrock_client_with_sts()
        logger.info(f"Running Bedrock model with state: {state}")
        # Compose user input with intent/sentiment prefix
        prefixed_input = f"[intent={state['intent']}][sentiment={state['sentiment']}] {state['input']}"
        state["messages"] = state.get("messages", [])

        # Retrieve the system prompt for the intent
        # system_tool_prompt = get_tool_prompt_for_intent(state["intent"])
        # context = state.get("tool_output")

        # system_prompt = {
        #     "role": "system",
        #     "content": (system_tool_prompt or "") + "\n\nContext: " + (context or ""),
        # }
        notAdded = True
        if not isinstance(state["messages"], list) or len(state["messages"]) == 0:
            # Add user input as the first message
            notAdded = False
            state["messages"].append({"role": "user", "content": prefixed_input})
        last_msg = state["messages"][-1]

        # ✅ Check if last message is from the tool and has valid <tool_response> content
        if (
            last_msg.get("role") == "tool"
            and isinstance(last_msg.get("content"), str)
            and re.search(
                r"<tool_response>.*?</tool_response>", last_msg["content"], re.DOTALL
            )
        ):
            # 🧠 Add a system prompt to help the model explain the tool's result naturally
            # system_prompt = {
            #     "role": "system",
            #     "content": "Tool response has been received. Now summarize it clearly and help the user decide.",
            # }
            # last = state["messages"].pop()

            # state["messages"].append(system_prompt)
            # state["messages"].append(last)
            # logger.info(last.get("content"))
            # last.get("content").replace("<tool_response>", "")
            # last.get("content").replace("</tool_response>", "")
            # state["messages"][-1]["content"] = (
            #     state["messages"][-1]["content"]
            #     .replace("<tool_response>", "")
            #     .replace("</tool_response>", "")
            # )
            logger.info(
                f"Updated last message content: {state['messages'][-1]['content']}"
            )
            # state["messages"].append(system_prompt)
        elif notAdded:
            # Add user input as the first message
            state["messages"].append({"role": "user", "content": prefixed_input})
        # Construct wrapped payload exactly like in playground
        # state["messages"].insert(
        #     0,
        #     {
        #         "role": "system",
        #         "content": (
        #             "You are Hermes, an intelligent travel assistant helping users book flights, check offers, and plan travel. "
        #             "You always reason step by step using the ReAct format:\n\n"
        #             "- Thought: Reflect on what the user wants or what the tool result shows.\n"
        #             "- Action: (Optional) If needed, call an appropriate tool using correct arguments.\n"
        #             "- Observation: (After tool calls) Summarize what the tool returned in clear, natural language.\n"
        #             "- Response: Speak to the user directly, answering clearly and politely, based on the observation.\n\n"
        #             "You follow this pattern for every turn. Always explain your reasoning clearly. After every tool result, "
        #             "summarize it in a human-friendly way unless the result is empty or failed.\n\n"
        #             "You are helpful, honest, and concise. If information is missing, ask a polite follow-up question. "
        #             "If the user’s intent is unclear, ask for clarification. Use markdown for formatting when helpful "
        #             "(e.g., bolding prices, flight dates).\n"
        #         ),
        #     },
        # )

        if isinstance(state.get("messages"), list):
            cleaned_messages = []

            for i, msg in enumerate(state["messages"]):
                is_last = i == len(state["messages"]) - 1
                if msg.get("role") == "tool":
                    if is_last:
                        cleaned_messages.append(msg)  # keep only last tool message
                    # else: skip earlier tool messages
                else:
                    cleaned_messages.append(msg)  # keep non-tool messages

            state["messages"] = cleaned_messages
        bedrock_prompt_payload = {"messages": state["messages"]}
        logger.info(
            "Constructed Bedrock prompt payload: %s",
            json.dumps(bedrock_prompt_payload, indent=2),
        )
        payload = {
            "prompt": get_tool_prompt_for_intent(state["intent"], state["messages"]),
            # "prompt": json.dumps(bedrock_prompt_payload),
            "max_tokens": 250,
            "temperature": 0.5,
            "top_p": 0.9,
            "top_k": 50,
        }
        logger.info(
            "Invoking Bedrock model with payload: %s", json.dumps(payload, indent=2)
        )
        # Invoke model
        response = client.invoke_model(
            modelId=settings.BEDROCK_MODEL_ID,
            body=json.dumps(payload),
            contentType="application/json",
        )

        model_response = json.loads(response["body"].read())
        logger.info(f"Model response: {model_response}")
        # Extract final response from first content block
        final_response = model_response["outputs"][0]["text"]

        state["messages"].append(
            {"role": "assistant", "content": final_response.strip()}
        )

        return {**state, "messages": state["messages"]}
