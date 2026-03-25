#!/bin/bash
# Claude Code Statusline — optimized single-jq extraction

INPUT=$(cat)

# Single jq call extracting all fields
eval "$(echo "$INPUT" | jq -r '
  "model=" + (.model.display_name // "---" | @sh) +
  " ctx=" + (.context_window.used_percentage // 0 | tostring | split(".")[0] | @sh) +
  " duration_ms=" + (.cost.total_duration_ms // 0 | tostring | split(".")[0] | @sh) +
  " cost_usd=" + (.cost.total_cost_usd // 0 | tostring | @sh) +
  " project=" + ((.workspace.project_dir // .cwd // "---") | split("/")[-1] | @sh) +
  " sid=" + ((.session_id // "---")[0:8] | @sh) +
  " agent=" + (.agent.name // "" | @sh) +
  " branch=" + (.worktree.branch // "" | @sh)
')"

# Duration: ms -> Xm Ys
if [ "$duration_ms" -gt 0 ] 2>/dev/null; then
  total_sec=$((duration_ms / 1000))
  mins=$((total_sec / 60))
  secs=$((total_sec % 60))
  if [ "$mins" -gt 0 ]; then
    duration="${mins}m ${secs}s"
  else
    duration="${secs}s"
  fi
else
  duration="0s"
fi

# Progress bar (10 chars) — use printf for UTF-8
filled=$((ctx / 10))
empty=$((10 - filled))
bar=""
for ((i=0; i<filled; i++)); do bar+=$(printf '\xe2\x96\x93'); done
for ((i=0; i<empty; i++)); do bar+=$(printf '\xe2\x96\x91'); done

# Color based on context usage
if [ "$ctx" -ge 80 ]; then
  color="\033[31m"  # red
elif [ "$ctx" -ge 60 ]; then
  color="\033[33m"  # yellow
else
  color="\033[32m"  # green
fi
reset="\033[0m"
dim="\033[2m"
cyan="\033[36m"
bold="\033[1m"
green="\033[32m"

# Agent color: pick a consistent color from palette based on agent name
agent_color() {
  local name="$1"
  local hash=0
  for ((i=0; i<${#name}; i++)); do
    hash=$(( (hash * 31 + $(printf '%d' "'${name:$i:1}")) % 7 ))
  done
  local colors=("\033[35m" "\033[36m" "\033[34m" "\033[33m" "\033[32m" "\033[95m" "\033[96m")
  echo "${colors[$hash]}"
}

# Format cost (avoid bc dependency — use awk)
cost_fmt=$(awk "BEGIN { c=$cost_usd+0; if (c>0) printf \"\\$%.2f\", c; else print \"\\$0.00\" }" 2>/dev/null || echo "\$0.00")

# Line 1: model + project + optional agent/worktree
line1="${cyan}${model}${reset} ${dim}|${reset} ${project}"
if [ -n "$agent" ]; then
  acolor=$(agent_color "$agent")
  line1+=" ${dim}|${reset} ${acolor}${bold}[${agent}]${reset}"
fi
[ -n "$branch" ] && line1+=" ${dim}|${reset} ${branch}"

# Line 2: progress bar + duration + cost + session
line2="${color}${bar}${reset} ${ctx}% ${dim}|${reset} ${duration} ${dim}|${reset} ${green}${cost_fmt}${reset} ${dim}|${reset} ${dim}#${sid}${reset}"

printf '%b\n' "$line1"
printf '%b\n' "$line2"
