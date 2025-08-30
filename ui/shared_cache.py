from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gtk

UI_MODEL_CACHE: dict[tuple[str, int, str], Gtk.ListStore] = {}
