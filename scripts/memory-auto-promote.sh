#!/usr/bin/env bash
# ~/.claude/scripts/memory-auto-promote.sh
# Daily cron — promote cross-project patterns with safety nets (spec §7.6)

# NOTE: we intentionally do NOT use `set -u` here because associative arrays
# and group-matching logic reference keys that may not exist yet (bash 5.x
# treats unset associative keys as errors under -u). Only -o pipefail is set.
set -o pipefail

case "${OSTYPE:-unknown}" in
  msys*|cygwin*|win32*) VAULT="$HOME/Documents/obsidiano" ;;
  *) VAULT="$HOME/obsidiano" ;;
esac
[ -d "$VAULT" ] || VAULT="$HOME/Documents/obsidiano"

PROJECTS_DIR="$HOME/.claude/projects"
LOG="$VAULT/Claude/memory/.promotion-log.jsonl"
TIMESTAMP=$(date -Iseconds)

# Defaults (overridden by yaml if present)
MIN_PROJECTS=3
MIN_AGE_DAYS=7
SIMILARITY_THRESHOLD=0.75
MAX_PER_RUN=5

# Parse YAML config if present (simple grep — no full yaml parser dep)
CONFIG="$HOME/.claude/config/auto-promote.yaml"
if [ -f "$CONFIG" ]; then
  MIN_PROJECTS=$(grep "min_projects:" "$CONFIG" | awk '{print $2}')
  MIN_AGE_DAYS=$(grep "min_age_days:" "$CONFIG" | awk '{print $2}')
  SIMILARITY_THRESHOLD=$(grep "similarity_threshold:" "$CONFIG" | awk '{print $2}')
  MAX_PER_RUN=$(grep "max_per_run:" "$CONFIG" | awk '{print $2}')
fi

# Normalize content for Jaccard (strip frontmatter, lowercase, strip stopwords)
normalize() {
  awk '/^---$/{c++; next} c>=2 {print}' "$1" | \
    tr '[:upper:]' '[:lower:]' | \
    tr -d '[:punct:]' | \
    tr -s '[:space:]' '\n' | \
    grep -vE '^(de|a|o|que|e|do|da|em|um|para|é|com|não|uma|os|no|se|na|por|mais|as|dos|como|mas|foi|ao|ele|das|à|seu|sua)$' | \
    grep -v '^$' | \
    sort -u
}

jaccard() {
  local file_a="$1"
  local file_b="$2"
  local tmp_a tmp_b
  tmp_a=$(mktemp)
  tmp_b=$(mktemp)
  normalize "$file_a" > "$tmp_a"
  normalize "$file_b" > "$tmp_b"

  local a_count b_count
  a_count=$(wc -l < "$tmp_a")
  b_count=$(wc -l < "$tmp_b")

  # Exclude if either file is too long (>500 tokens)
  if [ "$a_count" -gt 500 ] || [ "$b_count" -gt 500 ]; then
    rm -f "$tmp_a" "$tmp_b"
    echo "0.0"
    return
  fi

  local intersection union
  intersection=$(comm -12 "$tmp_a" "$tmp_b" | wc -l)
  union=$(sort -u "$tmp_a" "$tmp_b" | wc -l)

  rm -f "$tmp_a" "$tmp_b"

  if [ "$union" -eq 0 ]; then
    echo "0.0"
  else
    awk -v i="$intersection" -v u="$union" 'BEGIN { printf "%.4f\n", i/u }'
  fi
}

block_listed() {
  local content="$1"
  if [ -f "$CONFIG" ]; then
    local patterns
    patterns=$(grep -A20 "block_list_patterns:" "$CONFIG" | grep "^\s*-" | sed "s/^\s*- '\(.*\)'$/\1/")
    while IFS= read -r pattern; do
      [ -z "$pattern" ] && continue
      if echo "$content" | grep -qiE "$pattern" 2>/dev/null; then
        return 0
      fi
    done <<< "$patterns"
  fi
  return 1
}

