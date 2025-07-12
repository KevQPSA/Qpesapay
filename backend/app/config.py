from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Qpeasa"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    IS_PRODUCTION: bool = False
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    # M-Pesa
    MPESA_CONSUMER_KEY: str
    MPESA_CONSUMER_SECRET: str
    MPESA_SHORTCODE: str
    MPESA_PASSKEY: str
    MPESA_CALLBACK_URL: str
    MPESA_TIMEOUT_URL: str
    MPESA_RESULT_URL: str

    # Blockchain
    ETHEREUM_RPC_URL: str
    ETHEREUM_PRIVATE_KEY: str
    TRON_RPC_URL: str
    TRON_API_KEY: str
    TRON_PRIVATE_KEY: str
    BITCOIN_RPC_URL: str
    BITCOIN_RPC_USER: str
    BITCOIN_RPC_PASSWORD: str

    # Security
    ENCRYPTION_KEY: str
    WEBHOOK_SECRET: str
    EXCHANGE_RATE_API_KEY: str

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()