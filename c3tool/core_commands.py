"""Framework-owned commands that remain in every student edition."""

from c3tool.model import BaseCommand, ToolContext


class CommandsCommand(BaseCommand):
    """Render contracts from the stable catalog, not imported handlers."""

    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py commands")
        sections = []
        for spec in context.registry.specs:
            sections.append(
                "\n".join(
                    (
                        spec.name,
                        f"  Description: {spec.description}",
                        f"  Args: {spec.args}",
                        f"  Usage: {spec.usage}",
                        f"  Expected: {spec.expected_output}",
                    )
                )
            )
        return "\n\n".join(sections)
