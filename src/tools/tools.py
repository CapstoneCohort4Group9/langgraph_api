from langchain.tools import tool
from utils.prediction import PredictionPipeline

# @tool
# def detect_sentiment_tool(text: str) -> str:
#     result = sentiment_pipeline(text)[0]
#     return f"Label: {result['label']}, Score: {result['score']}"


@tool
def detect_intent_tool(text: str) -> str:
    """this function detects the intent of the given text using a pre-trained model."""
    result = PredictionPipeline(text).predict()
    print(f"Predicted Intent: {result}")
    return result["predicted_label"]
