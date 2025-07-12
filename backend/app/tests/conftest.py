"""
Test configuration and fixtures
"""
import os
import pytest

# Set environment variables BEFORE any imports that might use them
os.environ.setdefault("TESTING", "true")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-32-characters-long-secure")
os.environ.setdefault("POSTGRES_SERVER", "localhost")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("DATABASE_URL", "postgresql://test_user:test_password@localhost/test_db")
os.environ.setdefault("MPESA_CONSUMER_KEY", "test_consumer_key")
os.environ.setdefault("MPESA_CONSUMER_SECRET", "test_consumer_secret")
os.environ.setdefault("MPESA_SHORTCODE", "123456")
os.environ.setdefault("MPESA_PASSKEY", "test_passkey")
os.environ.setdefault("MPESA_CALLBACK_URL", "http://localhost:8000/callback")
os.environ.setdefault("MPESA_TIMEOUT_URL", "http://localhost:8000/timeout")
os.environ.setdefault("MPESA_RESULT_URL", "http://localhost:8000/result")
os.environ.setdefault("ETHEREUM_RPC_URL", "https://mainnet.infura.io/v3/test")
os.environ.setdefault("ETHEREUM_PRIVATE_KEY", "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef")
os.environ.setdefault("TRON_RPC_URL", "https://api.trongrid.io")
os.environ.setdefault("TRON_API_KEY", "test_api_key")
os.environ.setdefault("TRON_PRIVATE_KEY", "test_private_key")
os.environ.setdefault("BITCOIN_RPC_URL", "http://localhost:8332")
os.environ.setdefault("BITCOIN_RPC_USER", "test_user")
os.environ.setdefault("BITCOIN_RPC_PASSWORD", "test_password")
os.environ.setdefault("ENCRYPTION_KEY", "test-encryption-key-32-characters-long-secure")
os.environ.setdefault("WEBHOOK_SECRET", "test-webhook-secret")
os.environ.setdefault("EXCHANGE_RATE_API_KEY", "test-exchange-rate-api-key")