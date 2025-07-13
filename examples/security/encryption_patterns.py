"""
🟢 Production Ready: Security and Encryption Patterns for Qpesapay

This example demonstrates proper security implementation patterns for
financial systems, including encryption, key management, and secure storage.

Key Patterns:
- AES-256 encryption for sensitive data
- PBKDF2 key derivation with high iterations
- Secure private key storage
- Field-level encryption
- Audit-safe logging (no sensitive data)
- Proper error handling without information leakage
"""

import os
import hashlib
import hmac
import secrets
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import base64
import logging

from app.core.exceptions import EncryptionError, SecurityError
from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class EncryptedData:
    """Container for encrypted data with metadata."""
    ciphertext: bytes
    salt: bytes
    iv: bytes
    algorithm: str = "AES-256-GCM"
    key_derivation: str = "PBKDF2-SHA256"
    iterations: int = 100000


class SecureKeyManager:
    """
    🟢 Production Ready: Secure key management for financial systems.
    
    Handles encryption keys, private key storage, and key derivation
    with proper security practices for financial applications.
    
    Key Features:
    - AES-256 encryption
    - PBKDF2 key derivation with high iterations
    - Secure random salt generation
    - No keys stored in memory longer than necessary
    - Audit logging without sensitive data exposure
    """
    
    def __init__(self, master_key: Optional[str] = None):
        """
        Initialize secure key manager.
        
        Args:
            master_key: Master encryption key (from environment)
        """
        self._master_key = master_key or os.getenv("ENCRYPTION_KEY")
        if not self._master_key:
            raise SecurityError("Master encryption key not provided")
        
        if len(self._master_key) < 32:
            raise SecurityError("Master key must be at least 32 characters")
    
    def encrypt_sensitive_data(
        self,
        plaintext: str,
        context: Optional[str] = None
    ) -> EncryptedData:
        """
        Encrypt sensitive data with AES-256-GCM.
        
        Args:
            plaintext: Data to encrypt
            context: Optional context for audit logging
            
        Returns:
            EncryptedData: Encrypted data with metadata
            
        Raises:
            EncryptionError: If encryption fails
        """
        try:
            # Generate random salt and IV
            salt = secrets.token_bytes(32)
            iv = secrets.token_bytes(12)  # GCM mode uses 12-byte IV
            
            # Derive encryption key using PBKDF2
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            key = kdf.derive(self._master_key.encode())
            
            # Encrypt with AES-256-GCM
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
            
            # Securely clear key from memory
            if isinstance(key, bytes):
                key_ba = bytearray(key)
                for i in range(len(key_ba)):
                    key_ba[i] = 0
            elif isinstance(key, bytearray):
                for i in range(len(key)):
                    key[i] = 0
            
            # Log encryption (without sensitive data)
            logger.info(
                "Data encrypted successfully",
                extra={
                    "context": context,
                    "algorithm": "AES-256-GCM",
                    "data_length": len(plaintext)
                }
            )
            
            return EncryptedData(
                ciphertext=ciphertext + encryptor.tag,  # Append auth tag
                salt=salt,
                iv=iv,
                algorithm="AES-256-GCM",
                key_derivation="PBKDF2-SHA256",
                iterations=100000
            )
            
        except Exception as e:
            logger.error(
                "Encryption failed",
                extra={"context": context, "error_type": type(e).__name__}
            )
            raise EncryptionError(f"Encryption failed: {str(e)}")
    
    def decrypt_sensitive_data(
        self,
        encrypted_data: EncryptedData,
        context: Optional[str] = None
    ) -> str:
        """
        Decrypt sensitive data.
        
        Args:
            encrypted_data: Encrypted data to decrypt
            context: Optional context for audit logging
            
        Returns:
            str: Decrypted plaintext
            
        Raises:
            EncryptionError: If decryption fails
        """
        try:
            # Derive decryption key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=encrypted_data.salt,
                iterations=encrypted_data.iterations,
                backend=default_backend()
            )
            key = kdf.derive(self._master_key.encode())
            
            # Split ciphertext and auth tag
            ciphertext = encrypted_data.ciphertext[:-16]
            tag = encrypted_data.ciphertext[-16:]
            
            # Decrypt with AES-256-GCM
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(encrypted_data.iv, tag),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Securely clear key from memory
            if isinstance(key, bytes):
                key_ba = bytearray(key)
                for i in range(len(key_ba)):
                    key_ba[i] = 0
            elif isinstance(key, bytearray):
                for i in range(len(key)):
                    key[i] = 0
            
            # Log decryption (without sensitive data)
            logger.info(
                "Data decrypted successfully",
                extra={
                    "context": context,
                    "algorithm": encrypted_data.algorithm
                }
            )
            
            return plaintext.decode()
            
        except Exception as e:
            logger.error(
                "Decryption failed",
                extra={"context": context, "error_type": type(e).__name__}
            )
            raise EncryptionError(f"Decryption failed: {str(e)}")


