"""List mounted filesystems or logical drives."""

import os

from c3tool.commands.system._support import optional_psutil, run_platform_command
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("mounts", "None", "Shows mounted filesystems or logical drives.", "python3 script.py mounts", "Mount, device, filesystem, and usage rows.", "c3tool.commands.system.mounts:MountsCommand", order=25)


class MountsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List mounted filesystems or logical drives.
        # 1. Require no arguments and prefer psutil's partition information.
        # 2. Add total/free space when the mount is readable.
        # 3. Handle inaccessible mounts without failing the whole command.
        # 4. Provide appropriate Windows and POSIX native-command fallbacks.
        raise NotImplementedError("Implement the mounts command")
