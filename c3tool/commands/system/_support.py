"""Shared optional-dependency and platform helpers."""

import subprocess

from c3tool.model import CommandError


def optional_psutil():
    try:
        import psutil

        return psutil
    except ImportError:
        return None


def run_platform_command(arguments: list[str]) -> str:
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise CommandError(f"Platform command failed: {error}") from error
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0 and not output:
        raise CommandError(f"Platform command exited with code {result.returncode}")
    return output
