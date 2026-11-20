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