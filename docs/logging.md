# Logging Library — Practical Guide

A practical, example‑driven guide to initialize, configure, and use the logging library. The library centers on **channels** (named, per‑file logs), a **fluent API**, and optional **pretty serialization** for structured payloads.

> All names in this guide are neutral (project‑agnostic).

---

## TL;DR

```python
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS

setup_logging(channels=DEFAULT_CHANNELS, enable_console=True, console_for_all_channels=True)
logger = get_logger()  # bound to the configured base name

logger.channel("success").info("Initialization OK")
try:
    raise RuntimeError("boom")
except RuntimeError as e:
    logger.channel("exceptions").error("Operation failed", exc=e)
```

---

## What you get

- **Channel loggers** → each channel writes to its own rotating file.
- **Base logger** → a root/default file for non‑channeled logs.
- **Console mirroring** (off, all, or selective).
- **Fluent API**: `logger.channel("name").info(...).error(..., exc=e)`.
- **Pretty serialization** for dicts, dataclasses, sets, iterables, etc.
- Sensible **defaults** you can override via parameters or environment variables.

---

## Key imports

```python
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS, DEFAULTS
```

---

## Defaults (from `uconstants.logging`)

- Base logger name: `DEFAULT_BASE_LOGGER_NAME = "app"`
- Default base file: `DEFAULT_LOG_NAME = "default.log"`
- Line format: `"[%(asctime)s : %(filename)s : %(lineno)d : %(levelname).1s]: %(message)s"`
- Date format: `"%Y-%m-%d %H:%M:%S"`
- Rotation: `maxBytes = 5MB`, `backupCount = 5`
- Default levels:
  - `DEFAULT_ROOT_LEVEL = "INFO"`
  - `DEFAULT_CONSOLE_LEVEL = "WARNING"`
  - `DEFAULT_FILE_LEVEL = "INFO"`
- Default channels:
  - `"exceptions"` → `exceptions.log` (level `ERROR`, `stack_on_error=True`)
  - `"success"` → `success.log` (level `INFO`)

> One‑letter level code: `D/I/W/E/C` (from `%(levelname).1s`).

---

## API Overview

### `setup_logging(...)`

```python
setup_logging(
    base_name: str = "app",
    logs_dir: Optional[Path] = None,
    root_level: Optional[str] = None,
    enable_console: Optional[bool] = None,
    console_level: Optional[str] = None,
    file_level: Optional[str] = None,
    console_for_all_channels: bool = False,
    channels: Optional[dict[str, ChannelConfigOptional]] = None,
) -> None
```

- **base_name**: namespace for all loggers (e.g., `"app.channel.success"`).
- **logs_dir**: where files go. Default: `default_logs_dir()`.
- **root_level**: minimum level for the base logger.
- **enable_console**: if `True`, attach a console handler.
- **console_level**: minimum console level (e.g., `"INFO"`).
- **file_level**: minimum level for the base file.
- **console_for_all_channels**: if `True`, mirror all channel logs to console.
- **channels**: mapping `{name: {"filename": ..., "level": ..., "stack_on_error": ...}}`.

### `get_logger(name: str | None = None, *, pretty=False, with_types=False)`

Returns a **ChannelRouter** bound to `name` or to the globally configured base name.  
- `pretty=True` enables pretty serialization and allows consuming iterables/generators for display.
- `with_types=True` appends a `(type=...)` suffix in the pretty dump.

### Fluent usage

```python
lg = get_logger(pretty=True)  # or get_logger("mybase", pretty=True)
ch = lg.channel("success")
ch.debug({"k": {3, 1, 2}})      # visible only if channel level <= DEBUG
ch.info("Saved")
ch.warning("Will retry")
ch.error("Failed")              # or ch.error("Failed", exc=e)
ch.critical("Fatal")
```

---

## Levels (how minimum thresholds work)

Standard order: `DEBUG < INFO < WARNING < ERROR < CRITICAL`.

- A **channel** with `level="INFO"` writes `INFO/WARNING/ERROR/CRITICAL`, ignores `DEBUG`.
- A **console handler** or the **base file** also has its own minimum level.
- Effective output = intersection of the logger’s message level and the handler’s minimum level(s).

Examples:

```python
# Channel level = INFO -> DEBUG is dropped
logger.channel("success").debug("debug detail")   # not written
logger.channel("success").info("visible message") # written

# Channel level = ERROR -> only ERROR/CRITICAL
logger.channel("exceptions").warning("heads up")  # dropped
logger.channel("exceptions").error("oops")        # written
```

---

## Console logging modes

You can control **if** and **where** logs appear in the terminal:

1. **Disabled** (files only): `enable_console=False`
2. **Enabled for all channels and base**: `enable_console=True, console_for_all_channels=True`
3. **Enabled only for base logger**: `enable_console=True, console_for_all_channels=False`
4. **Selective per channel**: keep global console off, then attach your own `StreamHandler` to specific loggers (see recipe below).