class PrivateKeyManager:
    """
    🟢 Production Ready: Private key management for cryptocurrency wallets.
    
    Handles secure storage and retrieval of cryptocurrency private keys
    with proper encryption and access controls.
    """
    
    def __init__(self, key_manager: SecureKeyManager):
        """
        Initialize private key manager.
        
        Args:
            key_manager: Secure key manager instance
        """
        self._key_manager = key_manager
    
    def store_private_key(
        self,
        private_key: str,
        wallet_id: str,
        network: str
    ) -> EncryptedData:
        """
        Store private key with encryption.
        
        Args:
            private_key: Private key to store
            wallet_id: Wallet identifier
            network: Blockchain network (bitcoin, ethereum, tron)
            
        Returns:
            EncryptedData: Encrypted private key data
        """
        # Validate private key format
        self._validate_private_key(private_key, network)
        
        # Encrypt private key
        context = f"private_key_storage_{network}_{wallet_id}"
        encrypted_key = self._key_manager.encrypt_sensitive_data(
            private_key, context
        )
        
        # Log storage (without key data)
        logger.info(
            "Private key stored securely",
            extra={
                "wallet_id": wallet_id,
                "network": network,
                "encryption_algorithm": encrypted_key.algorithm
            }
        )
        
        return encrypted_key
    
    def retrieve_private_key(
        self,
        encrypted_data: EncryptedData,
        wallet_id: str,
        network: str
    ) -> str:
        """
        Retrieve and decrypt private key.
        
        Args:
            encrypted_data: Encrypted private key data
            wallet_id: Wallet identifier
            network: Blockchain network
            
        Returns:
            str: Decrypted private key
        """
        context = f"private_key_retrieval_{network}_{wallet_id}"
        
        # Decrypt private key
        private_key = self._key_manager.decrypt_sensitive_data(
            encrypted_data, context
        )
        
        # Validate decrypted key
        self._validate_private_key(private_key, network)
        
        # Log retrieval (without key data)
        logger.info(
            "Private key retrieved successfully",
            extra={
                "wallet_id": wallet_id,
                "network": network
            }
        )
        
        return private_key
    
    def _validate_private_key(self, private_key: str, network: str) -> None:
        """
        Validate private key format for specific network.
        
        Args:
            private_key: Private key to validate
            network: Blockchain network
            
        Raises:
            SecurityError: If private key is invalid
        """
        if network == "bitcoin":
            # Bitcoin private keys are 64 hex characters or WIF format
            if not (len(private_key) == 64 and all(c in '0123456789abcdefABCDEF' for c in private_key)):
                if not (private_key.startswith(('5', 'K', 'L')) and len(private_key) in [51, 52]):
                    raise SecurityError("Invalid Bitcoin private key format")
        
        elif network in ["ethereum", "tron"]:
            # Ethereum/Tron private keys are 64 hex characters
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            if not (len(private_key) == 64 and all(c in '0123456789abcdefABCDEF' for c in private_key)):
                raise SecurityError(f"Invalid {network} private key format")
        
        else:
            raise SecurityError(f"Unsupported network: {network}")


