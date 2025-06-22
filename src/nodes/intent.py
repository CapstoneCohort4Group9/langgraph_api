from src.state.state import State
from src.tools.tools import detect_intent_tool


class IntentToolNode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        pass

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        print("Running intent detection...", state["messages"])
        intent = detect_intent_tool.run(state["messages"][0].content)
        print("DEBUG: Detected intent:", intent)
        return {"intentMessage": intent}
