"""Hashing and SQLite data commands."""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

from c3tool.model import BaseCommand, CommandError, ToolContext, UsageError


def existing_file(value: str) -> Path:
    path = Path(value).expanduser().resolve(strict=False)
    if not path.is_file():
        raise CommandError(f"File not found: {path}")
    return path


class HashTextCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        if not args:
            raise UsageError("Usage: python3 script.py hashText <text>")
        text = " ".join(args)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()


class HashFileCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 1, "python3 script.py hashFile <file>")
        source = existing_file(args[0])
        digest = hashlib.sha256()
        # Streaming avoids loading large evidence files into memory at once.
        with source.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


class Md5HashCrackerCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 2, "python3 script.py md5HashCracker <hashFilePath> <wordlistFilePath>")
        hash_file = existing_file(args[0])
        wordlist_file = existing_file(args[1])
        targets = {
            line.strip().lower()
            for line in hash_file.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.strip()
        }
        invalid = sorted(value for value in targets if len(value) != 32 or any(char not in "0123456789abcdef" for char in value))
        if invalid:
            raise CommandError(f"Invalid MD5 digest in hash file: {invalid[0]}")

        recovered = {}
        with wordlist_file.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                word = line.rstrip("\r\n")
                digest = hashlib.md5(word.encode("utf-8"), usedforsecurity=False).hexdigest()
                if digest in targets and digest not in recovered:
                    recovered[digest] = word
                if len(recovered) == len(targets):
                    break
        rows = [f"{digest}: {recovered[digest]}" for digest in sorted(recovered)]
        missing = sorted(targets - recovered.keys())
        rows.extend(f"{digest}: not found" for digest in missing)
        return "\n".join(rows) if rows else "No hashes were supplied."


class SqliteCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        if len(args) < 2:
            raise UsageError("Usage: python3 script.py sqlite <filePath> <command>")
        database_path = Path(args[0]).expanduser().resolve(strict=False)
        command = " ".join(args[1:])
        database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = None
        try:
            connection = sqlite3.connect(database_path)
            with connection:
                cursor = connection.execute(command)
                if cursor.description:
                    columns = [column[0] for column in cursor.description]
                    rows = cursor.fetchall()
                    widths = [len(column) for column in columns]
                    for row in rows:
                        for index, value in enumerate(row):
                            widths[index] = max(widths[index], len(str(value)))
                    header = " | ".join(column.ljust(widths[index]) for index, column in enumerate(columns))
                    divider = "-+-".join("-" * width for width in widths)
                    body = [" | ".join(str(value).ljust(widths[index]) for index, value in enumerate(row)) for row in rows]
                    return "\n".join((header, divider, *body))
                connection.commit()
                return f"Statement complete. Rows affected: {cursor.rowcount}"
        except sqlite3.Error as error:
            raise CommandError(f"SQLite error: {error}") from error
        finally:
            # A sqlite connection context commits or rolls back but does not
            # close the handle. Explicit close matters on Windows, where an
            # open handle prevents the database from being moved or deleted.
            if connection is not None:
                connection.close()
