"""List running processes."""

import os

from c3tool.commands.system._support import optional_psutil, run_platform_command
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("processes", "None", "Lists running processes.", "python3 script.py processes", "PID, user, name, and command rows.", "c3tool.commands.system.processes:ProcessesCommand", order=12)


class ProcessesCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Produce a process table with PID, user, name, and command.
        # 1. Require no arguments and prefer ``optional_psutil``.
        # 2. Processes can disappear while iterating, so handle those races.
        # 3. If psutil is unavailable, run the correct native command for the OS.
        # 4. Return text instead of printing inside the command.
        raise NotImplementedError("Implement the processes command")
