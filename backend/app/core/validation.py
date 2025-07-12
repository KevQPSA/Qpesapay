"""
Input validation and sanitization utilities for Qpesapay backend.
Provides comprehensive validation for financial data, user inputs, and security.
"""

import re
import html
import unicodedata
from typing import Optional, Union, Any
from decimal import Decimal, InvalidOperation
from datetime import datetime
from uuid import UUID
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException

from app.config import settings


class ValidationError(Exception):
    """Custom validation error."""
    pass


def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize string input to prevent XSS and other attacks.
    
    Args:
        value: String to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized string
        
    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise ValidationError("Value must be a string")
    
    # Remove null bytes and control characters
    value = ''.join(char for char in value if ord(char) >= 32 or char in '\t\n\r')
    
    # Normalize unicode
    value = unicodedata.normalize('NFKC', value)
    
    # Remove dangerous JavaScript patterns
    dangerous_js_patterns = [
        r'javascript\s*:',
        r'on\w+\s*=',
        r'<\s*script',
        r'<\s*iframe',
        r'<\s*object',
        r'<\s*embed',
        r'<\s*link',
        r'<\s*meta',
        r'<\s*style',
    ]

    for pattern in dangerous_js_patterns:
        value = re.sub(pattern, '', value, flags=re.IGNORECASE)

    # HTML escape to prevent XSS
    value = html.escape(value, quote=True)

    # Strip whitespace
    value = value.strip()
    
    # Check length
    if max_length and len(value) > max_length:
        raise ValidationError(f"String too long (max {max_length} characters)")
    
    return value


def validate_email_address(email: str) -> str:
    """
    Validate and normalize email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        str: Normalized email address
        
    Raises:
        ValidationError: If email is invalid
    """
    try:
        # Sanitize first
        email = sanitize_string(email, max_length=255)
        
        # Validate email format
        valid = validate_email(email)
        return valid.normalized
        
    except EmailNotValidError as e:
        raise ValidationError(f"Invalid email address: {str(e)}")


def validate_phone_number(phone: str, country_code: str = "KE") -> str:
    """
    Validate and format phone number for Kenya.
    
    Args:
        phone: Phone number to validate
        country_code: Country code (default: KE for Kenya)
        
    Returns:
        str: Formatted phone number in E164 format
        
    Raises:
        ValidationError: If phone number is invalid
    """
    try:
        # Sanitize input
        phone = sanitize_string(phone, max_length=20)
        
        # Parse phone number
        parsed = phonenumbers.parse(phone, country_code)
        
        # Validate for Kenya specifically
        if country_code == "KE":
            # Kenya mobile numbers start with 7 (after country code)
            national_number = str(parsed.national_number)
            if not (national_number.startswith('7') and len(national_number) == 9):
                raise ValidationError("Invalid Kenya mobile number format")
        
        # Validate number
        if not phonenumbers.is_valid_number(parsed):
            raise ValidationError("Invalid phone number")
        
        # Return in E164 format
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        
    except NumberParseException as e:
        raise ValidationError(f"Invalid phone number: {str(e)}")


def validate_monetary_amount(amount: Union[str, int, float, Decimal]) -> Decimal:
    """
    Validate and convert monetary amount to Decimal.
    
    Args:
        amount: Amount to validate
        
    Returns:
        Decimal: Validated amount
        
    Raises:
        ValidationError: If amount is invalid
    """
    try:
        # Convert to Decimal (never use float for money!)
        if isinstance(amount, str):
            # Remove any currency symbols and whitespace
            amount = re.sub(r'[^\d.-]', '', amount.strip())
        
        decimal_amount = Decimal(str(amount))
        
        # Check for reasonable bounds
        if decimal_amount < 0:
            raise ValidationError("Amount cannot be negative")
        
        if decimal_amount > Decimal('999999999.99'):  # 999 million max
            raise ValidationError("Amount too large")
        
        # Check decimal places (max 2 for currency)
        if decimal_amount.as_tuple().exponent < -2:
            raise ValidationError("Amount cannot have more than 2 decimal places")
        
        return decimal_amount
        
    except (InvalidOperation, ValueError) as e:
        raise ValidationError(f"Invalid monetary amount: {str(e)}")


