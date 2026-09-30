"""Terminate one process by PID."""

import os
import signal

from c3tool.commands.system._support import optional_psutil
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("processKill", "<PID>", "Terminates a process by PID.", "python3 script.py processKill <PID>", "A termination confirmation.", "c3tool.commands.system.process_kill:ProcessKillCommand", order=13)


class ProcessKillCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Terminate exactly one process safely.
        # 1. Require one integer PID and reject PID 0, PID 1, and this process.
        # 2. Prefer psutil so you can wait briefly and report useful errors.
        # 3. Fall back to ``os.kill`` plus SIGTERM when psutil is unavailable.
        # 4. Never silently ignore missing processes or permission failures.
        raise NotImplementedError("Implement the processKill command")
