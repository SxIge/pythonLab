"""Shared path helpers for filesystem command modules."""

from pathlib import Path

from c3tool.model import CommandError, ToolContext


def expand_path(value: str, context: ToolContext) -> Path:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = context.cwd / candidate
    return candidate.resolve(strict=False)


def require_existing_file(value: str, context: ToolContext) -> Path:
    path = expand_path(value, context)
    if not path.is_file():
        raise CommandError(f"File not found: {path}")
    return path
