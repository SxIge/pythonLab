"""Shared host and port parsing helpers."""

from c3tool.model import UsageError


def parse_port(value: str) -> int:
    try:
        port = int(value)
    except ValueError as error:
        raise UsageError("Port must be an integer") from error
    if not 1 <= port <= 65535:
        raise UsageError("Port must be between 1 and 65535")
    return port


def parse_host_port(value: str) -> tuple[str, int]:
    if value.startswith("[") and "]:" in value:
        host, port_text = value[1:].rsplit("]:", 1)
    elif ":" in value:
        host, port_text = value.rsplit(":", 1)
    else:
        raise UsageError("Expected host:port")
    if not host:
        raise UsageError("Host cannot be empty")
    return host, parse_port(port_text)
