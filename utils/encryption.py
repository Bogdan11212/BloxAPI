"""
Encryption Utilities for BloxAPI

This module provides end-to-end encryption capabilities for sensitive data
handled by the BloxAPI. It uses industry-standard cryptographic algorithms
to ensure data security and privacy.
"""

import os
import base64
import json
import logging
import hashlib
import secrets
from typing import Dict, Any, Optional, Union, Tuple, List
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key, load_pem_public_key,
    Encoding, PrivateFormat, PublicFormat, NoEncryption
)
from cryptography.fernet import Fernet

# Configure logging
logger = logging.getLogger(__name__)

class EncryptionManager:
    """
    Manager for encryption and decryption operations in BloxAPI.
    
    This class provides methods for symmetric and asymmetric encryption,
    digital signatures, and secure key management.
    """
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize the encryption manager.
        
        Args:
            secret_key: Secret key for encryption operations. If not provided,
                        it will use the SECRET_KEY environment variable.
        """
        # Get encryption key from provided secret or environment variable
        self.secret_key = secret_key or os.environ.get('SECRET_KEY', None)
        
        if not self.secret_key:
            logger.warning("No secret key provided. Using a randomly generated key.")
            self.secret_key = secrets.token_hex(32)
        
        # Derive a key for symmetric encryption
        self.symmetric_key = self._derive_key(self.secret_key.encode(), b'symmetric')
        
        # Generate or load asymmetric keys
        self.private_key, self.public_key = self._init_asymmetric_keys()
    
    def _derive_key(self, key_material: bytes, salt: bytes, length: int = 32) -> bytes:
        """
        Derive a cryptographic key using PBKDF2.
        
        Args:
            key_material: Base key material
            salt: Salt value for key derivation
            length: Length of the derived key in bytes
            
        Returns:
            Derived cryptographic key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=length,
            salt=salt,
            iterations=100000,
        )
        return kdf.derive(key_material)
    
    def _init_asymmetric_keys(self) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """
        Initialize RSA private and public keys.
        
        If keys are available in the environment, load them.
        Otherwise, generate new keys.
        
        Returns:
            Tuple of (private_key, public_key)
        """
        private_key_pem = os.environ.get('RSA_PRIVATE_KEY')
        public_key_pem = os.environ.get('RSA_PUBLIC_KEY')
        
        if private_key_pem and public_key_pem:
            try:
                private_key = load_pem_private_key(
                    private_key_pem.encode(),
                    password=None
                )
                public_key = load_pem_public_key(public_key_pem.encode())
                
                return private_key, public_key
            except Exception as e:
                logger.error(f"Error loading RSA keys: {e}")
        
        # Generate new keys
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()
        
        return private_key, public_key
    
    def encrypt_symmetric(self, data: Union[str, bytes, Dict[str, Any]],
                         associated_data: Optional[bytes] = None) -> str:
        """
        Encrypt data using symmetric encryption (AES-GCM).
        
        Args:
            data: Data to encrypt (string, bytes, or JSON-serializable object)
            associated_data: Additional authenticated data
            
        Returns:
            Base64-encoded encrypted data
        """
        try:
            # Convert data to bytes if needed
            if isinstance(data, dict):
                plaintext = json.dumps(data).encode()
            elif isinstance(data, str):
                plaintext = data.encode()
            else:
                plaintext = data
            
            # Generate a random 96-bit IV/nonce
            iv = os.urandom(12)
            
            # Create an AES-GCM cipher instance
            aesgcm = AESGCM(self.symmetric_key)
            
            # Encrypt the data
            associated_data = associated_data or b''
            ciphertext = aesgcm.encrypt(iv, plaintext, associated_data)
            
            # Combine IV and ciphertext and encode as base64
            encrypted = base64.b64encode(iv + ciphertext).decode()
            
            return encrypted
        
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            raise
    
    def decrypt_symmetric(self, encrypted_data: str,
                         associated_data: Optional[bytes] = None) -> bytes:
        """
        Decrypt data using symmetric encryption (AES-GCM).
        
        Args:
            encrypted_data: Base64-encoded encrypted data
            associated_data: Additional authenticated data
            
        Returns:
            Decrypted data as bytes
        """
        try:
            # Decode base64
            data = base64.b64decode(encrypted_data)
            
            # Extract IV (first 12 bytes) and ciphertext
            iv = data[:12]
            ciphertext = data[12:]
            
            # Create an AES-GCM cipher instance
            aesgcm = AESGCM(self.symmetric_key)
            
            # Decrypt the data
            associated_data = associated_data or b''
            plaintext = aesgcm.decrypt(iv, ciphertext, associated_data)
            
            return plaintext
        
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            raise
    
    def encrypt_asymmetric(self, data: Union[str, bytes, Dict[str, Any]],
                          public_key: Optional[rsa.RSAPublicKey] = None) -> str:
        """
        Encrypt data using asymmetric encryption (RSA).
        
        This uses a hybrid approach: data is encrypted with a random AES key,
        and the AES key is encrypted with RSA.
        
        Args:
            data: Data to encrypt
            public_key: RSA public key to use (uses instance's public key if not provided)
            
        Returns:
            Base64-encoded encrypted data
        """
        try:
            # Convert data to bytes if needed
            if isinstance(data, dict):
                plaintext = json.dumps(data).encode()
            elif isinstance(data, str):
                plaintext = data.encode()
            else:
                plaintext = data
            
            # Use provided public key or default
            public_key = public_key or self.public_key
            
            # Generate a random AES key
            aes_key = Fernet.generate_key()
            fernet = Fernet(aes_key)
            
            # Encrypt the data with AES
            encrypted_data = fernet.encrypt(plaintext)
            
            # Encrypt the AES key with RSA
            encrypted_key = public_key.encrypt(
                aes_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Combine encrypted key and data
            result = {
                "key": base64.b64encode(encrypted_key).decode(),
                "data": base64.b64encode(encrypted_data).decode()
            }
            
            return json.dumps(result)
        
        except Exception as e:
            logger.error(f"Asymmetric encryption error: {e}")
            raise
    
    def decrypt_asymmetric(self, encrypted_data: str,
                          private_key: Optional[rsa.RSAPrivateKey] = None) -> bytes:
        """
        Decrypt data using asymmetric encryption (RSA).
        
        Args:
            encrypted_data: Base64-encoded encrypted data
            private_key: RSA private key to use (uses instance's private key if not provided)
            
        Returns:
            Decrypted data as bytes
        """
        try:
            # Parse the JSON structure
            data = json.loads(encrypted_data)
            encrypted_key = base64.b64decode(data["key"])
            encrypted_data = base64.b64decode(data["data"])
            
            # Use provided private key or default
            private_key = private_key or self.private_key
            
            # Decrypt the AES key
            aes_key = private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Decrypt the data
            fernet = Fernet(aes_key)
            plaintext = fernet.decrypt(encrypted_data)
            
            return plaintext
        
        except Exception as e:
            logger.error(f"Asymmetric decryption error: {e}")
            raise
    
    def sign_data(self, data: Union[str, bytes, Dict[str, Any]],
                 private_key: Optional[rsa.RSAPrivateKey] = None) -> str:
        """
        Create a digital signature for data.
        
        Args:
            data: Data to sign
            private_key: RSA private key to use (uses instance's private key if not provided)
            
        Returns:
            Base64-encoded signature
        """
        try:
            # Convert data to bytes if needed
            if isinstance(data, dict):
                data_bytes = json.dumps(data).encode()
            elif isinstance(data, str):
                data_bytes = data.encode()
            else:
                data_bytes = data
            
            # Use provided private key or default
            private_key = private_key or self.private_key
            
            # Sign the data
            signature = private_key.sign(
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return base64.b64encode(signature).decode()
        
        except Exception as e:
            logger.error(f"Signature error: {e}")
            raise
    
    def verify_signature(self, data: Union[str, bytes, Dict[str, Any]], 
                        signature: str,
                        public_key: Optional[rsa.RSAPublicKey] = None) -> bool:
        """
        Verify a digital signature.
        
        Args:
            data: Data to verify
            signature: Base64-encoded signature
            public_key: RSA public key to use (uses instance's public key if not provided)
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Convert data to bytes if needed
            if isinstance(data, dict):
                data_bytes = json.dumps(data).encode()
            elif isinstance(data, str):
                data_bytes = data.encode()
            else:
                data_bytes = data
            
            # Decode signature
            signature_bytes = base64.b64decode(signature)
            
            # Use provided public key or default
            public_key = public_key or self.public_key
            
            # Verify the signature
            public_key.verify(
                signature_bytes,
                data_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            # If no exception was raised, signature is valid
            return True
        
        except Exception as e:
            logger.error(f"Signature verification error: {e}")
            return False
    
    def generate_key_pair(self) -> Dict[str, str]:
        """
        Generate a new RSA key pair.
        
        Returns:
            Dictionary with 'private_key' and 'public_key' as PEM-encoded strings
        """
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            
            # Extract public key
            public_key = private_key.public_key()
            
            # Serialize keys to PEM format
            private_pem = private_key.private_bytes(
                encoding=Encoding.PEM,
                format=PrivateFormat.PKCS8,
                encryption_algorithm=NoEncryption()
            ).decode()
            
            public_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            ).decode()
            
            return {
                "private_key": private_pem,
                "public_key": public_pem
            }
        
        except Exception as e:
            logger.error(f"Key generation error: {e}")
            raise
    
    def hash_password(self, password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
        """
        Hash a password securely using PBKDF2.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dictionary with 'hash' and 'salt' as base64-encoded strings
        """
        try:
            # Generate salt if not provided
            salt = salt or os.urandom(16)
            
            # Hash password
            password_hash = self._derive_key(password.encode(), salt)
            
            return {
                "hash": base64.b64encode(password_hash).decode(),
                "salt": base64.b64encode(salt).decode()
            }
        
        except Exception as e:
            logger.error(f"Password hashing error: {e}")
            raise
    
    def verify_password(self, password: str, password_hash: str, salt: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Password to verify
            password_hash: Base64-encoded password hash
            salt: Base64-encoded salt
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            # Decode hash and salt
            hash_bytes = base64.b64decode(password_hash)
            salt_bytes = base64.b64decode(salt)
            
            # Hash the provided password
            derived_key = self._derive_key(password.encode(), salt_bytes)
            
            # Compare in constant time
            return hmac.compare_digest(derived_key, hash_bytes)
        
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False
    
    def export_public_key(self) -> str:
        """
        Export the public key as a PEM-encoded string.
        
        Returns:
            PEM-encoded public key
        """
        return self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        ).decode()


# Global encryption manager
_encryption_manager = None

def get_encryption_manager() -> EncryptionManager:
    """
    Get the global encryption manager instance.
    
    Returns:
        EncryptionManager instance
    """
    global _encryption_manager
    if _encryption_manager is None:
        _encryption_manager = EncryptionManager()
    
    return _encryption_manager


# Utility functions for easy use

def encrypt(data: Union[str, bytes, Dict[str, Any]]) -> str:
    """
    Encrypt data using the global encryption manager.
    
    Args:
        data: Data to encrypt
        
    Returns:
        Encrypted data
    """
    return get_encryption_manager().encrypt_symmetric(data)

def decrypt(encrypted_data: str) -> bytes:
    """
    Decrypt data using the global encryption manager.
    
    Args:
        encrypted_data: Encrypted data
        
    Returns:
        Decrypted data
    """
    return get_encryption_manager().decrypt_symmetric(encrypted_data)

def sign(data: Union[str, bytes, Dict[str, Any]]) -> str:
    """
    Sign data using the global encryption manager.
    
    Args:
        data: Data to sign
        
    Returns:
        Digital signature
    """
    return get_encryption_manager().sign_data(data)

def verify(data: Union[str, bytes, Dict[str, Any]], signature: str) -> bool:
    """
    Verify a signature using the global encryption manager.
    
    Args:
        data: Data to verify
        signature: Digital signature
        
    Returns:
        True if signature is valid
    """
    return get_encryption_manager().verify_signature(data, signature)