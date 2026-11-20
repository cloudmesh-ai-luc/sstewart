#!/usr/bin/env bash

# ---------------------------------------------------------------------------
# 911 Triage System – create a default configuration file.
#
# The application expects a ``.env``‑style file at ``$HOME/.config/911/env``.
# This script creates the directory (if necessary) and writes a template with
# placeholder values. The user should edit the generated file and replace the
# placeholders with real credentials before running the service.
# ---------------------------------------------------------------------------


#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="$HOME/.config/911"
CONFIG_FILE="$CONFIG_DIR/env"

echo "Creating configuration directory at $CONFIG_DIR..."
mkdir -p "$CONFIG_DIR"

if [[ -f "$CONFIG_FILE" ]]; then
    echo "Configuration already exists. Leaving it unchanged."
    exit 0
fi

cat > "$CONFIG_FILE" <<'EOF'
# 911 backend configuration

MARIADB_HOST=127.0.0.1
MARIADB_PORT=3306
MARIADB_DATABASE=911_analysis
MARIADB_USER=analysis_user
MARIADB_PASSWORD=replace_with_your_local_password

# Used by Docker Compose for database initialization
MARIADB_ROOT_PASSWORD=replace_with_a_different_root_password
EOF

chmod 600 "$CONFIG_FILE"

echo "Configuration file created at $CONFIG_FILE."
echo "Edit it and replace the placeholder passwords."
