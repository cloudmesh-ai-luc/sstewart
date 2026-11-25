
import os
from pathlib import Path

from dotenv import load_dotenv

CONFIG_FILE = Path.home() / ".config" / "911" / "env"

if not CONFIG_FILE.is_file():
    raise FileNotFoundError(
        f"Configuration file not found: {CONFIG_FILE}"
    )

load_dotenv(CONFIG_FILE)


def get_database_config() -> dict:
    required = [
        "MARIADB_HOST",
        "MARIADB_DATABASE",
        "MARIADB_USER",
        "MARIADB_PASSWORD",
    ]

    missing = [key for key in required if not os.getenv(key)]

    if missing:
        raise ValueError(
            f"Missing required database settings: {', '.join(missing)}"
        )

    return {
        "host": os.getenv("MARIADB_HOST"),
        "port": int(os.getenv("MARIADB_PORT", "3306")),
        "database": os.getenv("MARIADB_DATABASE"),
        "user": os.getenv("MARIADB_USER"),
        "password": os.getenv("MARIADB_PASSWORD"),
    }


def get_auth_config() -> dict:
    """Load and validate authentication settings."""

    secret_key = os.getenv("JWT_SECRET_KEY")

    if not secret_key:
        raise ValueError("Missing required setting: JWT_SECRET_KEY")

    if len(secret_key) < 32:
        raise ValueError(
            "JWT_SECRET_KEY must contain at least 32 characters"
        )

    expiration = os.getenv(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
        "30",
    )

    try:
        expiration_minutes = int(expiration)
    except ValueError:
        raise ValueError(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be an integer"
        )

    if expiration_minutes <= 0:
        raise ValueError(
            "JWT_ACCESS_TOKEN_EXPIRE_MINUTES must be positive"
        )

    return {
        "secret_key": secret_key,
        "algorithm": "HS256",
        "access_token_expire_minutes": expiration_minutes,
    }

def get_ollama_config() -> dict:
    """Return validated Ollama configuration."""

    base_url = os.getenv(
        "OLLAMA_BASE_URL",
        "http://localhost:11434",
    ).rstrip("/")

    model = os.getenv(
        "OLLAMA_MODEL",
        "llama3.2:1b",
    )

    timeout = os.getenv(
        "OLLAMA_TIMEOUT_SECONDS",
        "120",
    )

    if not base_url.startswith(("http://", "https://")):
        raise ValueError(
            "OLLAMA_BASE_URL must start with http:// or https://"
        )

    if not model.strip():
        raise ValueError("OLLAMA_MODEL cannot be empty")

    try:
        timeout_seconds = int(timeout)
    except ValueError:
        raise ValueError(
            "OLLAMA_TIMEOUT_SECONDS must be an integer"
        )

    if timeout_seconds <= 0:
        raise ValueError(
            "OLLAMA_TIMEOUT_SECONDS must be positive"
        )

    return {
        "base_url": base_url,
        "model": model,
        "timeout": timeout_seconds,
    }
