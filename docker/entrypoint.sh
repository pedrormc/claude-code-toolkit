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

# ── Detect auth method ──
AUTH_METHOD="none"
if [ -n "$ANTHROPIC_API_KEY" ]; then
  AUTH_METHOD="api-key"
elif [ -f "$CLAUDE_CONFIG_DIR/.credentials.json" ]; then
  AUTH_METHOD="oauth (saved)"
else
  AUTH_METHOD="oauth (login needed)"
fi

# ── Show sandbox status ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Claude Code Sandbox"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  User:       $(whoami)"
echo "  Workspace:  /workspace"
echo "  Config:     $CLAUDE_CONFIG_DIR"
echo "  Auth:       $AUTH_METHOD"
echo "  Node:       $(node --version)"
echo "  Claude:     $(claude --version 2>/dev/null || echo 'checking...')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$AUTH_METHOD" = "oauth (login needed)" ]; then
  echo ""
  echo "  Para autenticar com Claude Max/Pro/Team, rode:"
  echo "    claude login"
  echo ""
  echo "  Ou defina ANTHROPIC_API_KEY no .env para usar API key."
fi
echo ""

# ── Execute command ──
exec "$@"
