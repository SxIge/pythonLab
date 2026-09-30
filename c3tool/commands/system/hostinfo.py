"""Show operating-system and hardware information."""

import os
import platform
import socket

from c3tool.commands.system._support import optional_psutil
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("hostinfo", "None", "Shows operating system and hardware information.", "python3 script.py hostinfo", "A structured host summary.", "c3tool.commands.system.hostinfo:HostInfoCommand", order=10)


class HostInfoCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Build a labeled summary of this computer.
        # 1. Require no arguments.
        # 2. Collect hostname, OS, version, architecture, Python, and CPU details.
        # 3. If ``optional_psutil()`` returns a module, add memory information.
        # 4. Use sensible fallback text when a platform cannot provide a value.
        raise NotImplementedError("Implement the hostinfo command")
