from src.state.state import State
from src.agents.summarizer import summarize


class SummarizerNode:
    """
    Summarizer Node logic
    """

    def __init__(self):
        pass

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration.
        """
        print("Running summarization...", state)
        print("DEBUG:", state)
        summary = summarize(state)
        print("DEBUG: Summary result:", summary)
        return {"txt": summary}