def validate_uuid(uuid_string: str) -> UUID:
    """
    Validate UUID string.
    
    Args:
        uuid_string: UUID string to validate
        
    Returns:
        UUID: Validated UUID object
        
    Raises:
        ValidationError: If UUID is invalid
    """
    try:
        uuid_string = sanitize_string(uuid_string, max_length=36)
        return UUID(uuid_string)
    except ValueError as e:
        raise ValidationError(f"Invalid UUID: {str(e)}")


def validate_password(password: str) -> str:
    """
    Validate password against security policy.
    
    Args:
        password: Password to validate
        
    Returns:
        str: Validated password
        
    Raises:
        ValidationError: If password is invalid
    """
    if not isinstance(password, str):
        raise ValidationError("Password must be a string")
    
    # Import here to avoid circular imports
    from app.core.security import validate_password_strength
    
    is_valid, errors = validate_password_strength(password)
    if not is_valid:
        raise ValidationError(f"Password validation failed: {'; '.join(errors)}")
    
    return password


def validate_wallet_address(address: str, currency: str) -> str:
    """
    Validate cryptocurrency wallet address.
    
    Args:
        address: Wallet address to validate
        currency: Currency type (BTC, ETH, TRX)
        
    Returns:
        str: Validated address
        
    Raises:
        ValidationError: If address is invalid
    """
    address = sanitize_string(address, max_length=100)
    
    if currency.upper() == "BTC":
        # Bitcoin address validation (simplified)
        if not re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^bc1[a-z0-9]{39,59}$', address):
            raise ValidationError("Invalid Bitcoin address format")
    
    elif currency.upper() == "ETH":
        # Ethereum address validation
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            raise ValidationError("Invalid Ethereum address format")
    
    elif currency.upper() == "TRX":
        # Tron address validation
        if not re.match(r'^T[A-Za-z1-9]{33}$', address):
            raise ValidationError("Invalid Tron address format")
    
    else:
        raise ValidationError(f"Unsupported currency: {currency}")
    
    return address


def sanitize_sql_input(value: Any) -> Any:
    """
    Sanitize input to prevent SQL injection.
    Note: This is a backup - always use parameterized queries!
    
    Args:
        value: Value to sanitize
        
    Returns:
        Any: Sanitized value
    """
    if isinstance(value, str):
        # Remove dangerous SQL keywords and characters
        dangerous_patterns = [
            r"('|(\\'))",  # Single quotes
            r'("|(\\""))',  # Double quotes  
            r'(;|(\s*;\s*))',  # Semicolons
            r'(\s*(union|select|insert|update|delete|drop|create|alter|exec|execute)\s+)',  # SQL keywords
            r'(--|\s*--\s*)',  # SQL comments
            r'(/\*|\*/)',  # SQL block comments
        ]
        
        for pattern in dangerous_patterns:
            value = re.sub(pattern, '', value, flags=re.IGNORECASE)
    
    return value


def validate_api_key(api_key: str) -> str:
    """
    Validate API key format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        str: Validated API key
        
    Raises:
        ValidationError: If API key is invalid
    """
    api_key = sanitize_string(api_key, max_length=128)
    
    # API key should be alphanumeric with specific length
    if not re.match(r'^[a-zA-Z0-9]{32,128}$', api_key):
        raise ValidationError("Invalid API key format")
    
    return api_key


def validate_transaction_reference(reference: str) -> str:
    """
    Validate transaction reference.
    
    Args:
        reference: Transaction reference to validate
        
    Returns:
        str: Validated reference
        
    Raises:
        ValidationError: If reference is invalid
    """
    reference = sanitize_string(reference, max_length=50)
    
    # Allow alphanumeric, hyphens, and underscores only
    if not re.match(r'^[a-zA-Z0-9_-]+$', reference):
        raise ValidationError("Transaction reference contains invalid characters")
    
    if len(reference) < 3:
        raise ValidationError("Transaction reference too short (minimum 3 characters)")
    
    return reference
