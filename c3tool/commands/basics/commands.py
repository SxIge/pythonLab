"""Render the reference for all recursively discovered commands."""

from c3tool.model import BaseCommand, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("commands", "None", "Lists commands, descriptions, arguments, usage, and expected output.", "python3 script.py commands", "The complete command reference.", "c3tool.commands.basics.commands:CommandsCommand", order=5)


class CommandsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
         
        # TODO: Build a readable reference from ``context.registry.specs``.
        # 1. This command accepts no arguments.
        # 2. Loop over every discovered CommandSpec.
        # 3. Include its name, description, args, usage, and expected output.
        # 4. Return one string; blank lines between commands are easy to read.
         output_lines = []
         for spec in context.registry.specs:
                
                    output_lines.append(f"Command: {spec.name}")
                    output_lines.append(f"Description: {spec.description}")
                    output_lines.append(f"Arguments: {spec.args}")
                    output_lines.append(f"Usage: {spec.usage}")
                    output_lines.append(f"Expected Output: {spec.expected_output}")
                    output_lines.append("")  # Blank line between commands for readability

         return "\n".join(output_lines)
