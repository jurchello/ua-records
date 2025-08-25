import re
from pathlib import Path
import logging
import pytest

from ulogging import setup_logging, get_logger
from uconstants.logging import (
    DEFAULT_CHANNELS,
    ChannelConfigOptional,
    DEFAULT_LOG_NAME,
    DEFAULT_BASE_LOGGER_NAME,
)

# ---------- helpers ----------

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""

def rm(p: Path) -> None:
    """Clear file content instead of removing to avoid logging handler issues"""
    try:
        p.write_text("", encoding="utf-8")
    except FileNotFoundError:
        pass

def line_has_std_format(line: str, expected_filename: str) -> bool:
    # [YYYY-MM-DD HH:MM:SS : filename.py : N : L]:
    pat = rf"^\[\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}} : {re.escape(expected_filename)} : \d+ : [A-Z]\]: "
    return re.match(pat, line) is not None


# ---------- tests ----------

def test_success_channel_writes_to_own_file(tmp_path: Path) -> None:
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        channels=DEFAULT_CHANNELS,
        console_for_all_channels=False,
    )
    logger = get_logger()  # base="app" by default
    success_file = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(success_file)

    logger.channel("success").info("Done OK")

    assert success_file.exists(), "success channel log file must be created"
    txt = read_text(success_file)
    assert "Done OK" in txt
    first_line = txt.splitlines()[0]
    # ім'я цього тестового файлу виводиться у форматі
    assert line_has_std_format(first_line, expected_filename="test_logging_channels.py")


def test_exceptions_channel_writes_traceback(tmp_path: Path) -> None:
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        channels=DEFAULT_CHANNELS,  # exceptions has stack_on_error=True
        console_for_all_channels=False,
    )
    logger = get_logger()
    exc_file = tmp_path / DEFAULT_CHANNELS["exceptions"]["filename"]
    rm(exc_file)

    try:
        raise RuntimeError("boom-err")
    except RuntimeError as e:
        logger.channel("exceptions").error(e)

    assert exc_file.exists()
    txt = read_text(exc_file)
    assert "RuntimeError('boom-err')" in txt or "RuntimeError: boom-err" in txt
    assert "Traceback (most recent call last)" in txt


def test_default_log_receives_base_logs(tmp_path: Path) -> None:
    """Non-channeled logs should go to default.log under the base logger name."""
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        console_for_all_channels=False,
    )
    default_path = tmp_path / DEFAULT_LOG_NAME
    rm(default_path)

    # write via the base logger (non-channeled)
    logging.getLogger(DEFAULT_BASE_LOGGER_NAME).info("base-info")

    assert default_path.exists()
    txt = read_text(default_path)
    assert "base-info" in txt


def test_channel_console_echo_when_enabled(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging(
        logs_dir=tmp_path,
        enable_console=True,
        console_level="INFO",  # Allow INFO messages to console
        console_for_all_channels=True,
        channels=DEFAULT_CHANNELS,
    )
    logger = get_logger()

    logger.channel("success").info("to-console-and-file")

    captured = capsys.readouterr()
    # StreamHandler writes to stderr by default
    assert "to-console-and-file" in captured.err


def test_pretty_serializer_with_types_flag(tmp_path: Path) -> None:
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        channels=DEFAULT_CHANNELS,
    )
    logger = get_logger()

    success_file = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(success_file)

    payload = {"a": 1, "b": {1, 3, 2}}
    logger.channel("success").info(payload, with_types=True)

    txt = read_text(success_file)
    # dict with key 'a'
    assert "'a': 1" in txt
    # set becomes sorted list of reprs → square brackets present
    assert "[" in txt and "]" in txt
    # type info appended
    assert "(type=" in txt


def test_custom_channel_definition(tmp_path: Path) -> None:
    channels: dict[str, ChannelConfigOptional] = {
        "metrics": {"filename": "metrics.log", "level": "DEBUG"},
    }
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        channels=channels,
    )
    logger = get_logger()
    metrics_file = tmp_path / "metrics.log"
    rm(metrics_file)

    logger.channel("metrics").debug({"value": 42})

    assert metrics_file.exists()
    txt = read_text(metrics_file)
    assert "42" in txt


def test_exceptions_channel_explicit_exc_kwarg(tmp_path: Path) -> None:
    setup_logging(
        logs_dir=tmp_path,
        enable_console=False,
        channels=DEFAULT_CHANNELS,
    )
    logger = get_logger()
    exc_file = tmp_path / DEFAULT_CHANNELS["exceptions"]["filename"]
    rm(exc_file)

    try:
        1 / 0  # pyright: ignore[reportUnusedExpression]
    except ZeroDivisionError as e:
        logger.channel("exceptions").error("division failed", exc=e)

    txt = read_text(exc_file)
    assert "division failed" in txt
    assert "ZeroDivisionError" in txt
    assert "Traceback (most recent call last)" in txt


def test_log_line_format_contains_filename_and_lineno(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False)
    logger = get_logger()
    success_file = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(success_file)

    logger.channel("success").info("format-check")

    line0 = read_text(success_file).splitlines()[0]
    assert line_has_std_format(line0, "test_logging_channels.py")
    assert line0.endswith("format-check")

def test_generator_consumed_when_pretty_logging(tmp_path: Path) -> None:
    """Test that generators are consumed and logged as lists when pretty=True."""
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    p = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    p.write_text("", encoding="utf-8")

    def gen():
        for i in range(3):
            yield i

    g = gen()
    logger.channel("success").info(g)

    out = p.read_text(encoding="utf-8")
    assert "[0, 1, 2]" in out
    # Generator should be exhausted after logging
    assert list(g) == []