# Heartbeat for empty-state (Day 1 safe)
heartbeat_and_exit() {
  local promoted="$1"
  local eligible="$2"
  local reason="$3"
  mkdir -p "$(dirname "$LOG")"
  echo "{\"timestamp\":\"$TIMESTAMP\",\"action\":\"cron-run\",\"promoted\":$promoted,\"eligible\":$eligible,\"reason\":\"$reason\"}" >> "$LOG"
  exit 0
}

# Collect candidates: feedback_*.md and user_*.md older than MIN_AGE_DAYS
CANDIDATES=()
if [ -d "$PROJECTS_DIR" ]; then
  while IFS= read -r f; do
    AGE_DAYS=$(( ( $(date +%s) - $(stat -c '%Y' "$f" 2>/dev/null || echo 0) ) / 86400 ))
    [ "$AGE_DAYS" -ge "$MIN_AGE_DAYS" ] && CANDIDATES+=("$f")
  done < <(find "$PROJECTS_DIR" -name "feedback_*.md" -o -name "user_*.md" 2>/dev/null)
fi

if [ "${#CANDIDATES[@]}" -lt "$MIN_PROJECTS" ]; then
  heartbeat_and_exit 0 "${#CANDIDATES[@]}" "insufficient_candidates"
fi

# Group by similarity (O(n²) — fine for small candidate pools)
declare -A PROMO_GROUPS
declare -A GROUP_FILES
GROUP_ID=0

for file_a in "${CANDIDATES[@]}"; do
  ASSIGNED=""
  for gid in "${!PROMO_GROUPS[@]}"; do
    first_file="${GROUP_FILES[$gid]%% *}"
    SIM=$(jaccard "$file_a" "$first_file")
    if awk "BEGIN { exit !($SIM >= $SIMILARITY_THRESHOLD) }"; then
      PROMO_GROUPS[$gid]=$((PROMO_GROUPS[$gid] + 1))
      GROUP_FILES[$gid]+=" $file_a"
      ASSIGNED="yes"
      break
    fi
  done
  if [ -z "$ASSIGNED" ]; then
    GROUP_ID=$((GROUP_ID + 1))
    PROMO_GROUPS[$GROUP_ID]=1
    GROUP_FILES[$GROUP_ID]="$file_a"
  fi
done

# Promote groups with count >= MIN_PROJECTS
PROMOTED=0
for gid in "${!PROMO_GROUPS[@]}"; do
  [ "$PROMOTED" -ge "$MAX_PER_RUN" ] && break
  if [ "${PROMO_GROUPS[$gid]}" -ge "$MIN_PROJECTS" ]; then
    files=(${GROUP_FILES[$gid]})
    first="${files[0]}"

    # Read content (skip frontmatter)
    CONTENT=$(awk '/^---$/{c++; next} c>=2' "$first")

    # Block-list check
    if block_listed "$CONTENT"; then
      continue
    fi

    # Check if already promoted (hash-based)
    HASH=$(echo "$CONTENT" | sha256sum | cut -c1-16)
    if grep -q "\"hash\":\"$HASH\"" "$LOG" 2>/dev/null; then
      continue
    fi

    ENTRY_ID="prom-$(date +%Y-%m-%d)-$HASH"

    # Determine target (feedback -> preferences.md by default)
    TARGET="$VAULT/Claude/memory/preferences.md"

    # Append promoted entry with tag
    cat >> "$TARGET" <<EOF

## [auto-promoted $(date +%Y-%m-%d)] from ${PROMO_GROUPS[$gid]} projects
$CONTENT

> *auto_promoted: true | promoted_from: ${PROMO_GROUPS[$gid]} projects | entry_id: $ENTRY_ID | revert: \`memory-revert $ENTRY_ID\`*
EOF

    # Audit log
    echo "{\"timestamp\":\"$TIMESTAMP\",\"action\":\"promote\",\"target\":\"preferences.md\",\"entry_id\":\"$ENTRY_ID\",\"hash\":\"$HASH\",\"sources_count\":${PROMO_GROUPS[$gid]},\"confidence\":0.80}" >> "$LOG"

    PROMOTED=$((PROMOTED + 1))
  fi
done

# Final heartbeat
heartbeat_and_exit "$PROMOTED" "${#CANDIDATES[@]}" "cron_complete"
