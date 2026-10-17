#!/bin/bash
set -e

# Persistent cross-repo Idea Vault helper for the brainstormer skill.
# Stores IDEA.md briefs in ${IDEA_VAULT_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/brainstormer/ideas}
# so ideas brainstormed before a repository exists can be pulled into a new repo later.

TMP_FILE=""
cleanup() {
  if [ -n "$TMP_FILE" ] && [ -f "$TMP_FILE" ]; then
    rm -f "$TMP_FILE"
  fi
}
trap cleanup EXIT

VAULT_DIR="${IDEA_VAULT_DIR:-${XDG_CONFIG_HOME:-$HOME/.config}/brainstormer/ideas}"
mkdir -p "$VAULT_DIR"

ACTION="${1:-help}"
SLUG="${2:-}"
TARGET_PATH="${3:-./IDEA.md}"

json_escape() {
  python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().strip()))'
}

case "$ACTION" in
  save)
    if [ -z "$SLUG" ]; then
      echo "Error: Usage: $0 save <slug> [source-file-or-stdin]" >&2
      exit 1
    fi
    SAFE_SLUG="$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+|-+$//g')"
    IDEA_DIR="$VAULT_DIR/$SAFE_SLUG"
    mkdir -p "$IDEA_DIR"
    DEST_FILE="$IDEA_DIR/IDEA.md"

    if [ -n "${3:-}" ] && [ -f "${3}" ]; then
      cp "${3}" "$DEST_FILE"
    else
      TMP_FILE="$(mktemp)"
      cat > "$TMP_FILE"
      mv "$TMP_FILE" "$DEST_FILE"
    fi

    ln -sfn "$DEST_FILE" "$VAULT_DIR/latest.md"
    echo "Saved idea '$SAFE_SLUG' to persistent vault: $DEST_FILE" >&2
    printf '{"status":"saved","slug":%s,"vault_path":%s,"latest_link":%s}\n' \
      "$(printf '%s' "$SAFE_SLUG" | json_escape)" \
      "$(printf '%s' "$DEST_FILE" | json_escape)" \
      "$(printf '%s' "$VAULT_DIR/latest.md" | json_escape)"
    ;;

  list)
    echo "Listing saved ideas in $VAULT_DIR" >&2
    VAULT_DIR="$VAULT_DIR" python3 -c '
import json, os, pathlib

vault = pathlib.Path(os.environ["VAULT_DIR"])
ideas = []
if vault.exists():
    for entry in sorted(vault.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if entry.is_dir() and (entry / "IDEA.md").is_file():
            idea_file = entry / "IDEA.md"
            first_heading = ""
            for line in idea_file.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("# "):
                    first_heading = line[2:].strip()
                    break
            ideas.append({
                "slug": entry.name,
                "title": first_heading,
                "path": str(idea_file),
            })
print(json.dumps({"vault_dir": str(vault), "count": len(ideas), "ideas": ideas}, indent=2))
'
    ;;

  pull)
    if [ -z "$SLUG" ] || [ "$SLUG" = "latest" ]; then
      SOURCE_FILE="$VAULT_DIR/latest.md"
      RESOLVED_SLUG="latest"
    else
      SAFE_SLUG="$(echo "$SLUG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9._-]+/-/g; s/^-+|-+$//g')"
      SOURCE_FILE="$VAULT_DIR/$SAFE_SLUG/IDEA.md"
      RESOLVED_SLUG="$SAFE_SLUG"
    fi

    if [ ! -f "$SOURCE_FILE" ]; then
      echo "Error: No saved IDEA.md found for '$SLUG' in $VAULT_DIR" >&2
      exit 1
    fi

    mkdir -p "$(dirname "$TARGET_PATH")"
    cp -L "$SOURCE_FILE" "$TARGET_PATH"
    echo "Pulled '$RESOLVED_SLUG' from vault into $TARGET_PATH" >&2
    printf '{"status":"pulled","slug":%s,"source":%s,"target":%s}\n' \
      "$(printf '%s' "$RESOLVED_SLUG" | json_escape)" \
      "$(printf '%s' "$SOURCE_FILE" | json_escape)" \
      "$(printf '%s' "$TARGET_PATH" | json_escape)"
    ;;

  *)
    echo "Usage: $0 {save <slug> [source-file] | list | pull [slug|latest] [target-path]}" >&2
    exit 1
    ;;
esac
