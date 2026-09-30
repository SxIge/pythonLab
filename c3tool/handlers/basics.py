"""Foundational CLI commands."""

from c3tool.model import BaseCommand, ToolContext


class ExampleCommand(BaseCommand):
    """The smallest possible command and the first classroom exercise."""

    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py example")
        return "Hello World"


