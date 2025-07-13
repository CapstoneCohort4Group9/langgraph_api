from src.state.state import State
from src import logger
from src.config.settings import load_config

settings = load_config()


class AppendToolResultNode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        pass

    def process(self, state: State) -> State:
        # Get last assistant message
        last_msg = state["messages"][-1]

        # Check if it's an assistant response and has <tool_call> tag
        if last_msg["role"] == "assistant":
            content = last_msg.get("content", "")

            # Use regex or basic check for <tool_call> tag
            if "<tool_call>" in content and "</tool_call>" in content:
                tool_msg = {
                    "role": "tool",
                    "content": f"<tool_response>{state['tool_output']}</tool_response>",
                }
                state["messages"].append(tool_msg)
        logger.info(f"Appended tool result: {state['tool_output']}")
        return state