### Selective console for one channel

```python
import logging
from ulogging import setup_logging, get_logger

setup_logging(enable_console=False)  # global console off

exc = logging.getLogger("app.channel.exceptions")  # use your actual base_name
stream = logging.StreamHandler()
stream.setLevel(logging.ERROR)  # only show ERROR+ in console
stream.setFormatter(logging.Formatter("[%(levelname).1s] %(message)s"))
exc.addHandler(stream)

logger = get_logger()
logger.channel("exceptions").error("Failed with details")
```

---

## Log files location & rotation

- Default directory is resolved by `default_logs_dir()`.
- Override with `setup_logging(logs_dir=Path("/custom/logs"))`.
- Rotation for each file handler:
  - `maxBytes = 5 * 1024 * 1024` (5 MB)
  - `backupCount = 5`
- To change rotation globally, adjust `LOG_MAX_BYTES` and `LOG_BACKUP_COUNT` in `uconstants.logging` or override handlers in a custom setup.

---

## Exception logging (with stack traces)

Best practice: pass the exception via `exc=`. If a channel has `"stack_on_error": True`, `.error(...)` will include traceback automatically **even if** you omit `exc=`.

```python
try:
    1 / 0
except ZeroDivisionError as e:
    logger.channel("exceptions").error("Division failed", exc=e)

# or simply:
try:
    raise ValueError("bad value")
except ValueError as e:
    logger.channel("exceptions").error(e)
```

---

## Pretty serialization

Enable pretty mode when obtaining the logger/router:

```python
lg = get_logger(pretty=True)                   # pretty payloads
lg_t = get_logger(pretty=True, with_types=True)  # pretty + type suffixes

lg.channel("success").info({"k": {3,1,2}, "nested": {"a": 1}})
lg_t.channel("success").info({"k": {3,1,2}})
```

Behavior highlights:

- **dataclass instance** → serialized via `dataclasses.asdict(...)`.
- **set** → sorted list of `repr(...)` strings.
- **tuple** → converted to list.
- **iterables/generators** → pretty mode may **consume** them to display the full list.
  - If you need to preserve generators, log a snapshot (e.g., `list(itertools.islice(...))`) or avoid `pretty=True`.

---

## Channels: define & use

### Built‑ins

```python
from uconstants.logging import DEFAULT_CHANNELS

# {
#   "exceptions": {"filename": "exceptions.log", "level": "ERROR", "stack_on_error": True},
#   "success":    {"filename": "success.log",     "level": "INFO"},
# }
```

### Add custom channels

```python
CHANNELS = {
    **DEFAULT_CHANNELS,
    "forms.marriage": {"filename": "forms.marriage.log", "level": "INFO"},
    "forms.births":   {"filename": "forms.births.log",   "level": "DEBUG"},
}
setup_logging(channels=CHANNELS, enable_console=True, console_for_all_channels=False)

lg = get_logger(pretty=True)
lg.channel("forms.marriage").info({"record_id": 123, "status": "saved"})
lg.channel("forms.births").debug({"temp": True, "payload": [1,2,3]})
```

> Logger names take the form `"<base_name>.channel.<channel>"` internally. Filenames and levels are controlled by the channel specs, not by the dotted name alone.

---

## Base logger (non‑channeled)

Use the standard `logging` module or the base router’s name to write to the **default base file** (e.g., `default.log`). This is useful for third‑party or legacy logs that don’t use channels.

```python
import logging
from ulogging import setup_logging

setup_logging()
logging.info("Goes to the base file (and console if enabled for base)")
logging.error("Also goes to the base file (and console if enabled)")
```

---

## Environment variables (optional overrides)

The following environment variables (strings) are honored in addition to explicit arguments:

- `APP_LOG_LEVEL` → overrides `root_level`
- `APP_LOG_CONSOLE_LEVEL` → overrides `console_level`
- `APP_LOG_FILE_LEVEL` → overrides `file_level`
- `APP_LOG_ENABLE_CONSOLE` → `"1"|"true"|"yes"|"on"` enables console
- `APP_LOG_CONSOLE_FOR_ALL` → `"1"|"true"|"yes"|"on"` mirrors **all channels** to console

These allow zero‑code configuration flips between dev/test/prod shells.

Example:

```bash
export APP_LOG_ENABLE_CONSOLE=1
export APP_LOG_CONSOLE_FOR_ALL=1
export APP_LOG_CONSOLE_LEVEL=INFO
python your_app.py
```

---

## Ready‑to‑use “autoinit” modules (pick one)

Drop any of these as `ulogging/autoinit.py` (or similar) and import it early (or rely on your app entrypoint to import it). Each variant exposes a `logger` bound to `get_logger()`.

