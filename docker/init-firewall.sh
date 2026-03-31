#!/bin/bash
# Network firewall for Claude Code sandbox
# Based on Anthropic's official devcontainer firewall
# Only allows outbound to: Anthropic API, npm, GitHub, DNS

set -e

# ── Resolve IPs ──
resolve_ips() {
  local domain="$1"
  dig +short "$domain" A 2>/dev/null | grep -E '^[0-9]+\.' || true
}

# ── Create ipset for allowed destinations ──
ipset create allowed_hosts hash:ip -exist
ipset flush allowed_hosts

# Anthropic API
for ip in $(resolve_ips "api.anthropic.com"); do
  ipset add allowed_hosts "$ip" -exist
done

# Anthropic stats
for ip in $(resolve_ips "statsig.anthropic.com"); do
  ipset add allowed_hosts "$ip" -exist
done

# Sentry (error reporting)
for ip in $(resolve_ips "sentry.io"); do
  ipset add allowed_hosts "$ip" -exist
done

# npm registry
for ip in $(resolve_ips "registry.npmjs.org"); do
  ipset add allowed_hosts "$ip" -exist
done

# GitHub
for domain in github.com api.github.com raw.githubusercontent.com; do
  for ip in $(resolve_ips "$domain"); do
    ipset add allowed_hosts "$ip" -exist
  done
done

# GitHub IP ranges (CIDR)
if command -v curl &>/dev/null; then
  GITHUB_META=$(curl -s --max-time 5 https://api.github.com/meta 2>/dev/null || echo "{}")
  for field in git web api packages; do
    for cidr in $(echo "$GITHUB_META" | jq -r ".${field}[]?" 2>/dev/null || true); do
      iptables -A OUTPUT -d "$cidr" -j ACCEPT 2>/dev/null || true
    done
  done
fi

# n8n instance (if configured)
if [ -n "$N8N_API_URL" ]; then
  N8N_HOST=$(echo "$N8N_API_URL" | sed 's|https\?://||' | sed 's|/.*||' | sed 's|:.*||')
  for ip in $(resolve_ips "$N8N_HOST"); do
    ipset add allowed_hosts "$ip" -exist
  done
fi

# ── Flush existing rules ──
iptables -F OUTPUT 2>/dev/null || true

# ── Allow loopback ──
iptables -A OUTPUT -o lo -j ACCEPT

# ── Allow established connections ──
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# ── Allow DNS (UDP + TCP port 53) ──
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# ── Allow HTTPS to whitelisted hosts ──
iptables -A OUTPUT -p tcp --dport 443 -m set --match-set allowed_hosts dst -j ACCEPT

# ── Allow HTTP to whitelisted hosts (npm fallback) ──
iptables -A OUTPUT -p tcp --dport 80 -m set --match-set allowed_hosts dst -j ACCEPT

# ── Allow SSH (for git operations) ──
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT

# ── Block everything else ──
iptables -A OUTPUT -j REJECT --reject-with icmp-admin-prohibited

echo "[firewall] Rules applied: $(iptables -L OUTPUT -n | grep -c 'ACCEPT') ACCEPT, 1 REJECT (default deny)"
