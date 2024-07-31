import logging
import os

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from pydantic_settings import BaseSettings, SettingsConfigDict

# check if the server started from the correct directory
absolute_path = os.path.abspath("api_server.py")
print(f" absolute path is {absolute_path}")
directory_name = os.path.dirname(absolute_path)
if os.getcwd() != directory_name:
    raise Exception(
        "Server should always start from the directory where the server.py file is located"
    )


# --- GLOBAL & ENVIRONMENT VARIABLES
class Settings(BaseSettings):
    """Settings class for the application."""

    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    # Azure OpenAI settings
    AZURE_OPENAI_DEPLOYMENT_NAME: str
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_API_VERSION: str = "2024-02-01"

    # Azure Search settings
    AZURE_SEARCH_SERVICE_ENDPOINT: str
    AZURE_SEARCH_INDEX_NAME: str
    AZURE_SEARCH_INDEXER_NAME: str
    AZURE_SEARCH_API_KEY: str
    AZURE_SEARCH_TOP_K: int = 2
    SEMENTIC_CONFIGURATION_NAME: str

    # Azure Storage settings
    AZURE_STORAGE_ACCOUNT_NAME: str
    AZURE_STORAGE_ACCOUNT_KEY: str
    AZURE_CONTAINER_NAME: str

    # FastAPI settings
    FASTAPI_HOST: str = "localhost"
    FASTAPI_PORT: int = 8080
    STREAMLIT_PORT: int = 8501
    DEV_MODE: bool = True


def initialize():
    logger = logging.getLogger("uvicorn.default")
    settings = Settings()

    search_client = SearchClient(
        settings.AZURE_SEARCH_SERVICE_ENDPOINT,
        settings.AZURE_SEARCH_INDEX_NAME,
        AzureKeyCredential(settings.AZURE_SEARCH_API_KEY),
    )
    return settings, logger, search_client


settings, logger, search_client = initialize()
