"""Write text to a file."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandSpec, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("writeFile", "<filename> <text>", "Writes text to a file.", "python3 script.py writeFile <filename> <text>", "A confirmation containing the written path.", "c3tool.commands.files.write_file:WriteFileCommand", order=2)


class WriteFileCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Write user-provided text to a path.
        # 1. Require a filename plus at least one text argument.
        # 2. Resolve the filename with ``expand_path``.
        # 3. Join all remaining arguments so spaces in the text are preserved.
        # 4. Create missing parent folders, write UTF-8 text, and confirm the path.
        raise NotImplementedError("Implement the writeFile command")
