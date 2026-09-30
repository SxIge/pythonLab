"""Cross-platform system enumeration and process commands."""

from __future__ import annotations

import getpass
import os
import platform
import signal
import socket
import subprocess
import sys

from c3tool.model import BaseCommand, CommandError, ToolContext, UsageError


def optional_psutil():
    """Import psutil only when a command needs it.

    This keeps the core CLI usable before optional classroom dependencies are
    installed and makes dependency-related exercises fail in isolation.
    """

    try:
        import psutil

        return psutil
    except ImportError:
        return None


def run_platform_command(arguments: list[str]) -> str:
    try:
        result = subprocess.run(arguments, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.TimeoutExpired) as error:
        raise CommandError(f"Platform command failed: {error}") from error
    output = (result.stdout or result.stderr).strip()
    if result.returncode != 0 and not output:
        raise CommandError(f"Platform command exited with code {result.returncode}")
    return output


class WhoAmICommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py whoami")
        return getpass.getuser()


class HostnameCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py hostname")
        return socket.gethostname()


class HostInfoCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py hostinfo")
        rows = [
            f"Hostname: {socket.gethostname()}",
            f"OS: {platform.system()} {platform.release()}",
            f"Version: {platform.version()}",
            f"Architecture: {platform.machine()}",
            f"Processor: {platform.processor() or 'unknown'}",
            f"Python: {platform.python_version()}",
            f"CPU count: {os.cpu_count() or 'unknown'}",
        ]
        psutil = optional_psutil()
        if psutil:
            memory = psutil.virtual_memory()
            rows.extend((f"Memory total: {memory.total}", f"Memory available: {memory.available}"))
        return "\n".join(rows)


class InterfacesCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py interfaces")
        psutil = optional_psutil()
        if psutil:
            rows = []
            for interface, addresses in sorted(psutil.net_if_addrs().items()):
                for address in addresses:
                    family = getattr(address.family, "name", str(address.family))
                    rows.append(f"{interface:20} {family:12} {address.address}")
            return "\n".join(rows) if rows else "No interfaces found."

        # Standard-library fallback gives host addresses but not full interface
        # metadata. It is still useful when psutil is intentionally omitted.
        addresses = sorted({item[4][0] for item in socket.getaddrinfo(socket.gethostname(), None)})
        return "\n".join(f"host                 address      {address}" for address in addresses)


class ProcessesCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py processes")
        psutil = optional_psutil()
        if psutil:
            rows = ["PID      USER                 NAME                 COMMAND"]
            for process in psutil.process_iter(("pid", "username", "name", "cmdline")):
                try:
                    info = process.info
                    command = " ".join(info.get("cmdline") or [])
                    rows.append(f"{info['pid']:<8} {(info.get('username') or '-'):20.20} {(info.get('name') or '-'):20.20} {command}")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return "\n".join(rows)
        return run_platform_command(["tasklist"] if os.name == "nt" else ["ps", "-eo", "pid,user,comm,args"])


class ProcessKillCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py processKill <PID>")
        try:
            pid = int(args[0])
        except ValueError as error:
            raise UsageError("PID must be an integer") from error
        if pid <= 1 or pid == os.getpid():
            raise CommandError("Refusing to terminate PID 0, PID 1, or the current tool process")

        psutil = optional_psutil()
        if psutil:
            try:
                process = psutil.Process(pid)
                name = process.name()
                process.terminate()
                process.wait(timeout=5)
                return f"Terminated PID {pid} ({name})"
            except psutil.NoSuchProcess as error:
                raise CommandError(f"Process not found: {pid}") from error
            except psutil.AccessDenied as error:
                raise CommandError(f"Permission denied for PID {pid}") from error
            except psutil.TimeoutExpired as error:
                raise CommandError(f"PID {pid} did not terminate within 5 seconds") from error

        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError as error:
            raise CommandError(f"Process not found: {pid}") from error
        except PermissionError as error:
            raise CommandError(f"Permission denied for PID {pid}") from error
        return f"Sent termination signal to PID {pid}"


class UsersCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py users")
        if os.name == "nt":
            return run_platform_command(["net", "user"])
        import pwd

        rows = ["USERNAME             UID    GID    HOME                         SHELL"]
        for user in pwd.getpwall():
            rows.append(f"{user.pw_name:20.20} {user.pw_uid:<6} {user.pw_gid:<6} {user.pw_dir:28.28} {user.pw_shell}")
        return "\n".join(rows)


class GroupsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py groups")
        if os.name == "nt":
            return run_platform_command(["whoami", "/groups"])
        import grp

        group_ids = set(os.getgroups())
        group_ids.add(os.getgid())
        return "\n".join(sorted(grp.getgrgid(group_id).gr_name for group_id in group_ids))


class EnvironmentCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py env")
        return "\n".join(f"{name}={value}" for name, value in sorted(os.environ.items()))


class MountsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py mounts")
        psutil = optional_psutil()
        if psutil:
            rows = ["DEVICE                         MOUNT                          TYPE       TOTAL        FREE"]
            for partition in psutil.disk_partitions(all=False):
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    rows.append(f"{partition.device:30.30} {partition.mountpoint:30.30} {partition.fstype:10.10} {usage.total:<12} {usage.free}")
                except (PermissionError, OSError):
                    rows.append(f"{partition.device:30.30} {partition.mountpoint:30.30} {partition.fstype:10.10} unavailable")
            return "\n".join(rows)
        if os.name == "nt":
            return run_platform_command(["wmic", "logicaldisk", "get", "caption,filesystem,freespace,size"])
        return run_platform_command(["mount"])
