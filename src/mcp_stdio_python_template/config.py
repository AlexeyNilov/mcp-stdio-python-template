from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_LOG_LEVEL = "INFO"
LOG_LEVELS = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}


@dataclass(frozen=True)
class Config:
    log_level: int


def load_config(env_file: Path | str = ".env") -> Config:
    dotenv_values = read_dotenv(Path(env_file))
    log_level_name = os.environ.get("LOG_LEVEL", dotenv_values.get("LOG_LEVEL", DEFAULT_LOG_LEVEL))
    return Config(log_level=parse_log_level(log_level_name))


def read_dotenv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key_value = parse_dotenv_line(line)
        if key_value is not None:
            key, value = key_value
            values[key] = value
    return values


def parse_dotenv_line(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None

    key, value = stripped.split("=", 1)
    return key.strip(), strip_quotes(value.strip())


def strip_quotes(value: str) -> str:
    if len(value) < 2:
        return value
    if value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_log_level(value: str) -> int:
    normalized = value.strip().upper()
    if normalized not in LOG_LEVELS:
        levels = ", ".join(LOG_LEVELS)
        raise ValueError(f"Unsupported LOG_LEVEL {value!r}; expected one of: {levels}")
    return LOG_LEVELS[normalized]
