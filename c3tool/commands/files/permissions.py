"""Show cross-platform path permissions and ownership metadata."""

import os
import stat

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("permissions", "<file>", "Shows permissions and ownership for a path.", "python3 script.py permissions <file>", "Numeric mode, symbolic mode, owner, and group.", "c3tool.commands.files.permissions:PermissionsCommand", order=26)


class PermissionsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Describe a path's permissions and ownership.
        # 1. Require and validate one path.
        # 2. Use ``Path.stat`` and the ``stat`` module for symbolic/numeric modes.
        # 3. On POSIX, resolve owner and group names; provide a Windows fallback.
        # 4. Return labeled rows that are useful to a beginner reading the output.
        raise NotImplementedError("Implement the permissions command")
