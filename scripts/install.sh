#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"
SOURCE_JSON="$REPO_ROOT/assets/pet.json"
SOURCE_SPRITESHEET="$REPO_ROOT/assets/spritesheet.webp"
PET_ID="phoebe-codex"

PET_DIR="${CODEX_PET_DIR:-${CODEX_HOME:-$HOME/.codex}/pets/$PET_ID}"
DRY_RUN=0
NO_BACKUP=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [options]

Install the Phoebe Codex Pet runtime pair into a Codex v2 pet directory.

Options:
  --dry-run                 Print the plan without writing files
  --no-backup               Do not back up an existing pet directory
  --pet-dir PATH            Override the destination directory
  -h, --help                Show this help

Environment:
  CODEX_HOME                Optional Codex data root
  CODEX_PET_DIR             Optional full destination override
EOF
}

while (($# > 0)); do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --no-backup)
      NO_BACKUP=1
      shift
      ;;
    --pet-dir)
      if (($# < 2)); then
        echo "error: --pet-dir needs a path" >&2
        exit 2
      fi
      PET_DIR="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -f "$SOURCE_JSON" || ! -f "$SOURCE_SPRITESHEET" ]]; then
  echo "error: the repository is missing assets/pet.json or assets/spritesheet.webp" >&2
  exit 1
fi

if [[ -L "$PET_DIR" ]]; then
  echo "error: refusing to install through a symbolic-link destination: $PET_DIR" >&2
  exit 1
fi

if [[ -e "$PET_DIR" && ! -d "$PET_DIR" ]]; then
  echo "error: destination exists but is not a directory: $PET_DIR" >&2
  exit 1
fi

BACKUP_DIR=""
if [[ -d "$PET_DIR" ]]; then
  if ((NO_BACKUP == 0)); then
    BACKUP_BASE="${PET_DIR}.backup-$(date +%Y%m%d-%H%M%S)"
    BACKUP_DIR="$BACKUP_BASE"
    BACKUP_INDEX=1
    while [[ -e "$BACKUP_DIR" || -L "$BACKUP_DIR" ]]; do
      BACKUP_DIR="${BACKUP_BASE}-${BACKUP_INDEX}"
      BACKUP_INDEX=$((BACKUP_INDEX + 1))
    done
  fi
fi

if ((DRY_RUN == 1)); then
  echo "[dry-run] destination: $PET_DIR"
  if [[ -n "$BACKUP_DIR" ]]; then
    echo "[dry-run] backup:      $BACKUP_DIR"
  elif [[ -d "$PET_DIR" ]]; then
    echo "[dry-run] backup:      skipped (--no-backup)"
  fi
  echo "[dry-run] copy:         pet.json"
  echo "[dry-run] copy:         spritesheet.webp"
  exit 0
fi

if [[ -n "$BACKUP_DIR" ]]; then
  cp -R "$PET_DIR" "$BACKUP_DIR"
  echo "Backed up existing pet to: $BACKUP_DIR"
fi

mkdir -p "$PET_DIR"
cp "$SOURCE_JSON" "$PET_DIR/pet.json"
cp "$SOURCE_SPRITESHEET" "$PET_DIR/spritesheet.webp"

echo "Installed Phoebe Codex Pet."
echo "Runtime directory: $PET_DIR"
echo "Restart or reload Codex to refresh the pet list."
