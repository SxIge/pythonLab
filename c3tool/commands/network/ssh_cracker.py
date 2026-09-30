"""Audit a dedicated classroom SSH account with a password list."""

from pathlib import Path

from c3tool.commands.network._addressing import parse_host_port, parse_port
from c3tool.model import BaseCommand, CommandError, CommandSpec, FeatureUnavailable, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("sshCracker", "<user:IP:port> <passwordFile>", "Audits a lab SSH account using a password list.", "python3 script.py sshCracker <user:IP:port> <passwordFile>", "The accepted password or a not-found result.", "c3tool.commands.network.ssh_cracker:SshCrackerCommand", order=24)


def parse_ssh_target(value: str) -> tuple[str, str, int]:
    if "@" in value:
        user, address = value.split("@", 1)
        host, port = parse_host_port(address)
        return user, host, port
    parts = value.rsplit(":", 2)
    if len(parts) != 3:
        raise UsageError("SSH target must be user:IP:port or user@IP:port")
    user, host, port_text = parts
    if not user or not host:
        raise UsageError("SSH user and host cannot be empty")
    return user, host, parse_port(port_text)


class SshCrackerCommand(BaseCommand):
    MAX_ATTEMPTS = 10_000

    def run(self, args, context: ToolContext) -> str:
        # TODO: Audit only the supplied classroom SSH target.
        # 1. Require target/password-file arguments and use ``parse_ssh_target``.
        # 2. Validate the file and enforce MAX_ATTEMPTS before making connections.
        # 3. Import paramiko here so other commands work without that dependency.
        # 4. Try passwords sequentially, always close the client, and distinguish
        #    a rejected password from a service/network error.
        # 5. Return the accepted password or a not-found summary.
        raise NotImplementedError("Implement the sshCracker command")
