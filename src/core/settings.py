from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field
from functools import lru_cache

class Settings(BaseSettings):

    app_name: Optional[str] = Field(None, alias="APP_NAME")

    azure_api_key: Optional[str] = Field(None, alias="AZURE_API_KEY")
    azure_endpoint: Optional[str] = Field(None, alias="AZURE_ENDPOINT")
    azure_deployment: Optional[str] = Field(None, alias="AZURE_DEPLOYMENT")
    azure_api_version: Optional[str] = Field(None, alias="AZURE_API_VERSION")

@lru_cache
def get_settings():
    return Settings

settings = get_settings()
