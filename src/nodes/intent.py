from src.state.state import State
from src.tools.tools import get_intent_tool
from src import logger


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

        intentSearchQuery = ""
        logger.info(f"state in intent detection...{state}")
        # if (
        #     isinstance(state.get("messages"), list)
        #     and len(state["messages"]) > 0
        #     and state["messages"][-1].get("role") == "assistant"
        # ):
        #     intentSearchQuery = (
        #         state["messages"][-2]["content"]
        #         + " "
        #         + state["messages"][-1]["content"]
        #         + " "
        #         + state["input"]
        #     )
        # else:
        #     intentSearchQuery = state["input"]
        intentSearchQuery = state["input"]
        # if state["input"] == " Yes, please book that flight":
        #     intent = "confirm_booking"
        logger.info(f"Running intent detection...{intentSearchQuery}")
        intent = get_intent_tool.run(intentSearchQuery)

        logger.info(f"Detected intent: {intent}")
        return {**state, "intent": intent}
