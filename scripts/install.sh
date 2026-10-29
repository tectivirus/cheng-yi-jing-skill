#!/usr/bin/env bash
# 一键安装到 agent 的 skills 目录
# 用法: ./scripts/install.sh [dsh|claude|codex]
set -euo pipefail

HOST="${1:-dsh}"
NAME="celebrity-cheng-yi-jing"
FILES=(SKILL.md work.md persona.md work_skill.md persona_skill.md manifest.json meta.json LICENSE)

case "$HOST" in
  dsh)    DEST="${DSH_SKILLS_DIR:-$HOME/.dsh/skills}/$NAME" ;;
  claude) DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/$NAME" ;;
  codex)  DEST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}/$NAME" ;;
  *) echo "usage: ./scripts/install.sh [dsh|claude|codex]" >&2; exit 1 ;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p "$DEST" "$DEST/tools" "$DEST/fixtures"
for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then echo "missing $f" >&2; exit 1; fi
  cp "$f" "$DEST/$f"
done
cp tools/lint_h3_prompt.py "$DEST/tools/"
cp fixtures/*.txt "$DEST/fixtures/"

echo "installed $NAME -> $DEST"