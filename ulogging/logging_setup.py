from __future__ import annotations

import logging
import logging.config
import os
import pprint
from dataclasses import is_dataclass, asdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Dict, List, cast
from collections.abc import Iterator, Generator

from uconstants.logging import (
    LOG_LINE_FORMAT,
    LOG_DATE_FORMAT,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
    DEFAULTS,
    DEFAULT_CHANNELS,
    DEFAULT_LOG_NAME,
    DEFAULT_BASE_LOGGER_NAME,
    default_logs_dir,
    ChannelConfigOptional,
)

# --------------------------------------------------------------------------------------
# Logs dir resolution
# --------------------------------------------------------------------------------------

def _resolve_logs_dir() -> Path:
    return default_logs_dir()

# --------------------------------------------------------------------------------------
# Formatting / serialization
# --------------------------------------------------------------------------------------

class UniformFormatter(logging.Formatter):
    """Formatter that prints one-letter level code via %(levelname).1s in LOG_LINE_FORMAT."""
    def __init__(self) -> None:
        super().__init__(fmt=LOG_LINE_FORMAT, datefmt=LOG_DATE_FORMAT)

class PrettySerializer:
    def __init__(
        self,
        width: int = DEFAULTS.pp_width,
        compact: bool = DEFAULTS.pp_compact,
        sort_dicts: bool = DEFAULTS.pp_sort_dicts,
        log_exhaustibles: bool = DEFAULTS.log_exhaustibles,
    ):
        self.width = width
        self.compact = compact
        self.sort_dicts = sort_dicts
        self.log_exhaustibles = log_exhaustibles

    def _is_nonstring_iterable(self, obj: object) -> bool:
        if isinstance(obj, (str, bytes, bytearray)):
            return False
        if isinstance(obj, Mapping):
            return False
        try:
            iter(obj)  # type: ignore[call-overload]
        except Exception:
            return False
        return True

    @staticmethod
    def is_exhaustible(obj: object) -> bool:
        if isinstance(obj, (str, bytes, bytearray)):
            return False
        if isinstance(obj, (Iterator, Generator)):
            return True
        if not hasattr(obj, "__iter__"):
            return False
        it = iter(cast(Iterable[Any], obj))
        return it is obj

    def _normalize(self, obj: object) -> object:
        # Only dataclass instances (not classes)
        if is_dataclass(obj) and not isinstance(obj, type):
            # asdict expects a dataclass instance
            return asdict(obj)  # type: ignore[arg-type]

        if isinstance(obj, set):
            s = cast(set[Any], obj)
            return sorted(map(repr, s))
        
        if isinstance(obj, tuple):
            return list(cast(tuple[Any, ...], obj))

        if self._is_nonstring_iterable(obj):
            if self.is_exhaustible(obj):
                if not self.log_exhaustibles:
                    name = type(obj).__name__
                    return f"<{name} (exhaustible, not logged)>"
                try:
                    it = cast(Iterable[Any], obj)
                    return list(it)
                except Exception:
                    # fall through to plain string repr if conversion failed
                    return str(obj)
            # Non-exhaustible iterables (like tuple, list, set) should be processed normally

        return obj

    def _typename(self, obj: object) -> str:
        cls: type = type(obj)
        module = getattr(cls, "__module__", "builtins")
        name = getattr(cls, "__name__", cls.__name__)
        return f"{module}.{name}"

    def dumps(self, obj: object, with_types: bool = False) -> str:
        norm = self._normalize(obj)
        text = pprint.pformat(
            norm,
            width=self.width,
            compact=self.compact,
            sort_dicts=self.sort_dicts,
        )
        if with_types:
            text = f"{text}  (type={self._typename(obj)})"
        return text

# --------------------------------------------------------------------------------------
# Fluent API
# --------------------------------------------------------------------------------------

