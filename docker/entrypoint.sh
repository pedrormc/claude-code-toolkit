#!/bin/bash
set -e

# ── Initialize firewall if capabilities available ──
if sudo iptables -L -n &>/dev/null 2>&1; then
  echo "[sandbox] Initializing network firewall..."
  sudo /usr/local/bin/init-firewall.sh
  echo "[sandbox] Firewall active — only Anthropic API, npm, GitHub allowed"
else
  echo "[sandbox] WARNING: NET_ADMIN capability not available, firewall NOT active"
  echo "[sandbox] Add --cap-add=NET_ADMIN --cap-add=NET_RAW to docker run for full isolation"
fi

# ── Validate API key ──
if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  ERROR: ANTHROPIC_API_KEY not set"
  echo ""
  echo "  Run with: docker compose run --rm claude"
  echo "  And set ANTHROPIC_API_KEY in .env file"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""
  exit 1
fi

# ── Show sandbox status ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Claude Code Sandbox"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  User:       $(whoami)"
echo "  Workspace:  /workspace"
echo "  Config:     $CLAUDE_CONFIG_DIR"
echo "  API Key:    ${ANTHROPIC_API_KEY:0:12}...${ANTHROPIC_API_KEY: -4}"
echo "  Node:       $(node --version)"
echo "  Claude:     $(claude --version 2>/dev/null || echo 'checking...')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Execute command ──
exec "$@"
