import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config(BaseSettings):
    # API Keys
    langchain_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
    langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "convo_ai")
    langchain_endpoint: str = os.getenv("LANGCHAIN_ENDPOINT", "")
    huggingface_api_key: str = os.getenv("HUGGINGFACE_API_KEY", "")
    openai_api_key: Optional[str] = os.getenv(
        "OPENAI_API_KEY",
        "",
    )

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Model Settings
    use_gpu: bool = True  # Set to False if GPU is not available

    # Agent Settings
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    intent_model: str = "facebook/bart-large-mnli"

    INTENT_API_URL: str
    SENTIMENT_API_URL: str
    RAG_API_URL: str
    SEARCH_FLIGHT_API_URL: str
    BOOK_FLIGHT_API_URL: str
    BAGGAGE_STATUS_API_URL: str
    CHECK_FLIGHT_OFFERS_API_URL: str

    BEDROCK_REGION: str
    BEDROCK_MODEL_ID: str

    # Optional for STS
    AWS_PROFILE: str = ""
    ASSUME_ROLE_ARN: str = ""

    class Config:
        env_file = ".env"
        extra = "allow"  # Accept unmodeled fields without failing


def load_config() -> Config:
    """Load and validate configuration."""
    return Config()
