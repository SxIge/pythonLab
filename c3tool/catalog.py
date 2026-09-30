"""Stable catalog for every supported C3T command.

Keep this file in the student edition. Even if a handler is removed, the
``commands`` command can still describe the intended contract from this data.
"""

from c3tool.model import CommandSpec


def spec(name: str, args: str, description: str, usage: str, expected: str, handler: str) -> CommandSpec:
    return CommandSpec(name, args, description, usage, expected, handler)


COMMAND_SPECS = (
    spec("example", "None", "Prints hello world.", "python3 script.py example", "Hello World", "c3tool.handlers.basics:ExampleCommand"),
    spec("writeFile", "<filename> <text>", "Writes text to a file.", "python3 script.py writeFile <filename> <text>", "A confirmation containing the written path.", "c3tool.handlers.files:WriteFileCommand"),
    spec("cat", "<filepath>", "Prints a text file.", "python3 script.py cat <filepath>", "The complete file contents.", "c3tool.handlers.files:CatCommand"),
    spec("del", "<filepath>", "Deletes one file or symbolic link.", "python3 script.py del <filepath>", "A deletion confirmation.", "c3tool.handlers.files:DeleteCommand"),
    spec("commands", "None", "Lists commands, descriptions, arguments, usage, and expected output.", "python3 script.py commands", "The complete command reference.", "c3tool.core_commands:CommandsCommand"),
    spec("whoami", "None", "Prints the current account.", "python3 script.py whoami", "The current username.", "c3tool.handlers.system:WhoAmICommand"),
    spec("pwd", "None", "Prints the current working directory.", "python3 script.py pwd", "An absolute path.", "c3tool.handlers.files:PwdCommand"),
    spec("ls", "<filepath, default current>", "Lists a directory.", "python3 script.py ls [filepath]", "Directory entries with type and size.", "c3tool.handlers.files:ListCommand"),
    spec("hostname", "None", "Prints the system hostname.", "python3 script.py hostname", "The hostname.", "c3tool.handlers.system:HostnameCommand"),
    spec("hostinfo", "None", "Shows operating system and hardware information.", "python3 script.py hostinfo", "A structured host summary.", "c3tool.handlers.system:HostInfoCommand"),
    spec("interfaces", "None", "Lists network interfaces and addresses.", "python3 script.py interfaces", "Interface and address rows.", "c3tool.handlers.system:InterfacesCommand"),
    spec("processes", "None", "Lists running processes.", "python3 script.py processes", "PID, user, name, and command rows.", "c3tool.handlers.system:ProcessesCommand"),
    spec("processKill", "<PID>", "Terminates a process by PID.", "python3 script.py processKill <PID>", "A termination confirmation.", "c3tool.handlers.system:ProcessKillCommand"),
    spec("ping", "<IP or hostname>", "Tests whether a host responds to ping.", "python3 script.py ping <IP>", "An online or offline result.", "c3tool.handlers.network:PingCommand"),
    spec("ports", "None", "Lists local listening ports and services.", "python3 script.py ports", "Listening endpoints and service details.", "c3tool.handlers.network:PortsCommand"),
    spec("portScan", "<host> <port>", "Tests one TCP host and port.", "python3 script.py portScan <host> <port>", "An open or closed result.", "c3tool.handlers.network:PortScanCommand"),
    spec("users", "None", "Lists local user accounts.", "python3 script.py users", "Local account rows.", "c3tool.handlers.system:UsersCommand"),
    spec("groups", "None", "Lists current account group memberships.", "python3 script.py groups", "Group names or platform group rows.", "c3tool.handlers.system:GroupsCommand"),
    spec("env", "None", "Lists environment variables.", "python3 script.py env", "Sorted NAME=value rows.", "c3tool.handlers.system:EnvironmentCommand"),
    spec("find", "<filename> <folder>", "Recursively finds partial filename matches.", "python3 script.py find <filename> <folder>", "Matching paths.", "c3tool.handlers.files:FindCommand"),
    spec("grep", "<filename> <regex>", "Shows matching lines and line numbers.", "python3 script.py grep <filename> <regex>", "line_number: matching text rows.", "c3tool.handlers.files:GrepCommand"),
    spec("hashText", "<text>", "Calculates a SHA-256 text digest.", "python3 script.py hashText <text>", "A SHA-256 hexadecimal digest.", "c3tool.handlers.data:HashTextCommand"),
    spec("hashFile", "<file>", "Calculates a streaming SHA-256 file digest.", "python3 script.py hashFile <file>", "A SHA-256 hexadecimal digest.", "c3tool.handlers.data:HashFileCommand"),
    spec("sshCracker", "<user:IP:port> <passwordFile>", "Audits a lab SSH account using a password list.", "python3 script.py sshCracker <user:IP:port> <passwordFile>", "The accepted password or a not-found result.", "c3tool.handlers.network:SshCrackerCommand"),
    spec("mounts", "None", "Shows mounted filesystems or logical drives.", "python3 script.py mounts", "Mount, device, filesystem, and usage rows.", "c3tool.handlers.system:MountsCommand"),
    spec("permissions", "<file>", "Shows permissions and ownership for a path.", "python3 script.py permissions <file>", "Numeric mode, symbolic mode, owner, and group.", "c3tool.handlers.files:PermissionsCommand"),
    spec("exec", "<command>", "Runs a command in Bash or PowerShell.", "python3 script.py exec <command>", "Captured stdout, stderr, and exit code.", "c3tool.handlers.operations:ExecCommand"),
    spec("download", "<source URL> [pathToSave]", "Downloads a URL to a local file.", "python3 script.py download <sourceURL> [pathToSave]", "A confirmation containing the saved path.", "c3tool.handlers.network:DownloadCommand"),
    spec("screenshot", "None", "Captures a screenshot in the output folder.", "python3 script.py screenshot", "The saved image path.", "c3tool.handlers.operations:ScreenshotCommand"),
    spec("md5HashCracker", "<hashFilePath> <wordlistFilePath>", "Recovers classroom MD5 values using a wordlist.", "python3 script.py md5HashCracker <hashFilePath> <wordlistFilePath>", "Recovered hash-to-word mappings.", "c3tool.handlers.data:Md5HashCrackerCommand"),
    spec("sqlite", "<filePath> <command>", "Runs a SQLite statement.", "python3 script.py sqlite <filePath> <command>", "Query columns and rows or an affected-row count.", "c3tool.handlers.data:SqliteCommand"),
    spec("portConnect", "<host:port>", "Connects to a TCP port and prints received data.", "python3 script.py portConnect <host:port>", "The received banner or a no-data message.", "c3tool.handlers.network:PortConnectCommand"),
)
