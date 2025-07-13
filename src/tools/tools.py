from langchain.tools import tool
from src.config.settings import load_config
import httpx
from src import logger

settings = load_config()


@tool
def get_intent_tool(text: str) -> str:
    """this function detects the intent of the given text."""
    logger.info(f"Intent API URL: {settings.INTENT_API_URL}")
    response = httpx.post(settings.INTENT_API_URL, json={"text": f"{text}"})
    result = response.json()["intent"]
    logger.info(f"Predicted Intent: {result}")
    return result


@tool
def get_sentiment_tool(text: str) -> str:
    """this function analysis the sentiment of the given text."""
    print(f"DEBUG: Sentiment API URL: {settings.SENTIMENT_API_URL}")
    logger.info(f"Sentiment API URL: {settings.SENTIMENT_API_URL}")
    response = httpx.post(settings.SENTIMENT_API_URL, json={"text": f"{text}"})
    result = response.json()["sentiment"]
    logger.info(f"Analysed Sentiment: {result}")
    return result
