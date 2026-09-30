"""Recursive command discovery for the folder-based command architecture."""

from __future__ import annotations

import importlib
import pkgutil

import c3tool.commands
from c3tool.model import CommandSpec


def discover_command_specs() -> tuple[CommandSpec, ...]:
    """Import every non-private module below ``c3tool.commands``.

    A command module registers itself by exposing one ``COMMAND_SPEC`` value.
    New category folders and command files are picked up automatically; there
    is no central command list to update.
    """

    discovered: dict[str, CommandSpec] = {}
    prefix = f"{c3tool.commands.__name__}."
    modules = sorted(pkgutil.walk_packages(c3tool.commands.__path__, prefix), key=lambda item: item.name)
    for module_info in modules:
        if module_info.ispkg or any(part.startswith("_") for part in module_info.name.split(".")):
            continue
        module = importlib.import_module(module_info.name)
        spec = getattr(module, "COMMAND_SPEC", None)
        if spec is None:
            continue
        if not isinstance(spec, CommandSpec):
            raise TypeError(f"{module_info.name}.COMMAND_SPEC must be a CommandSpec")
        if spec.name in discovered:
            raise ValueError(f"Duplicate command name discovered: {spec.name}")
        discovered[spec.name] = spec
    return tuple(sorted(discovered.values(), key=lambda item: (item.order, item.name.casefold())))
