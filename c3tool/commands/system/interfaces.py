"""List network interfaces and addresses."""

import socket

from c3tool.commands.system._support import optional_psutil
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("interfaces", "None", "Lists network interfaces and addresses.", "python3 script.py interfaces", "Interface and address rows.", "c3tool.commands.system.interfaces:InterfacesCommand", order=11)


class InterfacesCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List interface names, address families, and addresses.
        # 1. Require no arguments.
        # 2. Prefer psutil when available because it exposes every interface.
        # 3. Provide a standard-library socket fallback when psutil is absent.
        # 4. Return stable rows or a clear empty result.
        raise NotImplementedError("Implement the interfaces command")
