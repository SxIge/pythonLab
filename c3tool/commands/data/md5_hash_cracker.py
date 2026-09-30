"""Recover classroom MD5 values using a wordlist."""

import hashlib

from c3tool.commands.data._files import existing_file
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("md5HashCracker", "<hashFilePath> <wordlistFilePath>", "Recovers classroom MD5 values using a wordlist.", "python3 script.py md5HashCracker <hashFilePath> <wordlistFilePath>", "Recovered hash-to-word mappings.", "c3tool.commands.data.md5_hash_cracker:Md5HashCrackerCommand", order=30)


class Md5HashCrackerCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Match classroom MD5 hashes against a wordlist.
        # 1. Require and validate both input files.
        # 2. Normalize target hashes and reject malformed 32-character values.
        # 3. Read the wordlist one line at a time, hash each candidate, and save matches.
        # 4. Stop early once every target is recovered.
        # 5. Return deterministic ``hash: word`` or ``hash: not found`` rows.
        raise NotImplementedError("Implement the md5HashCracker command")
