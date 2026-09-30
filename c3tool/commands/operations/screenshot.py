"""Capture a screenshot into the configured output folder."""

from datetime import datetime, timezone

from c3tool.model import BaseCommand, CommandError, CommandSpec, FeatureUnavailable, ToolContext

COMMAND_SPEC = CommandSpec("screenshot", "None", "Captures a screenshot in the output folder.", "python3 script.py screenshot", "The saved image path.", "c3tool.commands.operations.screenshot:ScreenshotCommand", order=29)


class ScreenshotCommand(BaseCommand):
    def run(self, args, context: ToolContext) -> str:
        # TODO: Capture the current graphical display with Pillow.
        # 1. Require no arguments and import ImageGrab inside this method.
        # 2. Ensure ``context.output_dir`` exists.
        # 3. Create a unique UTC timestamped PNG filename.
        # 4. Save the image and turn display/dependency failures into friendly errors.
        # 5. Return the saved path so the web runner can show the artifact.
        raise NotImplementedError("Implement the screenshot command")
