"""Platform command execution and screenshot collection."""

from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime, timezone

from c3tool.model import BaseCommand, CommandError, FeatureUnavailable, ToolContext, UsageError


class ExecCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        if not args:
            raise UsageError("Usage: python3 script.py exec <command>")
        command = " ".join(args)
        if os.name == "nt":
            executable = shutil.which("pwsh") or shutil.which("powershell")
            if not executable:
                raise FeatureUnavailable("PowerShell was not found")
            invocation = [executable, "-NoProfile", "-NonInteractive", "-Command", command]
        else:
            bash = shutil.which("bash") or "/bin/bash"
            invocation = [bash, "-lc", command]
        try:
            result = subprocess.run(invocation, capture_output=True, text=True, timeout=60, check=False)
        except subprocess.TimeoutExpired as error:
            raise CommandError("Command exceeded the 60-second timeout") from error
        except OSError as error:
            raise CommandError(f"Could not start the platform shell: {error}") from error

        sections = []
        if result.stdout:
            sections.append(result.stdout.rstrip())
        if result.stderr:
            sections.append(f"[stderr]\n{result.stderr.rstrip()}")
        sections.append(f"[exit code: {result.returncode}]")
        return "\n".join(sections)


class ScreenshotCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        self.require_count(args, 0, "python3 script.py screenshot")
        try:
            from PIL import ImageGrab
        except ImportError as error:
            raise FeatureUnavailable("Install Pillow to use screenshot") from error

        context.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        destination = context.output_dir / f"screenshot-{timestamp}.png"
        try:
            image = ImageGrab.grab(all_screens=True)
            image.save(destination, format="PNG")
        except Exception as error:
            raise CommandError(
                "Screenshot capture failed. Linux runners need an active graphical display: "
                f"{error}"
            ) from error
        return f"Screenshot saved to {destination}"
