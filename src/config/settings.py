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

    INTENT_API_URL: str = os.getenv("INTENT_API_URL", "")
    SENTIMENT_API_URL: str = os.getenv("SENTIMENT_API_URL", "")
    RAG_API_URL: str = os.getenv("RAG_API_URL", "")
    SEARCH_FLIGHT_API_URL: str = os.getenv("SEARCH_FLIGHT_API_URL", "")
    BOOK_FLIGHT_API_URL: str = os.getenv("BOOK_FLIGHT_API_URL", "")
    BAGGAGE_STATUS_API_URL: str = os.getenv("BAGGAGE_STATUS_API_URL", "")
    CHECK_FLIGHT_OFFERS_API_URL: str = os.getenv("CHECK_FLIGHT_OFFERS_API_URL", "")
    NON_AI_API_URL: str = os.getenv("NON_AI_API_URL", "")

    BEDROCK_REGION: str = os.getenv("BEDROCK_REGION", "")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "")

    # Optional for STS
    AWS_REGION: str = os.getenv("AWS_REGION", "us-east-1")
    API_KEY: str = os.getenv("API_KEY", "")
    AWS_PROFILE: str = os.getenv("AWS_PROFILE", "")
    ASSUME_ROLE_ARN: str = os.getenv("ASSUME_ROLE_ARN", "")

    class Config:
        env_file = ".env"
        extra = "allow"  # Accept unmodeled fields without failing


def load_config() -> Config:
    """Load and validate configuration."""
    return Config()
