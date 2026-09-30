"""Calculate a streaming SHA-256 file digest."""

import hashlib

from c3tool.commands.data._files import existing_file
from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("hashFile", "<file>", "Calculates a streaming SHA-256 file digest.", "python3 script.py hashFile <file>", "A SHA-256 hexadecimal digest.", "c3tool.commands.data.hash_file:HashFileCommand", order=23)


class HashFileCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Calculate a SHA-256 digest without loading the whole file.
        # 1. Require one existing file.
        # 2. Open it in binary mode and update a hash object chunk by chunk.
        # 3. Return the final hexadecimal digest.
        raise NotImplementedError("Implement the hashFile command")
