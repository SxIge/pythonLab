"""Print the current account name."""

import getpass

from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("whoami", "None", "Prints the current account.", "python3 script.py whoami", "The current username.", "c3tool.commands.system.whoami:WhoAmICommand", order=6)


class WhoAmICommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Require no arguments and return the current account name.
        # ``getpass`` provides a cross-platform way to find that name.
        raise NotImplementedError("Implement the whoami command")
