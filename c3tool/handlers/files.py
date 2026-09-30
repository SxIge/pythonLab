"""Filesystem commands implemented with pathlib for Windows/Linux parity."""

from __future__ import annotations

import os
import re
import stat
from pathlib import Path

from c3tool.model import BaseCommand, CommandError, ToolContext, UsageError


def expand_path(value: str, context: ToolContext) -> Path:
    """Resolve user paths without requiring that they already exist."""

    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = context.cwd / candidate
    return candidate.resolve(strict=False)


def require_existing_file(value: str, context: ToolContext) -> Path:
    path = expand_path(value, context)
    if not path.is_file():
        raise CommandError(f"File not found: {path}")
    return path


class WriteFileCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        if len(args) < 2:
            raise UsageError("Usage: python3 script.py writeFile <filename> <text>")
        destination = expand_path(args[0], context)
        destination.parent.mkdir(parents=True, exist_ok=True)
        text = " ".join(args[1:])
        destination.write_text(text, encoding="utf-8")
        return f"Wrote {len(text.encode('utf-8'))} bytes to {destination}"


class CatCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py cat <filepath>")
        return require_existing_file(args[0], context).read_text(encoding="utf-8", errors="replace")


class DeleteCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py del <filepath>")
        target = expand_path(args[0], context)
        # Deliberately avoid recursive deletion. A training command should not
        # turn one mistyped folder into a broad filesystem wipe.
        if target.is_dir() and not target.is_symlink():
            raise CommandError("del removes files or symbolic links, not directories")
        if not target.exists() and not target.is_symlink():
            raise CommandError(f"Path not found: {target}")
        target.unlink()
        return f"Deleted {target}"


class PwdCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py pwd")
        return str(context.cwd)


class ListCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_range(args, 0, 1, "python3 script.py ls [filepath]")
        target = expand_path(args[0], context) if args else context.cwd
        if not target.is_dir():
            raise CommandError(f"Directory not found: {target}")
        rows = []
        for item in sorted(target.iterdir(), key=lambda path: path.name.lower()):
            kind = "dir" if item.is_dir() else "link" if item.is_symlink() else "file"
            size = "-" if item.is_dir() else str(item.stat().st_size)
            rows.append(f"{kind:4} {size:>10}  {item.name}")
        return "\n".join(rows) if rows else "(empty directory)"


class FindCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 2, "python3 script.py find <filename> <folder>")
        needle = args[0].casefold()
        root = expand_path(args[1], context)
        if not root.is_dir():
            raise CommandError(f"Directory not found: {root}")
        matches = []
        for current_root, directory_names, file_names in os.walk(root):
            directory_names.sort(key=str.casefold)
            for file_name in sorted(file_names, key=str.casefold):
                if needle in file_name.casefold():
                    matches.append(str(Path(current_root) / file_name))
        return "\n".join(matches) if matches else "No matching files found."


class GrepCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 2, "python3 script.py grep <filename> <regex>")
        source = require_existing_file(args[0], context)
        try:
            pattern = re.compile(args[1])
        except re.error as error:
            raise CommandError(f"Invalid regular expression: {error}") from error
        matches = []
        with source.open("r", encoding="utf-8", errors="replace") as handle:
            for line_number, line in enumerate(handle, start=1):
                if pattern.search(line):
                    matches.append(f"{line_number}: {line.rstrip()}")
        return "\n".join(matches) if matches else "No matches found."


class PermissionsCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py permissions <file>")
        target = expand_path(args[0], context)
        if not target.exists():
            raise CommandError(f"Path not found: {target}")
        details = target.stat()
        rows = [
            f"Path: {target}",
            f"Mode: {stat.filemode(details.st_mode)}",
            f"Numeric mode: {oct(stat.S_IMODE(details.st_mode))}",
        ]
        if os.name == "posix":
            import grp
            import pwd

            rows.append(f"Owner: {pwd.getpwuid(details.st_uid).pw_name} ({details.st_uid})")
            rows.append(f"Group: {grp.getgrgid(details.st_gid).gr_name} ({details.st_gid})")
        else:
            rows.append(f"Owner UID: {details.st_uid}")
        return "\n".join(rows)
