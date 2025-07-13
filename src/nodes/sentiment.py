from src.state.state import State
from src.tools.tools import get_sentiment_tool
from src import logger


class SentimentToolNode:
    """
    Node logic enhanced with tool integration.
    """

    def __init__(self):
        pass

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        logger.info(f"Running sentiment analysis...{state['input']}")
        sentiment = get_sentiment_tool.run(state["input"])
        logger.info(f"Analysed sentiment: {sentiment}")
        return {**state, "sentiment": sentiment}
