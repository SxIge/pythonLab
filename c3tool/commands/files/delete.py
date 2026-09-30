"""Delete one file or symbolic link without recursive removal."""

from c3tool.commands.files._paths import expand_path
from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("del", "<filepath>", "Deletes one file or symbolic link.", "python3 script.py del <filepath>", "A deletion confirmation.", "c3tool.commands.files.delete:DeleteCommand", order=4)


class DeleteCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Safely delete exactly one file or symbolic link.
        # 1. Require one path and resolve it with ``expand_path``.
        # 2. Refuse normal directories; this exercise must never delete trees.
        # 3. Report a missing path with CommandError.
        # 4. Unlink the target and return a confirmation.
        raise NotImplementedError("Implement the del command")
