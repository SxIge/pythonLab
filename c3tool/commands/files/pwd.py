"""Print the current working directory."""

from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("pwd", "None", "Prints the current working directory.", "python3 script.py pwd", "An absolute path.", "c3tool.commands.files.pwd:PwdCommand", order=7)


class PwdCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # Require no arguments and return the resolved working directory as text.
        # The context already contains an absolute, resolved working directory.
        if args:
            raise ValueError("pwd does not accept any arguments.")
        return str(context.cwd)
