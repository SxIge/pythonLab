"""Compatibility view of the recursively discovered command contracts."""

from c3tool.discovery import discover_command_specs


COMMAND_SPECS = discover_command_specs()
