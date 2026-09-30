"""Connect to a TCP endpoint and print received data."""

import socket

from c3tool.commands.network._addressing import parse_host_port
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("portConnect", "<host:port>", "Connects to a TCP port and prints received data.", "python3 script.py portConnect <host:port>", "The received banner or a no-data message.", "c3tool.commands.network.port_connect:PortConnectCommand", order=32)


class PortConnectCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Connect to one ``host:port`` and read its banner.
        # 1. Require one argument and parse it with ``parse_host_port``.
        # 2. Use short connect/read timeouts and always close the socket.
        # 3. Read in chunks with a sensible maximum so a service cannot stream forever.
        # 4. Decode received bytes safely or report that no data arrived.
        raise NotImplementedError("Implement the portConnect command")