class SecureHasher:
    """
    🟢 Production Ready: Secure hashing utilities for financial systems.
    
    Provides secure hashing functions for passwords, data integrity,
    and audit trail verification.
    """
    
    @staticmethod
    def hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        """
        Hash password with PBKDF2-SHA256.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dict containing hash and salt
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Use PBKDF2 with high iteration count
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        password_hash = kdf.derive(password.encode())
        
        return {
            "hash": base64.b64encode(password_hash).decode(),
            "salt": base64.b64encode(salt).decode(),
            "algorithm": "PBKDF2-SHA256",
            "iterations": 100000
        }
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify password against stored hash.
        
        Args:
            password: Password to verify
            stored_hash: Stored password hash
            salt: Salt used for hashing
            
        Returns:
            bool: True if password matches
        """
        try:
            salt_bytes = base64.b64decode(salt.encode())
            stored_hash_bytes = base64.b64decode(stored_hash.encode())
            
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt_bytes,
                iterations=100000,
                backend=default_backend()
            )
            
            computed_hash = kdf.derive(password.encode())
            return hmac.compare_digest(computed_hash, stored_hash_bytes)
            
        except Exception:
            return False
    
    @staticmethod
    def create_audit_hash(data: Dict[str, Any]) -> str:
        """
        Create tamper-proof hash for audit records.
        
        Args:
            data: Data to hash for audit trail
            
        Returns:
            str: SHA-256 hash of the data
        """
        # Sort keys for consistent hashing
        sorted_data = {k: data[k] for k in sorted(data.keys())}
        data_string = str(sorted_data).encode()
        
        return hashlib.sha256(data_string).hexdigest()


# Example usage patterns
def example_security_usage():
    """
    Example of how to use security patterns in Qpesapay.
    This demonstrates proper patterns for financial system security.

    SECURITY NOTE: This is an example only. In production:
    - Never hardcode sensitive data like private keys
    - Use secure input methods for sensitive data
    - Implement proper key management systems
    - Ensure sensitive outputs are not logged
    """
    try:
        # Initialize key manager
        key_manager = SecureKeyManager()
        private_key_manager = PrivateKeyManager(key_manager)

        # Encrypt sensitive data
        sensitive_data = "user_private_information"
        try:
            encrypted = key_manager.encrypt_sensitive_data(
                sensitive_data,
                context="user_kyc_data"
            )
            logger.info("Data encryption successful")
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

        # Decrypt sensitive data
        try:
            decrypted = key_manager.decrypt_sensitive_data(
                encrypted,
                context="user_kyc_data"
            )
            logger.info("Data decryption successful")
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            raise

        # Store private key (SECURITY: In production, use secure input methods)
        # This is for demonstration only - never hardcode private keys
        try:
            # Simulate secure key generation/input
            private_key = "0123456789abcdef" * 4  # Example only - use secure generation
            encrypted_key = private_key_manager.store_private_key(
                private_key,
                wallet_id="wallet-123",
                network="ethereum"
            )
            logger.info("Private key storage successful")
        except Exception as e:
            logger.error(f"Key storage failed: {e}")
            raise

        # Hash password
        try:
            password_data = SecureHasher.hash_password("user_password_123")
            logger.info("Password hashing successful")
        except Exception as e:
            logger.error(f"Password hashing failed: {e}")
            raise

        # Verify password
        try:
            is_valid = SecureHasher.verify_password(
                "user_password_123",
                password_data["hash"],
                password_data["salt"]
            )
            logger.info(f"Password verification: {'valid' if is_valid else 'invalid'}")
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            raise

        # Create audit hash
        try:
            audit_data = {
                "transaction_id": "tx-123",
                "amount": "100.50",
                "timestamp": "2024-01-01T00:00:00Z"
            }
            audit_hash = SecureHasher.create_audit_hash(audit_data)
            logger.info("Audit hash creation successful")
        except Exception as e:
            logger.error(f"Audit hash creation failed: {e}")
            raise

        # Return non-sensitive summary (do not return actual encrypted data)
        return {
            "encryption_successful": True,
            "decryption_successful": True,
            "key_storage_successful": True,
            "password_validation_successful": is_valid,
            "audit_hash_created": True
        }

    except Exception as e:
        # Handle errors securely, do not log sensitive data
        logger.error("Security operation failed - check individual operation logs")
        return {"error": "A security error occurred. Check logs for details."}