class FluentChannelLogger:
    """Fluent API: logger.channel('name').info(...).debug(...).error(...)."""
    def __init__(self, logger: logging.Logger, *, pretty: bool = False, with_types: bool = False, stack_on_error: bool = False):
        self._logger: logging.Logger = logger
        self._pretty: bool = pretty
        self._with_types: bool = with_types
        self._stack_on_error_default: bool = stack_on_error
        self._ser = PrettySerializer(log_exhaustibles=pretty)

    def _fmt(self, msg_or_obj: Any, with_types: Optional[bool]) -> str:
        use_types = with_types if with_types is not None else self._with_types
        if self._pretty or use_types:
            return self._ser.dumps(msg_or_obj, use_types)
        return str(msg_or_obj)

    def debug(self, msg_or_obj: Any, *args: Any, with_types: Optional[bool] = None, **kwargs: Any) -> "FluentChannelLogger":
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug(self._fmt(msg_or_obj, with_types), *args, stacklevel=2, **kwargs)
        return self

    def info(self, msg_or_obj: Any, *args: Any, with_types: Optional[bool] = None, **kwargs: Any) -> "FluentChannelLogger":
        if self._logger.isEnabledFor(logging.INFO):
            self._logger.info(self._fmt(msg_or_obj, with_types), *args, stacklevel=2, **kwargs)
        return self

    def warning(self, msg_or_obj: Any, *args: Any, with_types: Optional[bool] = None, **kwargs: Any) -> "FluentChannelLogger":
        if self._logger.isEnabledFor(logging.WARNING):
            self._logger.warning(self._fmt(msg_or_obj, with_types), *args, stacklevel=2, **kwargs)
        return self

    def error(self, msg_or_obj: Any, *args: Any, with_types: Optional[bool] = None, exc: BaseException | None = None, **kwargs: Any) -> "FluentChannelLogger":
        if isinstance(msg_or_obj, BaseException) and exc is None:
            exc = msg_or_obj
            msg = repr(msg_or_obj)
        else:
            msg = self._fmt(msg_or_obj, with_types)
        self._logger.error(msg, *args, stacklevel=2, exc_info=exc if (exc or self._stack_on_error_default) else None, **kwargs)
        return self

    def critical(self, msg_or_obj: Any, *args: Any, with_types: Optional[bool] = None, exc: BaseException | None = None, **kwargs: Any) -> "FluentChannelLogger":
        msg = self._fmt(msg_or_obj, with_types)
        self._logger.critical(msg, *args, stacklevel=2, exc_info=exc if exc else None, **kwargs)
        return self

class ChannelRouter:
    """get_logger(...).channel('name') -> FluentChannelLogger"""
    def __init__(self, base_name: str, *, pretty: bool = False, with_types: bool = False, channel_specs: Dict[str, ChannelConfigOptional] | None = None):
        self._base: str = base_name
        self._pretty: bool = pretty
        self._with_types: bool = with_types
        self._specs: Dict[str, ChannelConfigOptional] = channel_specs or {}

    def channel(self, name: str) -> FluentChannelLogger:
        lg_name = f"{self._base}.channel.{name}"
        lg = logging.getLogger(lg_name)
        spec = self._specs.get(name, {"filename": f"{name}.log", "level": "INFO"})
        return FluentChannelLogger(
            lg,
            pretty=self._pretty,
            with_types=self._with_types,
            stack_on_error=bool(spec.get("stack_on_error", False)),
        )

# --------------------------------------------------------------------------------------
# Public API
# --------------------------------------------------------------------------------------

_channels_runtime: Dict[str, ChannelConfigOptional] = {}
_base_logger_name: str = DEFAULT_BASE_LOGGER_NAME  # configurable via setup_logging(base_name=...)

def get_logger(name: str | None = None, *, pretty: bool = False, with_types: bool = False) -> ChannelRouter:
    """
    Returns a ChannelRouter bound to `name` or to the globally configured base name.
    """
    base = name or _base_logger_name
    return ChannelRouter(base, pretty=pretty, with_types=with_types, channel_specs=_channels_runtime)

