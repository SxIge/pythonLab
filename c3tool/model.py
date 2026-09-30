"""Shared command models and intentionally small framework primitives."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from c3tool.registry import CommandRegistry


class CommandError(Exception):
    """A user-facing command failure that should not produce a traceback."""


class UsageError(CommandError):
    """The user supplied the wrong number or shape of arguments."""


class FeatureUnavailable(CommandError):
    """A handler is absent, unfinished, or missing an optional dependency."""


@dataclass(frozen=True)
class CommandSpec:
    """Permanent public contract for one command.

    The handler is stored as ``module:ClassName`` so importing one broken or
    intentionally removed exercise never prevents the rest of the CLI loading.
    """

    name: str
    args: str
    description: str
    usage: str
    expected_output: str
    handler: str
    order: int = 999


@dataclass
class ToolContext:
    """Runtime services shared by handlers."""

    cwd: Path
    output_dir: Path
    registry: "CommandRegistry"


class BaseCommand:
    """Small handler interface used by every implementation."""

    def run(self, args: Sequence[str], context: ToolContext) -> str:
        raise NotImplementedError("Command implementation has not been written")

    @staticmethod
    def require_count(args: Sequence[str], expected: int, usage: str) -> None:
        if len(args) != expected:
            raise UsageError(f"Usage: {usage}")

    @staticmethod
    def require_range(args: Sequence[str], minimum: int, maximum: int, usage: str) -> None:
        if not minimum <= len(args) <= maximum:
            raise UsageError(f"Usage: {usage}")
