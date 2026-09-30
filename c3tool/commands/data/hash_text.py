"""Calculate a SHA-256 text digest."""

import hashlib

from c3tool.model import BaseCommand, CommandSpec, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("hashText", "<text>", "Calculates a SHA-256 text digest.", "python3 script.py hashText <text>", "A SHA-256 hexadecimal digest.", "c3tool.commands.data.hash_text:HashTextCommand", order=22)


class HashTextCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Calculate a SHA-256 digest for supplied text.
        # 1. Require at least one text argument.
        # 2. Join arguments with spaces and encode the result as UTF-8 bytes.
        # 3. Return the hexadecimal digest as a string.
        raise NotImplementedError("Implement the hashText command")
