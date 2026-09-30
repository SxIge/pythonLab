"""Network reachability, socket, download, and lab SSH commands."""

from __future__ import annotations

import os
import socket
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from c3tool.model import BaseCommand, CommandError, FeatureUnavailable, ToolContext, UsageError


def parse_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise UsageError("Port must be an integer") from error
    if not 1 <= port <= 65535:
        raise UsageError("Port must be between 1 and 65535")
    return port


def parse_host_port(value: str) -> tuple[str, int]:
    """Parse hostname:port, including bracketed IPv6 addresses."""

    if value.startswith("[") and "]:" in value:
        host, port_text = value[1:].rsplit("]:", 1)
    elif ":" in value:
        host, port_text = value.rsplit(":", 1)
    else:
        raise UsageError("Expected host:port")
    if not host:
        raise UsageError("Host cannot be empty")
    return host, parse_port(port_text)


class PingCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py ping <IP>")
        count_flag = "-n" if os.name == "nt" else "-c"
        timeout_flag = ["-w", "2000"] if os.name == "nt" else ["-W", "2"]
        try:
            result = subprocess.run(
                ["ping", count_flag, "1", *timeout_flag, args[0]],
                capture_output=True,
                text=True,
                timeout=8,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise CommandError(f"Ping failed to run: {error}") from error
        state = "online" if result.returncode == 0 else "offline"
        detail = (result.stdout or result.stderr).strip()
        return f"{args[0]} is {state}\n{detail}"


class PortsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py ports")
        try:
            import psutil
        except ImportError:
            command = ["netstat", "-ano"] if os.name == "nt" else ["netstat", "-tulpen"]
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=20, check=False)
            except OSError as error:
                raise FeatureUnavailable("Install psutil or provide netstat for the ports command") from error
            return (result.stdout or result.stderr).strip()

        rows = ["PROTO  ADDRESS                                      PORT   SERVICE          PID"]
        for connection in psutil.net_connections(kind="inet"):
            listening = connection.status == psutil.CONN_LISTEN or connection.type == socket.SOCK_DGRAM
            if not connection.laddr or not listening:
                continue
            address = connection.laddr.ip
            port = connection.laddr.port
            try:
                service = socket.getservbyport(port, "tcp" if connection.type == socket.SOCK_STREAM else "udp")
            except OSError:
                service = "-"
            protocol = "tcp" if connection.type == socket.SOCK_STREAM else "udp"
            rows.append(f"{protocol:6} {address:44.44} {port:<6} {service:16.16} {connection.pid or '-'}")
        return "\n".join(rows)


class PortScanCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 2, "python3 script.py portScan <host> <port>")
        host, port = args[0], parse_port(args[1])
        try:
            with socket.create_connection((host, port), timeout=3):
                return f"{host}:{port} is open"
        except (OSError, socket.timeout) as error:
            return f"{host}:{port} is closed or unreachable ({error})"


class PortConnectCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py portConnect <host:port>")
        host, port = parse_host_port(args[0])
        chunks = []
        try:
            with socket.create_connection((host, port), timeout=4) as connection:
                connection.settimeout(2)
                while sum(map(len, chunks)) < 65536:
                    try:
                        chunk = connection.recv(min(4096, 65536 - sum(map(len, chunks))))
                    except socket.timeout:
                        break
                    if not chunk:
                        break
                    chunks.append(chunk)
        except OSError as error:
            raise CommandError(f"Could not connect to {host}:{port}: {error}") from error
        if not chunks:
            return f"Connected to {host}:{port}; no data was received before timeout."
        return b"".join(chunks).decode("utf-8", errors="replace")


class DownloadCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_range(args, 1, 2, "python3 script.py download <sourceURL> [pathToSave]")
        source = args[0]
        parsed = urllib.parse.urlparse(source)
        if parsed.scheme not in {"http", "https"}:
            raise CommandError("download supports only HTTP and HTTPS URLs")
        default_name = Path(urllib.parse.unquote(parsed.path)).name or "downloaded-file"
        destination = Path(args[1]).expanduser() if len(args) == 2 else context.cwd / default_name
        if not destination.is_absolute():
            destination = context.cwd / destination
        destination = destination.resolve(strict=False)
        destination.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(source, headers={"User-Agent": "C3T-Python-Tools/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response, destination.open("wb") as output:
                total = 0
                while True:
                    chunk = response.read(65536)
                    if not chunk:
                        break
                    output.write(chunk)
                    total += len(chunk)
        except Exception as error:
            destination.unlink(missing_ok=True)
            raise CommandError(f"Download failed: {error}") from error
        return f"Downloaded {total} bytes to {destination}"


def parse_ssh_target(value: str) -> tuple[str, str, int]:
    """Accept both user:host:port and familiar user@host:port notation."""

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
    """Small, sequential password audit for the dedicated classroom SSH VM."""

    MAX_ATTEMPTS = 10_000

    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 2, "python3 script.py sshCracker <user:IP:port> <passwordFile>")
        user, host, port = parse_ssh_target(args[0])
        password_file = Path(args[1]).expanduser().resolve(strict=False)
        if not password_file.is_file():
            raise CommandError(f"Password file not found: {password_file}")
        try:
            import paramiko
        except ImportError as error:
            raise FeatureUnavailable("Install paramiko to use sshCracker") from error

        passwords = password_file.read_text(encoding="utf-8", errors="replace").splitlines()
        if len(passwords) > self.MAX_ATTEMPTS:
            raise CommandError(f"Password file exceeds the {self.MAX_ATTEMPTS}-attempt classroom limit")

        for attempt_number, password in enumerate(passwords, start=1):
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(
                    hostname=host,
                    port=port,
                    username=user,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False,
                    timeout=4,
                    auth_timeout=4,
                    banner_timeout=4,
                )
                return f"Password found after {attempt_number} attempts: {password}"
            except paramiko.AuthenticationException:
                continue
            except (paramiko.SSHException, OSError) as error:
                raise CommandError(f"SSH service error at {host}:{port}: {error}") from error
            finally:
                client.close()
        return f"No password matched after {len(passwords)} attempts."
