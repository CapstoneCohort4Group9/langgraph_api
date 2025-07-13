from src.state.state import State
from src.utils.tool_register import get_tool_prompt_for_intent
from src import logger
import json
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from src.config.settings import load_config

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

        # Compose user input with intent/sentiment prefix
        prefixed_input = f"[intent={state['intent']}][sentiment={state['sentiment']}] {state['input']}"

        state["messages"].append({"role": "user", "content": prefixed_input})

        # Retrieve the system prompt for the intent
        system_tool_prompt = get_tool_prompt_for_intent(state["intent"])
        context = state.get("tool_output")

        system_prompt = {
            "role": "system",
            "content": (system_tool_prompt or "") + "\n\nContext: " + (context or ""),
        }

        # Construct wrapped payload exactly like in playground
        bedrock_prompt_payload = {"messages": state["messages"]}

        payload = {
            "prompt": json.dumps(bedrock_prompt_payload),
            "max_tokens": 384,
            "temperature": 0.5,
        }
        logger.info(f"Invoking Bedrock model with payload: {payload}")
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
