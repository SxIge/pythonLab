"""Download an HTTP or HTTPS resource."""

import urllib.parse
import urllib.request
from pathlib import Path

from c3tool.model import BaseCommand, CommandError, CommandSpec, ToolContext

COMMAND_SPEC = CommandSpec("download", "<source URL> [pathToSave]", "Downloads a URL to a local file.", "python3 script.py download <sourceURL> [pathToSave]", "A confirmation containing the saved path.", "c3tool.commands.network.download:DownloadCommand", order=28)


class DownloadCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Download one HTTP/HTTPS URL safely.
        # 1. Accept a URL plus an optional destination path.
        # 2. Reject non-web schemes and derive a useful default filename.
        # 3. Stream bytes in chunks instead of loading the whole response.
        # 4. Remove a partial file if the transfer fails.
        # 5. Return the byte count and final path.
        raise NotImplementedError("Implement the download command")
