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

    class Config:
        env_file = ".env"


def load_config() -> Config:
    """Load and validate configuration."""
    return Config()
