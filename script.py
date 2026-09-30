#!/usr/bin/env python3
"""Discover every command module recursively, then start the C3T CLI."""

from c3tool.cli import main
from c3tool.discovery import discover_command_specs
from c3tool.registry import CommandRegistry


if __name__ == "__main__":
    registry = CommandRegistry(discover_command_specs())
    raise SystemExit(main(registry=registry))
