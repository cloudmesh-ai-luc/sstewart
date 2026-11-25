
"""Password hashing and verification utilities."""

from pwdlib import PasswordHash


# Create one reusable password hashing instance.
password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Securely hash a plaintext password."""
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Verify a password against its stored hash."""
    return password_hasher.verify(
        plain_password,
        hashed_password,
    )
