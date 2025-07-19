from src.state.state import State
import re
from src import logger
from src.config.settings import load_config

settings = load_config()


class ParseToolCallToolNode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        pass

    def process(self, state: State) -> State:
        """Extracts <tool_call>{...}</tool_call> block from the assistant's response"""

        last_msg = state["messages"][-1]
        logger.info(f"Last message: {last_msg}")
        # ✅ Check if this message was from the assistant
        if last_msg.get("role") != "assistant":
            return {**state, "tool_call": ""}

        content = last_msg.get("content", "")
        if not isinstance(content, str):
            return {**state, "tool_call": ""}

        # ✅ Extract tool call block using regex
        match = re.search(r"<tool_call>(.*?)</tool_call>", content, re.DOTALL)
        if not match:
            return {**state, "tool_call": ""}

        tool_json_str = match.group(1).strip()
        logger.info(f"Extracted tool call: {tool_json_str}")
        return {**state, "tool_call": tool_json_str}
