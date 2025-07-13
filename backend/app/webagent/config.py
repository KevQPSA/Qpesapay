"""
WebAgent Configuration for Qpesapay Integration
"""

import os
from typing import Dict, Optional
from pydantic import BaseSettings, Field


class WebAgentConfig(BaseSettings):
    """Configuration for WebAgent integration"""
    
    # API Keys
    google_search_key: str = Field(..., env="GOOGLE_SEARCH_KEY")
    jina_api_key: str = Field(..., env="JINA_API_KEY") 
    dashscope_api_key: str = Field(..., env="DASHSCOPE_API_KEY")
    
    # Model Configuration
    webdancer_model_path: Optional[str] = Field(None, env="WEBDANCER_MODEL_PATH")
    websailor_model_path: Optional[str] = Field(None, env="WEBSAILOR_MODEL_PATH")
    
    # Server Configuration
    model_server_host: str = Field("127.0.0.1", env="MODEL_SERVER_HOST")
    model_server_port: int = Field(6001, env="MODEL_SERVER_PORT")
    
    # Agent Configuration
    max_llm_calls_per_run: int = Field(40, env="MAX_LLM_CALL_PER_RUN")
    max_token_length: int = Field(31744, env="MAX_TOKEN_LENGTH")  # 31*1024 - 500
    max_multiquery_num: int = Field(3, env="MAX_MULTIQUERY_NUM")
    
    # Financial-specific Configuration
    crypto_apis: Dict[str, str] = {
        "coinmarketcap": os.getenv("COINMARKETCAP_API_KEY", ""),
        "coingecko": os.getenv("COINGECKO_API_KEY", ""),
        "binance": os.getenv("BINANCE_API_KEY", "")
    }
    
    # Compliance Configuration
    regulatory_sources: Dict[str, str] = {
        "cma_kenya": "https://www.cma.or.ke",
        "cbk": "https://www.centralbank.go.ke",
        "fatf": "https://www.fatf-gafi.org"
    }
    
    # Cache Configuration
    enable_cache: bool = Field(True, env="WEBAGENT_ENABLE_CACHE")
    cache_ttl: int = Field(3600, env="WEBAGENT_CACHE_TTL")  # 1 hour
    
    # Security Configuration
    enable_rate_limiting: bool = Field(True, env="WEBAGENT_RATE_LIMITING")
    max_requests_per_minute: int = Field(60, env="WEBAGENT_MAX_REQUESTS_PER_MINUTE")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global configuration instance
webagent_config = WebAgentConfig()


def get_webagent_config() -> WebAgentConfig:
    """Get WebAgent configuration instance"""
    return webagent_config


def validate_api_keys() -> Dict[str, bool]:
    """Validate required API keys are present"""
    config = get_webagent_config()
    
    validation_results = {
        "google_search": bool(config.google_search_key),
        "jina_api": bool(config.jina_api_key),
        "dashscope": bool(config.dashscope_api_key),
        "crypto_apis": any(config.crypto_apis.values()),
    }
    
    return validation_results


def get_model_server_url() -> str:
    """Get the model server URL"""
    config = get_webagent_config()
    return f"http://{config.model_server_host}:{config.model_server_port}/v1"
