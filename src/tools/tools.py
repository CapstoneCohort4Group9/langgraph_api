from langchain.tools import tool
from src.utils.prediction import PredictionPipeline


@tool
def detect_intent_tool(text: str) -> str:
    """this function detects the intent of the given text using a pre-trained model."""
    result = PredictionPipeline(text).predict()
    print(f"Predicted Intent: {result}")
    return result["predicted_label"]
