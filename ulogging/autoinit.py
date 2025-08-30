from __future__ import annotations

from .logging_setup import get_logger, setup_logging

setup_logging(enable_console=False, console_for_all_channels=True)

logger = get_logger()

__all__ = ["logger"]
