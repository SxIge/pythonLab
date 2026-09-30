"""Recursively find partial filename matches."""

import os
from pathlib import Path

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("find", "<filename> <folder>", "Recursively finds partial filename matches.", "python3 script.py find <filename> <folder>", "Matching paths.", "c3tool.commands.files.find:FindCommand", order=20)


class FindCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Recursively search a folder for partial filename matches.
        # 1. Require a search fragment and a root folder.
        # 2. Validate the folder before walking it.
        # 3. Compare names case-insensitively and keep output deterministic.
        # 4. Return matching full paths or a helpful no-results message.
        raise NotImplementedError("Implement the find command")
