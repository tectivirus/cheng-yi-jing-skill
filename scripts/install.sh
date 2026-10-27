#!/usr/bin/env bash
# 一键安装到 agent 的 skills 目录
# 用法: ./install.sh [dsh|claude|codex]
set -euo pipefail

HOST="${1:-dsh}"
NAME="colleague-cheng-yi-jing"
FILES=(SKILL.md work.md persona.md work_skill.md persona_skill.md manifest.json meta.json LICENSE)

case "$HOST" in
  dsh)    DEST="${DSH_SKILLS_DIR:-$HOME/.dsh/skills}/$NAME" ;;
  claude) DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}/$NAME" ;;
  codex)  DEST="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}/$NAME" ;;
  *) echo "usage: ./install.sh [dsh|claude|codex]" >&2; exit 1 ;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p "$DEST"
for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then echo "missing $f" >&2; exit 1; fi
  cp "$f" "$DEST/$f"
done

echo "installed $NAME -> $DEST"
echo "installed to: $DEST"
