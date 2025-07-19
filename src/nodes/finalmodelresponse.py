from nodes.callbedrockmodel import CallingBedrockModelToolNode
from state.state import State
import re


class FinalModelResponseNode:
    def __init__(self):
        self.model_node = CallingBedrockModelToolNode()  # Reuse same logic

    def process(self, state: State) -> State:
        messages = state.get("messages", [])

        if not messages:
            return state  # No messages at all

        last_msg = messages[-1]
        if (
            last_msg.get("role") == "tool"
            and isinstance(last_msg.get("content"), str)
            and re.search(
                r"<tool_response>.*?</tool_response>", last_msg["content"], re.DOTALL
            )
        ):
            return self.model_node.process(state)
