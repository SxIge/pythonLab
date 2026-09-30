"""Framework checks that remain valid while commands are implemented one by one."""

from __future__ import annotations

import io
import unittest

from c3tool.catalog import COMMAND_SPECS
from c3tool.cli import main
from c3tool.discovery import discover_command_specs
from c3tool.model import BaseCommand, CommandSpec
from c3tool.registry import CommandRegistry, MissingCommand


def invoke(arguments: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    code = main(arguments, stdout=stdout, stderr=stderr)
    return code, stdout.getvalue(), stderr.getvalue()


class TemplateTests(unittest.TestCase):
    def test_discovers_one_unique_spec_for_every_level(self) -> None:
        discovered = discover_command_specs()
        self.assertEqual(len(discovered), 32)
        self.assertEqual(len({item.name for item in discovered}), 32)
        self.assertEqual(COMMAND_SPECS, discovered)
        self.assertTrue(all(spec.handler.startswith("c3tool.commands.") for spec in discovered))

    def test_every_discovered_command_can_be_loaded(self) -> None:
        registry = CommandRegistry(COMMAND_SPECS)
        for spec in registry.specs:
            with self.subTest(command=spec.name):
                self.assertIsInstance(registry.load(spec.name), BaseCommand)

    def test_cli_help_starts_without_completed_commands(self) -> None:
        code, output, error = invoke([])
        self.assertEqual(code, 0)
        self.assertIn("python3 script.py <command>", output)
        self.assertEqual(error, "")

    def test_unknown_command_is_reported_cleanly(self) -> None:
        code, _output, error = invoke(["not-a-real-command"])
        self.assertEqual(code, 2)
        self.assertIn("Unknown command", error)

    def test_example_may_be_a_stub_or_a_completed_first_level(self) -> None:
        code, output, error = invoke(["example"])
        self.assertIn(code, {0, 3})
        if code == 0:
            self.assertEqual(output.strip(), "Hello World")
        else:
            self.assertIn("not implemented", error)

    def test_a_missing_implementation_does_not_break_registry_startup(self) -> None:
        broken = CommandSpec("missing", "None", "test", "missing", "unavailable", "does.not.exist:Missing")
        command = CommandRegistry([broken]).load("missing")
        self.assertIsInstance(command, MissingCommand)


if __name__ == "__main__":
    unittest.main()
