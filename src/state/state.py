from typing_extensions import TypedDict, List, Dict


class State(TypedDict):
    """
    Represent the structure of the state used in graph
    """

    input: str
    intent: str
    sentiment: str
    rag_response: str
    api_response: str
    final_response: str
    messages: List[Dict[str, str]]
    tool_call: str  # Raw XML or JSON extracted
    tool_output: str
