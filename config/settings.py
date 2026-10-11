from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Application Config
    environment: str = "development"
    debug: bool = True
    
    # Twilio Webhook & API
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    
    # AI Orchestration
    openai_api_key: str
    
    # Storage
    database_url: str
    
    # External Actions (Mocked for Demo)
    stripe_secret_key: str = "sk_test_mock123"

    # Automatically loads from a .env file during local development
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings() -> Settings:
    """
    Returns a cached instance of the settings. 
    This prevents re-reading the .env file on every import.
    """
    return Settings()

# Usage across the app: 
# from config.settings import get_settings
# settings = get_settings()