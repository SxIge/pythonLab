"""Shared data-command file validation."""

from pathlib import Path

from c3tool.model import CommandError


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve(strict=False)
    if not path.is_file():
        raise CommandError(f"File not found: {path}")
    return path
