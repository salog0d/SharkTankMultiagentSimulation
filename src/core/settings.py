from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    azure_deployment: str = Field(..., alias="AZURE_DEPLOYMENT")
    azure_api_version: str = Field(..., alias="AZURE_API_VERSION")
    azure_api_key: str = Field(..., alias="AZURE_API_KEY")
    azure_endpoint: str = Field(..., alias="AZURE_ENDPOINT")

    class Config:
        env_file = ENV_PATH
        env_file_encoding = "utf-8"
        populate_by_name = True

settings = Settings()
