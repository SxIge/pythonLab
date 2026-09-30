"""List one directory."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("ls", "<filepath, default current>", "Lists a directory.", "python3 script.py ls [filepath]", "Directory entries with type and size.", "c3tool.commands.files.list:ListCommand", order=8)


class ListCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: List either the supplied directory or ``context.cwd``.
        # 1. Accept zero or one argument and validate that the target is a folder.
        # 2. Sort entries consistently so output is predictable on every OS.
        # 3. Show a useful type, size, and name for each item.
        # 4. Return a clear message for an empty directory.
        raise NotImplementedError("Implement the ls command")
