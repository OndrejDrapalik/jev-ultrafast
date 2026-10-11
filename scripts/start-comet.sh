#!/usr/bin/env bash
# Connect through od-ab-e2b, then load .env before Python imports Browser Harness.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f .env ]; then
  (umask 077; cp .env.example .env)
  echo "Created .env. Add TYPESAFE_API_KEY and TEXT_MODEL_API_KEY for model actions."
fi

CONNECT_SCRIPT="${COMET_CONNECT_SCRIPT:-$HOME/.agents/skills/od-ab-e2b/scripts/connect-e2b.sh}"
if [ ! -x "$CONNECT_SCRIPT" ]; then
  echo "Missing od-ab-e2b connector: $CONNECT_SCRIPT" >&2
  exit 1
fi

# Exit 2 from the skill means Comet needs a user-approved relaunch. Do not restart it here.
PORT=9333 "$CONNECT_SCRIPT" about:blank
export BU_CDP_URL=http://127.0.0.1:9333 BU_NAME=jev-comet BH_TAB_MARKER=0
unset BU_CDP_WS BU_BROWSER_ID
exec uv run --env-file .env jev
