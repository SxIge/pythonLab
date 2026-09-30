# C3T Python Tools

A cross-platform Python command toolkit used as the complete reference implementation for the Obsidian Runner course.

The CLI is intentionally split into two layers:

- `c3tool/catalog.py` is the permanent command contract. It describes every command even when an implementation is missing.
- `c3tool/handlers/` contains the working implementations that can later be replaced with student stubs.

Handlers are loaded only when their command runs. Removing an entire handler module therefore does not stop `script.py`, `commands`, or unrelated commands from working. A removed or unfinished handler produces a clear `command unavailable` message instead of a traceback.

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

Run `python3 script.py commands` for the complete command, argument, usage, and expected-output reference.

## Creating the student edition

Keep these files intact:

- `script.py`
- `c3tool/catalog.py`
- `c3tool/cli.py`
- `c3tool/core_commands.py`
- `c3tool/model.py`
- `c3tool/registry.py`

Replace selected handler class bodies in `c3tool/handlers/` with:

```python
raise NotImplementedError("Rebuild this command")
```

You can also remove a handler module completely. The CLI will still start, list every command, and run all remaining implementations.

## Output folder

The `screenshot` command writes to `LAB_OUTPUT` when Obsidian Runner supplies it. Otherwise it writes to `./outputs`. Other commands write only to paths supplied on their command line.

## Tests

```bash
python3 -m unittest discover -s tests -v
```
