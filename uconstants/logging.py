from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict

from uconstants.paths import LOGS_SUBDIR, USER_DATA_DIRNAME

DEFAULT_BASE_LOGGER_NAME = "app"
DEFAULT_LOG_NAME = "default.log"

LOG_LINE_FORMAT = "[%(asctime)s : %(filename)s : %(lineno)d : %(levelname).1s]: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 5
PP_WIDTH = 120
PP_COMPACT = True
PP_SORT_DICTS = False

DEFAULT_ROOT_LEVEL = "INFO"
DEFAULT_CONSOLE_LEVEL = "WARNING"
DEFAULT_FILE_LEVEL = "INFO"


class ChannelConfig(TypedDict):
    filename: str
    level: str


class ChannelConfigOptional(ChannelConfig, total=False):
    stack_on_error: bool


# Levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
DEFAULT_CHANNELS: dict[str, ChannelConfigOptional] = {
    "exceptions": {"filename": "exceptions.log", "level": "ERROR", "stack_on_error": True},
    "success": {"filename": "success.log", "level": "INFO"},
}


@dataclass(frozen=True)
class LoggingDefaults:
    root_level: str = DEFAULT_ROOT_LEVEL
    console_level: str = DEFAULT_CONSOLE_LEVEL
    file_level: str = DEFAULT_FILE_LEVEL
    pp_width: int = PP_WIDTH
    pp_compact: bool = PP_COMPACT
    pp_sort_dicts: bool = PP_SORT_DICTS
    log_exhaustibles: bool = False


DEFAULTS = LoggingDefaults()


def default_logs_dir() -> Path:
    try:
        from gramps.gen.const import USER_DATA  # pylint: disable=import-outside-toplevel

        root = Path(USER_DATA)
    except Exception:
        root = Path(os.path.expanduser("~"))
    return root.joinpath(USER_DATA_DIRNAME, LOGS_SUBDIR)
