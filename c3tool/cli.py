"""Command-line dispatcher with concise, user-facing failure handling."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Sequence, TextIO

from c3tool.discovery import discover_command_specs
from c3tool.model import CommandError, FeatureUnavailable, ToolContext
from c3tool.registry import CommandRegistry


def main(
    argv: Sequence[str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    registry: CommandRegistry | None = None,
) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    registry = registry or CommandRegistry(discover_command_specs())

    if not args or args[0] in {"-h", "--help", "help"}:
        print("Usage: python3 script.py <command> [arguments]", file=stdout)
        print("Run 'python3 script.py commands' for the complete reference.", file=stdout)
        return 0

    command_name, command_args = args[0], args[1:]
    command = registry.load(command_name)
    if command is None:
        suggestions = registry.suggestions(command_name)
        suffix = f" Did you mean: {', '.join(suggestions)}?" if suggestions else ""
        print(f"Unknown command: {command_name}.{suffix}", file=stderr)
        return 2

    output_dir = Path(os.environ.get("LAB_OUTPUT", Path.cwd() / "outputs")).expanduser().resolve()
    context = ToolContext(cwd=Path.cwd().resolve(), output_dir=output_dir, registry=registry)

    try:
        result = command.run(command_args, context)
        if result:
            print(result, file=stdout)
        return 0
    except NotImplementedError as error:
        print(f"Command '{command_name}' is not implemented: {error}", file=stderr)
        return 3
    except FeatureUnavailable as error:
        print(str(error), file=stderr)
        return 3
    except CommandError as error:
        print(str(error), file=stderr)
        return 2
    except KeyboardInterrupt:
        print("Interrupted.", file=stderr)
        return 130
    except Exception as error:
        print(f"Command '{command_name}' failed: {type(error).__name__}: {error}", file=stderr)
        return 1