### 1) Files only (no terminal noise)

```python
# ulogging/autoinit.py
from __future__ import annotations
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS

setup_logging(channels=DEFAULT_CHANNELS, enable_console=False)
logger = get_logger()
__all__ = ["logger"]
```

### 2) Mirror everything to console (all channels + base)

```python
# ulogging/autoinit.py
from __future__ import annotations
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS

setup_logging(
    channels=DEFAULT_CHANNELS,
    enable_console=True,
    console_for_all_channels=True,
    console_level="INFO",   # raise to WARNING/ERROR in production
)
logger = get_logger()
__all__ = ["logger"]
```

### 3) Console for **base only** (channels silent in terminal)

```python
# ulogging/autoinit.py
from __future__ import annotations
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS

setup_logging(
    channels=DEFAULT_CHANNELS,
    enable_console=True,
    console_for_all_channels=False,  # only base logger prints
    console_level="WARNING",
)
logger = get_logger()
__all__ = ["logger"]
```

### 4) Selective console (only chosen channels, with level caps)

```python
# ulogging/autoinit.py
from __future__ import annotations
import logging
from ulogging import setup_logging, get_logger
from uconstants.logging import DEFAULT_CHANNELS

# Global console off → we will attach streams manually
setup_logging(channels=DEFAULT_CHANNELS, enable_console=False)

# Print only errors from "exceptions" channel
exc = logging.getLogger("app.channel.exceptions")  # replace "app" if you set base_name=...
h_exc = logging.StreamHandler()
h_exc.setLevel(logging.ERROR)
h_exc.setFormatter(logging.Formatter("[%(levelname).1s] %(message)s"))
exc.addHandler(h_exc)

# Also print info+ from "success" channel (but keep DEBUG hidden)
ok = logging.getLogger("app.channel.success")
h_ok = logging.StreamHandler()
h_ok.setLevel(logging.INFO)  # INFO/WARNING/ERROR/CRITICAL to console; DEBUG still hidden
h_ok.setFormatter(logging.Formatter("[%(levelname).1s] %(message)s"))
ok.addHandler(h_ok)

logger = get_logger()
__all__ = ["logger"]
```

> Tip: To change the **base name**, call `setup_logging(base_name="myapp")` and update the dotted names (`"myapp.channel.<name>"`) where you attach custom console handlers.

---

## Cookbook (more patterns)

### Change logs directory

```python
from pathlib import Path
from ulogging import setup_logging

setup_logging(logs_dir=Path("/var/log/myapp"))
```

### Lower base file noise but keep channel detail

```python
from ulogging import setup_logging
from uconstants.logging import DEFAULT_CHANNELS

setup_logging(
    file_level="WARNING",          # base file writes WARNING+ only
    channels={
        **DEFAULT_CHANNELS,
        "verbose": {"filename": "verbose.log", "level": "DEBUG"},
    },
    enable_console=True,
    console_level="ERROR",         # console shows only ERROR+
)
```

### Channel with forced tracebacks on `.error(...)`

```python
CHANNELS = {
    "taskqueue": {"filename": "taskqueue.log", "level": "INFO", "stack_on_error": True},
}
setup_logging(channels=CHANNELS)
get_logger().channel("taskqueue").error("Task failed without passing exc")  # still records traceback
```

### Log typed/structured payloads

```python
from dataclasses import dataclass

@dataclass
class Payload:
    id: int
    tags: list[str]

lg = get_logger(pretty=True, with_types=True)
lg.channel("success").info(Payload(7, ["a", "b"]))
```

### Avoid consuming generators in pretty mode

```python
def rows():
    for i in range(3):
        yield i

lg = get_logger(pretty=False)  # keep generator intact
lg.channel("success").info(rows())  # prints generator repr without exhausting it
```

---

## Example output

```
[2025-08-25 11:20:41 : worker.py : 22 : I]: Settings initialized
[2025-08-25 11:20:42 : sync.py   : 88 : E]: Failed to save form
[2025-08-25 11:20:43 : api.py    : 51 : W]: Retrying fetch (attempt 2/3)
```

---

## Troubleshooting

- **Nothing appears in console**: ensure `enable_console=True`. For channels, also set `console_for_all_channels=True` **or** attach custom stream handlers.
- **DEBUG not printed**: lower the relevant minimum levels (channel/file/console) to `"DEBUG"`.
- **No files created**: verify the process can create the `logs_dir` (or pass a writable directory).
- **Tracebacks missing**: pass `exc=e` to `.error(...)` or set `"stack_on_error": True` for that channel.
- **Generators look empty**: pretty mode may consume them. Log snapshots or disable `pretty` for those calls.

---

## License

This guide covers usage of a neutral logging library interface. See your project’s LICENSE for distribution terms.
