"""List environment variables."""

import os

from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("env", "None", "Lists environment variables.", "python3 script.py env", "Sorted NAME=value rows.", "c3tool.commands.system.environment:EnvironmentCommand", order=19)


class EnvironmentCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Require no arguments and format ``os.environ``.
        # Sort by variable name and return one ``NAME=value`` entry per line.
        # Remember that environment values are already strings.
        raise NotImplementedError("Implement the env command")
