"""
Encryption Service for Enhanced Report System.

This module provides comprehensive encryption functionality for FedRAMP and DoD compliance,
including data encryption at rest and in transit.
"""

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
from typing import Dict, Any, Optional, Union, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hmac import HMAC
import struct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EncryptionService:
    """
    Comprehensive encryption service for FedRAMP and DoD compliance.
    
    Features:
    - Symmetric encryption (AES-256)
    - Asymmetric encryption (RSA-4096)
    - Key derivation and management
    - Data integrity verification
    - Secure key storage
    - Compliance with FedRAMP and DoD standards
    """
    
    def __init__(self, key_file: str = "config/encryption_keys.json"):
        """
        Initialize the encryption service.
        
        Args:
            key_file: Path to the key storage file
        """
        self.key_file = key_file
        self.master_key = None
        self.rsa_private_key = None
        self.rsa_public_key = None
        self.key_derivation_salt = None
        
        # Initialize encryption keys
        self._initialize_keys()
        
    def _initialize_keys(self):
        """Initialize or load encryption keys."""
        try:
            if os.path.exists(self.key_file):
                self._load_keys()
            else:
                self._generate_keys()
                self._save_keys()
        except Exception as e:
            logger.error(f"Failed to initialize encryption keys: {e}")
            raise
    
    def _generate_keys(self):
        """Generate new encryption keys."""
        # Generate master key for symmetric encryption
        self.master_key = Fernet.generate_key()
        
        # Generate RSA key pair for asymmetric encryption
        self.rsa_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096
        )
        self.rsa_public_key = self.rsa_private_key.public_key()
        
        # Generate salt for key derivation
        self.key_derivation_salt = os.urandom(32)
        
        logger.info("Generated new encryption keys")
    
    def _save_keys(self):
        """Save encryption keys to file."""
        os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
        
        # Serialize RSA private key
        private_key_pem = self.rsa_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize RSA public key
        public_key_pem = self.rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        keys_data = {
            "master_key": base64.b64encode(self.master_key).decode('utf-8'),
            "private_key": private_key_pem.decode('utf-8'),
            "public_key": public_key_pem.decode('utf-8'),
            "key_derivation_salt": base64.b64encode(self.key_derivation_salt).decode('utf-8')
        }
        
        with open(self.key_file, 'w') as f:
            json.dump(keys_data, f, indent=2)
        
        logger.info(f"Saved encryption keys to {self.key_file}")
    
    def _load_keys(self):
        """Load encryption keys from file."""
        with open(self.key_file, 'r') as f:
            keys_data = json.load(f)
        
        # Load master key
        self.master_key = base64.b64decode(keys_data["master_key"])
        
        # Load RSA private key
        self.rsa_private_key = serialization.load_pem_private_key(
            keys_data["private_key"].encode('utf-8'),
            password=None
        )
        
        # Load RSA public key
        self.rsa_public_key = serialization.load_pem_public_key(
            keys_data["public_key"].encode('utf-8')
        )
        
        # Load key derivation salt
        self.key_derivation_salt = base64.b64decode(keys_data["key_derivation_salt"])
        
        logger.info(f"Loaded encryption keys from {self.key_file}")
    
    def encrypt_data(self, data: Union[str, bytes, Dict[str, Any]], 
                    encryption_type: str = "symmetric") -> Dict[str, Any]:
        """
        Encrypt data using specified encryption method.
        
        Args:
            data: Data to encrypt
            encryption_type: Type of encryption ("symmetric" or "asymmetric")
            
        Returns:
            Dictionary containing encrypted data and metadata
        """
        if encryption_type == "symmetric":
            return self._encrypt_symmetric(data)
        elif encryption_type == "asymmetric":
            return self._encrypt_asymmetric(data)
        else:
            raise ValueError(f"Unsupported encryption type: {encryption_type}")
    
    def _encrypt_symmetric(self, data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """Encrypt data using symmetric encryption (AES-256)."""
        # Convert data to bytes if needed
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        else:
            data_bytes = data
        
        # Generate a random IV
        iv = os.urandom(16)
        
        # Derive encryption key
        encryption_key = self._derive_key("encryption", iv)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # Pad data to block size
        padded_data = self._pad_data(data_bytes)
        
        # Encrypt data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Generate HMAC for integrity
        hmac_key = self._derive_key("hmac", iv)
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(iv)
        h.update(encrypted_data)
        hmac_value = h.finalize()
        
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "hmac": base64.b64encode(hmac_value).decode('utf-8'),
            "encryption_type": "symmetric",
            "algorithm": "AES-256-CBC",
            "key_derivation": "PBKDF2-HMAC-SHA256"
        }
    
    def _encrypt_asymmetric(self, data: Union[str, bytes, Dict[str, Any]]) -> Dict[str, Any]:
        """Encrypt data using asymmetric encryption (RSA-4096)."""
        # Convert data to bytes if needed
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        else:
            data_bytes = data
        
        # RSA encryption has size limitations, so we'll use hybrid encryption
        # Generate a random AES key for the data
        aes_key = os.urandom(32)
        iv = os.urandom(16)
        
        # Encrypt the data with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = self._pad_data(data_bytes)
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Encrypt the AES key with RSA
        encrypted_key = self.rsa_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Generate HMAC for integrity
        hmac_key = self._derive_key("hmac", iv)
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(iv)
        h.update(encrypted_data)
        hmac_value = h.finalize()
        
        return {
            "encrypted_data": base64.b64encode(encrypted_data).decode('utf-8'),
            "encrypted_key": base64.b64encode(encrypted_key).decode('utf-8'),
            "iv": base64.b64encode(iv).decode('utf-8'),
            "hmac": base64.b64encode(hmac_value).decode('utf-8'),
            "encryption_type": "asymmetric",
            "algorithm": "RSA-4096-OAEP + AES-256-CBC",
            "key_derivation": "PBKDF2-HMAC-SHA256"
        }
    
    def decrypt_data(self, encrypted_data: Dict[str, Any]) -> Union[str, bytes, Dict[str, Any]]:
        """
        Decrypt data using the appropriate method.
        
        Args:
            encrypted_data: Dictionary containing encrypted data and metadata
            
        Returns:
            Decrypted data
        """
        encryption_type = encrypted_data.get("encryption_type", "symmetric")
        
        if encryption_type == "symmetric":
            return self._decrypt_symmetric(encrypted_data)
        elif encryption_type == "asymmetric":
            return self._decrypt_asymmetric(encrypted_data)
        else:
            raise ValueError(f"Unsupported encryption type: {encryption_type}")
    
    def _decrypt_symmetric(self, encrypted_data: Dict[str, Any]) -> Union[str, bytes, Dict[str, Any]]:
        """Decrypt data using symmetric decryption."""
        # Extract components
        encrypted_bytes = base64.b64decode(encrypted_data["encrypted_data"])
        iv = base64.b64decode(encrypted_data["iv"])
        hmac_value = base64.b64decode(encrypted_data["hmac"])
        
        # Verify HMAC
        hmac_key = self._derive_key("hmac", iv)
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(iv)
        h.update(encrypted_bytes)
        h.verify(hmac_value)
        
        # Derive decryption key
        decryption_key = self._derive_key("encryption", iv)
        
        # Create cipher
        cipher = Cipher(algorithms.AES(decryption_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        
        # Decrypt data
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
        
        # Remove padding
        decrypted_data = self._unpad_data(decrypted_padded)
        
        # Try to decode as JSON first, then as string
        try:
            return json.loads(decrypted_data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return decrypted_data
    
    def _decrypt_asymmetric(self, encrypted_data: Dict[str, Any]) -> Union[str, bytes, Dict[str, Any]]:
        """Decrypt data using asymmetric decryption."""
        # Extract components
        encrypted_bytes = base64.b64decode(encrypted_data["encrypted_data"])
        encrypted_key = base64.b64decode(encrypted_data["encrypted_key"])
        iv = base64.b64decode(encrypted_data["iv"])
        hmac_value = base64.b64decode(encrypted_data["hmac"])
        
        # Verify HMAC
        hmac_key = self._derive_key("hmac", iv)
        h = HMAC(hmac_key, hashes.SHA256())
        h.update(iv)
        h.update(encrypted_bytes)
        h.verify(hmac_value)
        
        # Decrypt the AES key with RSA
        aes_key = self.rsa_private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt the data with AES
        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_bytes) + decryptor.finalize()
        
        # Remove padding
        decrypted_data = self._unpad_data(decrypted_padded)
        
        # Try to decode as JSON first, then as string
        try:
            return json.loads(decrypted_data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return decrypted_data
    
    def _derive_key(self, purpose: str, salt: bytes) -> bytes:
        """Derive a key for a specific purpose."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt + self.key_derivation_salt,
            iterations=100000,
        )
        return kdf.derive(self.master_key + purpose.encode('utf-8'))
    
    def _pad_data(self, data: bytes) -> bytes:
        """Pad data to AES block size."""
        block_size = 16
        padding_length = block_size - (len(data) % block_size)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    def _unpad_data(self, data: bytes) -> bytes:
        """Remove padding from data."""
        padding_length = data[-1]
        return data[:-padding_length]
    
    def encrypt_file(self, file_path: str, output_path: Optional[str] = None) -> str:
        """
        Encrypt a file using symmetric encryption.
        
        Args:
            file_path: Path to the file to encrypt
            output_path: Path for the encrypted file (optional)
            
        Returns:
            Path to the encrypted file
        """
        if output_path is None:
            output_path = file_path + ".encrypted"
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        encrypted_data = self._encrypt_symmetric(file_data)
        
        with open(output_path, 'w') as f:
            json.dump(encrypted_data, f, indent=2)
        
        logger.info(f"Encrypted file {file_path} to {output_path}")
        return output_path
    
    def decrypt_file(self, encrypted_file_path: str, output_path: Optional[str] = None) -> str:
        """
        Decrypt a file.
        
        Args:
            encrypted_file_path: Path to the encrypted file
            output_path: Path for the decrypted file (optional)
            
        Returns:
            Path to the decrypted file
        """
        if output_path is None:
            output_path = encrypted_file_path.replace(".encrypted", "")
        
        with open(encrypted_file_path, 'r') as f:
            encrypted_data = json.load(f)
        
        decrypted_data = self._decrypt_symmetric(encrypted_data)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        logger.info(f"Decrypted file {encrypted_file_path} to {output_path}")
        return output_path
    
    def hash_data(self, data: Union[str, bytes], algorithm: str = "sha256") -> str:
        """
        Generate a cryptographic hash of data.
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if algorithm == "sha256":
            return hashlib.sha256(data).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data).hexdigest()
        elif algorithm == "md5":
            return hashlib.md5(data).hexdigest()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    
    def verify_data_integrity(self, data: Union[str, bytes], expected_hash: str, 
                             algorithm: str = "sha256") -> bool:
        """
        Verify data integrity using cryptographic hash.
        
        Args:
            data: Data to verify
            expected_hash: Expected hash value
            algorithm: Hash algorithm used
            
        Returns:
            True if integrity is verified, False otherwise
        """
        actual_hash = self.hash_data(data, algorithm)
        return hmac.compare_digest(actual_hash, expected_hash)
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure token.
        
        Args:
            length: Length of the token in bytes
            
        Returns:
            Base64-encoded secure token
        """
        token = secrets.token_bytes(length)
        return base64.b64encode(token).decode('utf-8')
    
    def encrypt_sensitive_fields(self, data: Dict[str, Any], 
                               sensitive_fields: list) -> Dict[str, Any]:
        """
        Encrypt specific fields in a dictionary.
        
        Args:
            data: Dictionary containing data
            sensitive_fields: List of field names to encrypt
            
        Returns:
            Dictionary with sensitive fields encrypted
        """
        encrypted_data = data.copy()
        
        for field in sensitive_fields:
            if field in encrypted_data:
                encrypted_data[field] = self._encrypt_symmetric(encrypted_data[field])
        
        return encrypted_data
    
    def decrypt_sensitive_fields(self, data: Dict[str, Any], 
                               sensitive_fields: list) -> Dict[str, Any]:
        """
        Decrypt specific fields in a dictionary.
        
        Args:
            data: Dictionary containing encrypted data
            sensitive_fields: List of field names to decrypt
            
        Returns:
            Dictionary with sensitive fields decrypted
        """
        decrypted_data = data.copy()
        
        for field in sensitive_fields:
            if field in decrypted_data:
                decrypted_data[field] = self._decrypt_symmetric(decrypted_data[field])
        
        return decrypted_data
    
    def get_public_key_pem(self) -> str:
        """Get the public key in PEM format."""
        public_key_pem = self.rsa_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_key_pem.decode('utf-8')
    
    def rotate_keys(self):
        """Rotate encryption keys for security."""
        logger.info("Rotating encryption keys...")
        
        # Generate new keys
        old_master_key = self.master_key
        old_rsa_private_key = self.rsa_private_key
        old_rsa_public_key = self.rsa_public_key
        
        self._generate_keys()
        
        # Save new keys
        self._save_keys()
        
        logger.info("Encryption keys rotated successfully")
        
        return {
            "old_master_key": base64.b64encode(old_master_key).decode('utf-8'),
            "old_public_key": old_rsa_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode('utf-8')
        }


# Global encryption service instance
encryption_service = EncryptionService()
