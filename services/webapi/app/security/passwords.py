"""Guacamole-compatible password hashing service.

Guacamole (auth-jdbc) stores passwords as SHA-256(password + hex(salt)) with a
random 32-byte salt. Both hash and salt are stored as raw bytes (bytea).
"""

from __future__ import annotations

import binascii
import hashlib
import os


class GuacPasswordService:
    """Implements Guacamole-compatible password hashing and verification."""

    def __init__(self, salt_len: int = 32) -> None:
        self.salt_len = salt_len

    def generate_salt(self) -> bytes:
        return os.urandom(self.salt_len)

    def _hash_with_salt(self, password: str, salt: bytes) -> bytes:
        # Concatenate plaintext password with hex-encoded salt (uppercase),
        # matching Postgres encode(salt, 'hex') used by Guacamole SQL
        salt_hex = binascii.hexlify(salt).decode("ascii").upper()
        digest = hashlib.sha256()
        digest.update((password + salt_hex).encode("utf-8"))
        return digest.digest()

    def hash_password(self, password: str) -> tuple[bytes, bytes]:
        """Return (salt, hash) for the given password."""
        salt = self.generate_salt()
        pwd_hash = self._hash_with_salt(password, salt)
        return salt, pwd_hash

    def verify(self, password: str, salt: bytes, password_hash: bytes) -> bool:
        return self._hash_with_salt(password, salt) == password_hash
