"""List local user accounts."""

import os

from c3tool.commands.system._support import run_platform_command
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("users", "None", "Lists local user accounts.", "python3 script.py users", "Local account rows.", "c3tool.commands.system.users:UsersCommand", order=17)


class UsersCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List local user accounts on Windows and Linux.
        # 1. Require no arguments and branch on ``os.name``.
        # 2. Windows may use ``run_platform_command`` with a native utility.
        # 3. POSIX systems expose account records through Python's ``pwd`` module.
        # 4. Return a labeled table with the most useful account fields.
        raise NotImplementedError("Implement the users command")
