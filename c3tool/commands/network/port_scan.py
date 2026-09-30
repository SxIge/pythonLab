"""Test one TCP host and port."""

import socket

from c3tool.commands.network._addressing import parse_port
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("portScan", "<host> <port>", "Tests one TCP host and port.", "python3 script.py portScan <host> <port>", "An open or closed result.", "c3tool.commands.network.port_scan:PortScanCommand", order=16)


class PortScanCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Test one TCP host and port only.
        # 1. Require host and port arguments; validate the port with ``parse_port``.
        # 2. Attempt a short ``socket.create_connection``.
        # 3. Close successful sockets promptly with a context manager.
        # 4. Return an open or closed/unreachable result instead of a traceback.
        raise NotImplementedError("Implement the portScan command")
