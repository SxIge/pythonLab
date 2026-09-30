"""Execute a SQLite statement and format its result."""

import sqlite3
from pathlib import Path

from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext, UsageError

COMMAND_SPEC = CommandSpec("sqlite", "<filePath> <command>", "Runs a SQLite statement.", "python3 script.py sqlite <filePath> <command>", "Query columns and rows or an affected-row count.", "c3tool.commands.data.sqlite:SqliteCommand", order=31)


class SqliteCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Execute one SQLite statement against the supplied database.
        # 1. Require a database path plus a command; join multi-word SQL arguments.
        # 2. Open the database with a context that commits or rolls back safely.
        # 3. Format query columns/rows as a readable table.
        # 4. For non-query statements, report the affected-row count.
        # 5. Convert sqlite errors to CommandError and always close the connection.
        raise NotImplementedError("Implement the sqlite command")
