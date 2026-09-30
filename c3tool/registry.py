"""Lazy command resolution that keeps partial student builds runnable."""

from __future__ import annotations

import importlib
from difflib import get_close_matches
from typing import Iterable

from c3tool.model import BaseCommand, CommandSpec, FeatureUnavailable


class MissingCommand(BaseCommand):
    """Fallback used when an exercise implementation is absent or broken."""

    def __init__(self, spec: CommandSpec, reason: str) -> None:
        self.spec = spec
        self.reason = reason

    def run(self, args, context) -> str:
        raise FeatureUnavailable(
            f"Command '{self.spec.name}' is unavailable: {self.reason}. "
            "Reimplement its handler to enable this level."
        )


class CommandRegistry:
    def __init__(self, specs: Iterable[CommandSpec]) -> None:
        self._specs = {item.name: item for item in specs}

    @property
    def specs(self) -> tuple[CommandSpec, ...]:
        return tuple(sorted(self._specs.values(), key=lambda item: (item.order, item.name.casefold())))

    def get_spec(self, name: str) -> CommandSpec | None:
        return self._specs.get(name)

    def suggestions(self, name: str) -> list[str]:
        return get_close_matches(name, self._specs, n=3, cutoff=0.45)

    def load(self, name: str) -> BaseCommand | None:
        spec = self.get_spec(name)
        if spec is None:
            return None

        module_name, class_name = spec.handler.split(":", 1)
        try:
            module = importlib.import_module(module_name)
            command_class = getattr(module, class_name)
            command = command_class()
            if not isinstance(command, BaseCommand):
                raise TypeError(f"{class_name} is not a BaseCommand")
            return command
        except (ImportError, AttributeError, SyntaxError, TypeError) as error:
            # One removed or unfinished module becomes one unavailable command
            # instead of breaking startup or unrelated command implementations.
            return MissingCommand(spec, f"{type(error).__name__}: {error}")