def setup_logging(
    *,
    base_name: str = DEFAULT_BASE_LOGGER_NAME,
    logs_dir: Path | None = None,
    root_level: str | None = None,
    enable_console: bool | None = None,
    console_level: str | None = None,
    file_level: str | None = None,
    console_for_all_channels: bool = False,
    channels: Dict[str, ChannelConfigOptional] | None = None,
) -> None:
    """
    Initialize logging:
      - per-channel rotating files
      - optional console mirroring (all channels or base only)
      - a base logger (non-channeled) writing to DEFAULT_LOG_NAME
    """
    global _channels_runtime, _base_logger_name

    _base_logger_name = base_name

    logs_dir = logs_dir or _resolve_logs_dir()
    logs_dir.mkdir(parents=True, exist_ok=True)

    root_level = (root_level or os.getenv("APP_LOG_LEVEL") or DEFAULTS.root_level).upper()
    console_level = (console_level or os.getenv("APP_LOG_CONSOLE_LEVEL") or DEFAULTS.console_level).upper()
    file_level = (file_level or os.getenv("APP_LOG_FILE_LEVEL") or DEFAULTS.file_level).upper()

    if enable_console is None:
        enable_console = (os.getenv("APP_LOG_ENABLE_CONSOLE") or "1") in {"1", "true", "yes", "on"}
    if os.getenv("APP_LOG_CONSOLE_FOR_ALL") in {"1", "true", "yes", "on"}:
        console_for_all_channels = True

    # Handlers registry
    handlers: Dict[str, Dict[str, Any]] = {}

    # Console handler (optional)
    if enable_console:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "level": console_level,
            "formatter": "uniform",
        }

    # Default file handler for the base logger (non-channeled logs)
    handlers["file_default"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "level": file_level,
        "formatter": "uniform",
        "filename": str(logs_dir / DEFAULT_LOG_NAME),
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
        "encoding": "utf-8",
    }

    # Channels (per-file)
    channels = channels or DEFAULT_CHANNELS
    _channels_runtime = channels

    channel_loggers: Dict[str, Dict[str, Any]] = {}
    for ch_name, spec in channels.items():
        filename = spec.get("filename", f"{ch_name}.log")
        level = spec.get("level", "INFO").upper()
        handler_id = f"file_channel_{ch_name}"

        handlers[handler_id] = {
            "class": "logging.handlers.RotatingFileHandler",
            "level": level,
            "formatter": "uniform",
            "filename": str(logs_dir / filename),
            "maxBytes": LOG_MAX_BYTES,
            "backupCount": LOG_BACKUP_COUNT,
            "encoding": "utf-8",
        }

        ch_logger_name = f"{_base_logger_name}.channel.{ch_name}"
        ch_handlers: List[str] = [handler_id]
        if enable_console and console_for_all_channels:
            ch_handlers.append("console")

        channel_loggers[ch_logger_name] = {
            "level": level,
            "handlers": ch_handlers,
            "propagate": False,
        }

    # Root: only console if explicitly requested "for all"
    root_handlers: List[str] = []
    if enable_console and console_for_all_channels:
        root_handlers.append("console")

    # Base logger (non-channeled) -> default.log (+ optional console)
    base_handlers: List[str] = ["file_default"]
    if enable_console and not console_for_all_channels:
        base_handlers.append("console")

    base_logger_cfg = {
        "level": root_level,
        "handlers": base_handlers,
        "propagate": False,
    }

    # Final dictConfig
    config: Dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {"uniform": {"()": UniformFormatter}},
        "handlers": handlers,
        "root": {"level": root_level, "handlers": root_handlers},
        "loggers": {
            **channel_loggers,
            _base_logger_name: base_logger_cfg,  # base logger bound to default.log
        },
    }
    logging.config.dictConfig(config)