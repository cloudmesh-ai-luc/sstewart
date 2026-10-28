"""Configuration loader for the 911 analysis backend.

The application expects a ``.env``‑style file located at
``~/.config/911/env``.  The file shipped with the template contains placeholder
values for the MariaDB passwords:

```
MARIADB_PASSWORD=replace_with_a_local_password
MARIADB_ROOT_PASSWORD=replace_with_a_different_root_password
```

If those placeholders are left in the file the program should abort with a
clear error message – this module performs that validation.

The implementation purposefully avoids an external dependency such as
``python‑dotenv``; it parses the file manually, which is sufficient for the
simple ``KEY=VALUE`` format used in the project.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Mapping


class ConfigError(RuntimeError):
    """Custom exception raised when the configuration is invalid."""


class Config:
    """Load and validate environment configuration.

    Parameters
    ----------
    env_path:
        Optional path to the environment file.  If omitted the default location
        ``~/.config/911/env`` is used.  Supplying a path is handy for tests.
    """

    # Placeholder values that indicate the user has not replaced them.
    _PASSWORD_PLACEHOLDERS = {
        "MARIADB_PASSWORD": "replace_with_a_local_password",
        "MARIADB_ROOT_PASSWORD": "replace_with_a_different_root_password",
    }

    def __init__(self, env_path: str | os.PathLike | None = None):
        # Resolve the configuration file location.
        default_path = Path.home() / ".config" / "911" / "env"
        self._path: Path = Path(env_path) if env_path is not None else default_path

        if not self._path.is_file():
            raise ConfigError(f"Configuration file not found: {self._path}")

        # Parse the file into a dict.
        self._values: Dict[str, str] = self._parse_env_file(self._path)

        # Validate required password fields.
        self._validate_passwords()

        # Expose commonly used variables as attributes for convenience.
        self.mariadb_database: str = self._values.get("MARIADB_DATABASE", "")
        self.mariadb_user: str = self._values.get("MARIADB_USER", "")
        self.mariadb_password: str = self._values["MARIADB_PASSWORD"]
        self.mariadb_root_password: str = self._values["MARIADB_ROOT_PASSWORD"]
        self.mariadb_port: str = self._values.get("MARIADB_PORT", "3306")

    @staticmethod
    def _parse_env_file(path: Path) -> Dict[str, str]:
        """Read a ``.env``‑style file into a ``dict``.

        Empty lines and lines starting with ``#`` are ignored.  The first ``=``
        character splits the key from the value.  Whitespace around the key and
        value is stripped.
        """
        values: Dict[str, str] = {}
        with path.open("r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    # Skip malformed lines but keep processing the rest.
                    continue
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
        return values

    def _validate_passwords(self) -> None:
        """Ensure password placeholders have been replaced.

        Raises
        ------
        ConfigError
            If either ``MARIADB_PASSWORD`` or ``MARIADB_ROOT_PASSWORD`` is still
            set to its placeholder value.
        """
        for var, placeholder in self._PASSWORD_PLACEHOLDERS.items():
            actual = self._values.get(var)
            if actual is None:
                raise ConfigError(f"Missing required configuration variable: {var}")
            if actual == placeholder:
                raise ConfigError(
                    f"{var} has not been set. Replace the placeholder in "
                    f"{self._path} with a real password."
                )

    # ---------------------------------------------------------------------
    # Helper API
    # ---------------------------------------------------------------------
    def as_dict(self) -> Mapping[str, str]:
        """Return the full configuration mapping.

        The returned mapping is read‑only; it is safe to expose to callers that
        only need to query values.
        """
        return dict(self._values)


def load_config(env_path: str | os.PathLike | None = None) -> Config:
    """Convenient function to obtain a :class:`Config` instance.

    This wrapper mirrors the common pattern ``config = load_config()`` used in
    other parts of the codebase, keeping the import surface tidy.
    """
    return Config(env_path=env_path)
