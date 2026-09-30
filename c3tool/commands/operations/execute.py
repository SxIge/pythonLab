"""Run one command through Bash or PowerShell."""

import os
import shutil
import subprocess

from c3tool.model import BaseCommand, CommandError, CommandSpec, FeatureUnavailable, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("exec", "<command>", "Runs a command in Bash or PowerShell.", "python3 script.py exec <command>", "Captured stdout, stderr, and exit code.", "c3tool.commands.operations.execute:ExecCommand", order=27)


class ExecCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Run a command through the platform's normal shell.
        # 1. Require command text and join all command-line pieces.
        # 2. Select non-interactive PowerShell on Windows or Bash elsewhere.
        # 3. Capture stdout/stderr, enforce a timeout, and keep the exit code.
        # 4. Raise friendly errors when the shell is absent or cannot start.
        # 5. Return the captured sections; do not print from this method.
        raise NotImplementedError("Implement the exec command")
