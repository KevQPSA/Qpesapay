"""
Comprehensive security tests for Qpesapay backend.
Tests all security features including authentication, validation, and protection mechanisms.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import Mock, patch
from decimal import Decimal

from app.main import app
from app.core.security import (
    create_tokens, validate_password_strength, get_password_hash, 
    verify_password, blacklist_token, is_token_blacklisted
)
from app.core.validation import (
    validate_email_address, validate_phone_number, validate_monetary_amount,
    sanitize_string, ValidationError
)
from app.core.security_audit import WebhookSecurityValidator, EndpointSecurityEnforcer
from app.models.user import User
from app.core.security_audit import WebhookSecurityValidator, EndpointSecurityEnforcer
from app.models.user import User
from app.schemas.user import UserCreate

client = TestClient(app)


class TestPasswordSecurity:
    """Test password security features."""
    
    def test_password_strength_validation(self):
        """Test password strength validation."""
        # Test weak passwords
        weak_passwords = [
            "weak",
            "password123",
            "Password123",
            "123456789012",
            "ALLUPPERCASE123!",
        ]
        
        for password in weak_passwords:
            is_valid, errors = validate_password_strength(password)
            assert not is_valid, f"Password '{password}' should be invalid"
            assert len(errors) > 0, f"Password '{password}' should have errors"
    
    def test_strong_password_validation(self):
        """Test strong password validation."""
        strong_passwords = [
            "MySecureP@ssw0rd2024",
            "Str0ng!P@ssw0rd#123",
            "C0mpl3x&S3cur3!Pass",
        ]
        
        for password in strong_passwords:
            is_valid, errors = validate_password_strength(password)
            assert is_valid, f"Password '{password}' should be valid, errors: {errors}"
            assert len(errors) == 0, f"Password '{password}' should have no errors"
    
    def test_password_hashing_and_verification(self):
        """Test password hashing and verification."""
        password = "MySecureP@ssw0rd2024"
        
        # Test hashing
        hashed = get_password_hash(password)
        assert hashed != password, "Password should be hashed"
        assert len(hashed) > 50, "Hash should be long enough"
        
        # Test verification
        assert verify_password(password, hashed), "Password verification should succeed"
        assert not verify_password("wrong-password", hashed), "Wrong password should fail"


class TestInputValidation:
    """Test input validation and sanitization."""
    
    def test_email_validation(self):
        """Test email validation."""
        # Valid emails (using real domains that accept email)
        valid_emails = [
            "test@gmail.com",
            "user.name@yahoo.com",
            "valid+email@outlook.com",
        ]
        
        for email in valid_emails:
            try:
                result = validate_email_address(email)
                assert result.lower() == email.lower(), f"Email {email} should be normalized"
            except ValidationError:
                pytest.fail(f"Valid email {email} was rejected")
        
        # Invalid emails
        invalid_emails = [
            "invalid-email",
            "@domain.com",
            "user@",
            "user space@domain.com",
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                validate_email_address(email)
    
    def test_phone_validation(self):
        """Test phone number validation."""
        # Valid Kenya phone numbers
        valid_phones = [
            "0712345678",
            "+254712345678", 
            "254712345678",
            "0723456789",
        ]
        
        for phone in valid_phones:
            try:
                result = validate_phone_number(phone, "KE")
                assert result.startswith("+254"), f"Phone {phone} should be normalized to +254 format"
            except ValidationError:
                pytest.fail(f"Valid phone {phone} was rejected")
        
        # Invalid phone numbers
        invalid_phones = [
            "123456",
            "+1234567890",
            "0812345678",  # Wrong prefix for Kenya
            "abcdefghij",
        ]
        
        for phone in invalid_phones:
            with pytest.raises(ValidationError):
                validate_phone_number(phone, "KE")
    
    def test_monetary_validation(self):
        """Test monetary amount validation."""
        # Valid amounts
        valid_amounts = ["100.50", "0.01", "999999.99", Decimal("50.25")]
        
        for amount in valid_amounts:
            try:
                result = validate_monetary_amount(amount)
                assert isinstance(result, Decimal), f"Amount {amount} should return Decimal"
                assert result >= 0, f"Amount {amount} should be non-negative"
            except ValidationError:
                pytest.fail(f"Valid amount {amount} was rejected")
        
        # Invalid amounts
        invalid_amounts = ["-100.00", "999999999999.99", "100.999", "NaN", "Infinity"]
        
        for amount in invalid_amounts:
            with pytest.raises(ValidationError):
                validate_monetary_amount(amount)
    
    def test_string_sanitization(self):
        """Test string sanitization."""
        # XSS attempts
        xss_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            '<img src=x onerror=alert("xss")>',
        ]
        
        for xss_input in xss_inputs:
            sanitized = sanitize_string(xss_input)
            assert "<script>" not in sanitized.lower(), f"XSS should be sanitized: {sanitized}"
            assert "javascript:" not in sanitized.lower(), f"JavaScript should be sanitized: {sanitized}"


class TestJWTSecurity:
    """Test JWT token security."""
    
    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification."""
        user_id = "test-user-123"
        
        # Create tokens
        tokens = create_tokens(user_id)
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert "token_type" in tokens
        assert tokens["token_type"] == "bearer"
    
    def test_token_blacklisting(self):
        """Test token blacklisting functionality."""
        user_id = "test-user-123"
        tokens = create_tokens(user_id)
        access_token = tokens["access_token"]
        
        # Token should not be blacklisted initially
        assert not is_token_blacklisted(access_token)
        
        # Blacklist token
        blacklist_token(access_token)
        
        # Token should now be blacklisted
        assert is_token_blacklisted(access_token)


