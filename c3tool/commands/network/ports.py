"""List local listening TCP and UDP endpoints."""

import os
import socket
import subprocess

from c3tool.model import BaseCommand, CommandSpec, FeatureUnavailable, ToolContext

COMMAND_SPEC = CommandSpec("ports", "None", "Lists local listening ports and services.", "python3 script.py ports", "Listening endpoints and service details.", "c3tool.commands.network.ports:PortsCommand", order=15)


class PortsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List local listening TCP ports and local UDP endpoints.
        # 1. Require no arguments and try importing psutil inside this method.
        # 2. Filter out connections that are not listening/local endpoints.
        # 3. Resolve common service names when possible and include the PID.
        # 4. If psutil is absent, use an OS-appropriate netstat fallback.
        raise NotImplementedError("Implement the ports command")
