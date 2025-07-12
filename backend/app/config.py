from pydantic_settings import BaseSettings
from pydantic import Field, validator
from functools import lru_cache
from typing import List, Optional
import secrets
import os

class Settings(BaseSettings):
    # Application Configuration
    PROJECT_NAME: str = "Qpesapay"  # FIXED: Correct application name
    API_V1_STR: str = "/api/v1"
    IS_PRODUCTION: bool = Field(default=False, env="IS_PRODUCTION")

    # Security Configuration
    SECRET_KEY: str = Field(
        default="default-secret-key-for-ci-cd-only-32-characters-long-secure",
        min_length=32,
        description="JWT secret key"
    )
    ENCRYPTION_KEY: str = Field(
        default="default-encryption-key-for-ci-cd-only-32-characters-long",
        min_length=32,
        description="Data encryption key"
    )
    WEBHOOK_SECRET: str = Field(
        default="default-webhook-secret-for-ci-cd-32-chars",
        min_length=16,
        description="Webhook signature secret"
    )

    # JWT Configuration
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=5, le=60)  # SECURITY: Reduced from 8 days to 30 minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, ge=1, le=30)

    # Password Policy
    MIN_PASSWORD_LENGTH: int = Field(default=12, ge=8, le=128)
    REQUIRE_PASSWORD_UPPERCASE: bool = Field(default=True)
    REQUIRE_PASSWORD_LOWERCASE: bool = Field(default=True)
    REQUIRE_PASSWORD_NUMBERS: bool = Field(default=True)
    REQUIRE_PASSWORD_SPECIAL: bool = Field(default=True)

    # Account Security
    MAX_LOGIN_ATTEMPTS: int = Field(default=5, ge=3, le=10)
    ACCOUNT_LOCKOUT_MINUTES: int = Field(default=15, ge=5, le=1440)
    PASSWORD_RESET_EXPIRE_MINUTES: int = Field(default=30, ge=10, le=120)

    # Rate Limiting
    DEFAULT_RATE_LIMIT: str = Field(default="60/minute")
    AUTH_RATE_LIMIT: str = Field(default="5/minute")
    PAYMENT_RATE_LIMIT: str = Field(default="10/minute")

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")

    # Database
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="password")
    POSTGRES_DB: str = Field(default="qpesapay_test")
    DATABASE_URL: str = Field(default="postgresql://postgres:password@localhost/qpesapay_test")

    # M-Pesa
    MPESA_CONSUMER_KEY: str = Field(default="test_consumer_key")
    MPESA_CONSUMER_SECRET: str = Field(default="test_consumer_secret")
    MPESA_SHORTCODE: str = Field(default="174379")
    MPESA_PASSKEY: str = Field(default="test_passkey")
    MPESA_CALLBACK_URL: str = Field(default="https://example.com/callback")
    MPESA_TIMEOUT_URL: str = Field(default="https://example.com/timeout")
    MPESA_RESULT_URL: str = Field(default="https://example.com/result")

    # Blockchain
    ETHEREUM_RPC_URL: str = Field(default="https://mainnet.infura.io/v3/test")
    ETHEREUM_PRIVATE_KEY: str = Field(default="0x" + "0" * 64)
    TRON_RPC_URL: str = Field(default="https://api.trongrid.io")
    TRON_API_KEY: str = Field(default="test_tron_api_key")
    TRON_PRIVATE_KEY: str = Field(default="0" * 64)
    BITCOIN_RPC_URL: str = Field(default="http://localhost:8332")
    BITCOIN_RPC_USER: str = Field(default="bitcoin")
    BITCOIN_RPC_PASSWORD: str = Field(default="password")

    # Security
    EXCHANGE_RATE_API_KEY: str = Field(default="test_exchange_rate_api_key")

    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        """Validate SECRET_KEY strength."""
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        if v == 'your-secret-key-here' or v == 'changeme':
            raise ValueError('SECRET_KEY must not be a default value')
        return v

    @validator('BACKEND_CORS_ORIGINS')
    def validate_cors_origins(cls, v):
        """Validate CORS origins."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v

    @validator('IS_PRODUCTION')
    def validate_production_settings(cls, v, values):
        """Validate production-specific settings."""
        if v:  # If production
            # Ensure secure settings in production
            if values.get('LOG_LEVEL') == 'DEBUG':
                raise ValueError('DEBUG logging not allowed in production')
            if 'localhost' in str(values.get('BACKEND_CORS_ORIGINS', [])):
                raise ValueError('localhost CORS origins not allowed in production')

            # Ensure no default values in production
            if values.get('SECRET_KEY', '').startswith('default-'):
                raise ValueError('Default SECRET_KEY not allowed in production')
            if values.get('POSTGRES_PASSWORD') == 'password':
                raise ValueError('Default database password not allowed in production')
        return v

    @validator('SECRET_KEY')
    def warn_default_secrets(cls, v):
        """Warn about default secrets in non-production environments."""
        if v.startswith('default-') and not (os.getenv('CI') or os.getenv('GITHUB_ACTIONS')):
            import warnings
            warnings.warn(
                "Using default SECRET_KEY. Set proper environment variables for production.",
                UserWarning
            )
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'

        # Note: In Pydantic v2, sensitive field exclusion is handled differently


def validate_environment():
    """Validate critical environment variables are set."""
    # Skip validation if we're in testing mode or CI/CD
    if (os.getenv('TESTING') == 'true' or
        os.getenv('CI') == 'true' or
        os.getenv('GITHUB_ACTIONS') == 'true'):
        return

    required_vars = [
        'SECRET_KEY',
        'ENCRYPTION_KEY',
        'WEBHOOK_SECRET',
        'DATABASE_URL',
        'POSTGRES_SERVER',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_DB'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


@lru_cache()
def get_settings():
    """Get validated settings instance."""
    validate_environment()
    return Settings()


settings = get_settings()