class TestWebhookSecurity:
    """Test webhook security features."""
    
    def test_webhook_signature_validation(self):
        """Test webhook signature validation."""
        payload = b'{"test": "data"}'
        secret = "test-secret-key"
        
        # Generate valid signature
        import hmac
        import hashlib
        valid_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        # Test valid signature
        assert WebhookSecurityValidator.validate_mpesa_signature(
            payload, valid_signature, secret
        )
        
        # Test invalid signature
        assert not WebhookSecurityValidator.validate_mpesa_signature(
            payload, "invalid-signature", secret
        )
    
    def test_webhook_timestamp_validation(self):
        """Test webhook timestamp validation."""
        from datetime import datetime, timezone
        
        # Valid timestamp (current time)
        valid_timestamp = datetime.now(timezone.utc).isoformat()
        assert WebhookSecurityValidator.validate_webhook_timestamp(valid_timestamp)
        
        # Invalid timestamp (too old)
        old_timestamp = "2020-01-01T00:00:00Z"
        assert not WebhookSecurityValidator.validate_webhook_timestamp(old_timestamp)
        
        # Invalid format
        invalid_timestamp = "not-a-timestamp"
        assert not WebhookSecurityValidator.validate_webhook_timestamp(invalid_timestamp)


class TestEndpointSecurity:
    """Test API endpoint security."""
    
    def test_payment_amount_validation(self):
        """Test payment amount validation."""
        # Valid amounts
        valid_amounts = ["100.50", "0.01", "999999.99"]
        for amount in valid_amounts:
            assert EndpointSecurityEnforcer.validate_payment_amount(amount)
        
        # Invalid amounts
        invalid_amounts = ["-100", "0", "1000001", "invalid"]
        for amount in invalid_amounts:
            assert not EndpointSecurityEnforcer.validate_payment_amount(amount)
    
    def test_webhook_payload_sanitization(self):
        """Test webhook payload sanitization."""
        malicious_payload = {
            "user_id": "<script>alert('xss')</script>",
            "amount": "100.50",
            "nested": {
                "field": "javascript:alert('xss')"
            },
            "number": 123,
            "boolean": True
        }
        
        sanitized = EndpointSecurityEnforcer.sanitize_webhook_payload(malicious_payload)
        
        # Check XSS is sanitized
        assert "<script>" not in sanitized["user_id"].lower()
        assert "javascript:" not in sanitized["nested"]["field"].lower()
        
        # Check valid data is preserved
        assert sanitized["amount"] == "100.50"
        assert sanitized["number"] == 123
        assert sanitized["boolean"] is True


class TestUserModelSecurity:
    """Test User model security features."""
    
    def test_account_lockout_mechanism(self):
        """Test account lockout after failed attempts."""
        user = User()
        user.failed_login_attempts = 0
        user.locked_until = None
        
        # Test progressive lockout
        for i in range(7):
            user.increment_failed_login_attempts()
            if i >= 4:  # After 5th attempt
                assert user.is_locked, f"Account should be locked after {i+1} attempts"
            else:
                assert not user.is_locked, f"Account should not be locked after {i+1} attempts"
    
    def test_password_reset_token_security(self):
        """Test password reset token security."""
        user = User()
        
        # Set password reset token
        user.set_password_reset_token("test-token-123", 30)
        
        # Valid token should work
        assert user.is_password_reset_token_valid("test-token-123")
        
        # Invalid token should fail
        assert not user.is_password_reset_token_valid("wrong-token")
        
        # Clear token
        user.clear_password_reset_token()
        assert not user.is_password_reset_token_valid("test-token-123")


@pytest.mark.asyncio
async def test_security_integration():
    """Test complete security integration."""
    # Test user registration with security validation
    user_data = {
        "email": "test@gmail.com",
        "phone_number": "0712345678",
        "first_name": "John",
        "last_name": "Doe",
        "password": "MySecureP@ssw0rd2024"
    }
    
    try:
        user_schema = UserCreate(**user_data)
        assert user_schema.email == "test@gmail.com"
        assert user_schema.phone_number == "+254712345678"
        assert user_schema.password == "MySecureP@ssw0rd2024"
    except Exception as e:
        pytest.fail(f"Security integration test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
