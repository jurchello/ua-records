"""GTK utility functions to reduce code duplication."""

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gtk


def setup_entry_completion(entry: Gtk.Entry, model: Gtk.ListStore) -> None:
    """Setup auto-completion for GTK Entry with custom matching."""
    comp = Gtk.EntryCompletion()
    comp.set_model(model)
    comp.set_text_column(0)
    comp.set_inline_completion(False)
    comp.set_inline_selection(False)
    comp.set_popup_completion(True)
    if hasattr(comp, "set_popup_single_match"):
        comp.set_popup_single_match(True)
    if hasattr(comp, "set_minimum_key_length"):
        comp.set_minimum_key_length(1)

    def _norm(s: str) -> str:
        return " ".join((s or "").strip().lower().split())

    def _match_func(_comp_, key_string, tree_iter, _data):
        q = _norm(key_string)
        if not q:
            return True
        val = model[tree_iter][1]
        start = 0
        for token in q.split(" "):
            pos = val.find(token, start)
            if pos == -1:
                return False
            start = pos + len(token)
        return True

    comp.set_match_func(_match_func, None)
    entry.set_completion(comp)


def parse_bool_from_string(raw_value) -> bool:
    """Parse boolean value from string or other type."""
    if isinstance(raw_value, str):
        norm = raw_value.strip().lower()
        return norm in ("1", "true", "yes", "y", "on")
    return bool(raw_value)
