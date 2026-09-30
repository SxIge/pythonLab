"""Print the first-course hello-world result."""

from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("example", "None", "Prints hello world.", "python3 script.py example", "Hello World", "c3tool.commands.basics.example:ExampleCommand", order=1)


class ExampleCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: This is the smallest exercise in the course.
        # 1. Reject unexpected arguments with ``self.require_count``.
        # 2. Return the exact greeting described by COMMAND_SPEC.
        # Replace this final line when your implementation is ready.
        raise NotImplementedError("Implement the example command")
