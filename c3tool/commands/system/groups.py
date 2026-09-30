"""List current-account group memberships."""

import os

from c3tool.commands.system._support import run_platform_command
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("groups", "None", "Lists current account group memberships.", "python3 script.py groups", "Group names or platform group rows.", "c3tool.commands.system.groups:GroupsCommand", order=18)


class GroupsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List group memberships for the current account.
        # 1. Require no arguments and select a Windows or POSIX approach.
        # 2. On POSIX, include both supplementary groups and the primary group.
        # 3. Resolve numeric IDs to names and return stable, sorted output.
        raise NotImplementedError("Implement the groups command")
