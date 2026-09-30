# C3T Python Tools — Practice Template

A cross-platform, beginner-friendly command toolkit for the Obsidian Runner course. The framework is complete, but each command intentionally contains a guided implementation exercise instead of its finished solution.

Every command now lives in its own file under a category folder:

```text
c3tool/commands/
  basics/example.py
  files/write_file.py
  network/ping.py
  system/process_kill.py
  ...one module per command
```

`script.py` asks `c3tool/discovery.py` to recursively walk those folders. Any module exposing a `COMMAND_SPEC` is registered automatically, so adding a command never requires editing a central command list. Implementations are loaded lazily, so one unfinished command does not prevent the CLI or unrelated completed commands from working.

Every unfinished `run()` method ends with a controlled `NotImplementedError`. The CLI catches it and prints a helpful message instead of a traceback. As soon as a student replaces that line with a working implementation, that command can run independently on the website.

## Setup

Python 3.11 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

The standard-library commands work without optional packages. `psutil` improves process, port, interface, mount, and host information; `Pillow` provides screenshots; `paramiko` provides the classroom SSH password-audit command.

## Usage

```bash
python3 script.py commands
python3 script.py example
python3 script.py hostinfo
python3 script.py portScan 127.0.0.1 8000
python3 script.py grep ./events.log "ERROR|WARN"
```

Until the `commands` exercise is implemented, command contracts can be read directly from each file's `COMMAND_SPEC` and from the corresponding website level.

## Completing a level

1. Open the matching file under `c3tool/commands/<category>/`.
2. Read its `COMMAND_SPEC` to understand the required inputs and output.
3. Follow the numbered TODO comments inside `run()`.
4. Replace the final `NotImplementedError` with your implementation.
5. Run that command locally, commit it, and push it to the GitHub repository used by Obsidian Runner.

The comments describe behavior rather than one mandatory solution. Students can choose their own loops, variables, formatting, and standard-library helpers as long as the command contract is satisfied.

Keep the small framework intact:

- `script.py`
- `c3tool/cli.py`
- `c3tool/discovery.py`
- `c3tool/model.py`
- `c3tool/registry.py`

Each exercise has exactly one implementation file in `c3tool/commands/<category>/`. During template creation, its implementation body was replaced with:

```python
raise NotImplementedError("Implement this command")
```

Do not remove `COMMAND_SPEC` or rename the command class. Those pieces allow recursive discovery and the website runner to locate the level. Remove or replace only the final `NotImplementedError` after implementing the method.

To add a brand-new command, copy one command module into any category folder, give it a unique `COMMAND_SPEC.name`, and point `COMMAND_SPEC.handler` at its command class. Recursive discovery handles the rest.

## Output folder

The `screenshot` command writes to `LAB_OUTPUT` when Obsidian Runner supplies it. Otherwise it writes to `./outputs`. Other commands write only to paths supplied on their command line.

## Template checks

```bash
python3 -m unittest discover -s tests -v
```

These checks verify discovery and CLI stability. They intentionally allow the `example` command to be either unfinished or correctly completed, so the template remains testable during incremental work.
