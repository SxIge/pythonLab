"""Report lines matching a regular expression."""

import re

from c3tool.commands.files._paths import require_existing_file
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("grep", "<filename> <regex>", "Shows matching lines and line numbers.", "python3 script.py grep <filename> <regex>", "line_number: matching text rows.", "c3tool.commands.files.grep:GrepCommand", order=21)


class GrepCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Search a text file with a regular expression.
        # 1. Require a filename and regex, then validate both.
        # 2. Convert regex compilation errors into CommandError messages.
        # 3. Check each line while counting from line 1.
        # 4. Return ``line_number: text`` rows or a no-match message.
        raise NotImplementedError("Implement the grep command")
