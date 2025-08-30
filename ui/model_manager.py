from __future__ import annotations
from typing import TYPE_CHECKING
import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gtk
from uhelpers.gtk_helpers import setup_entry_completion
from ui.shared_cache import UI_MODEL_CACHE

if TYPE_CHECKING:
    from gramps.gen.db.base import DbReadBase


def _dbid(db: DbReadBase) -> str:
    get_id = getattr(db, "get_dbid", None)
    if callable(get_id):
        try:
            return str(get_id())
        except Exception:
            pass
    return str(id(db))


def _options_model_key(db: DbReadBase, opts: object) -> tuple[str, int, str]:
    if callable(opts):
        orig = getattr(opts, "__wrapped__", opts)
        return ("fn", id(orig), _dbid(db))
    return ("list", id(opts), _dbid(db))


class ModelManager:

    def ensure_options_model(self, db: DbReadBase, opts) -> Gtk.ListStore:
        key = _options_model_key(db, opts)
        model = UI_MODEL_CACHE.get(key)

        if model is not None and len(model) == 0 and callable(opts):
            del UI_MODEL_CACHE[key]
            from configs import options as OPT  # pylint: disable=import-outside-toplevel

            OPT.clear_options_cache()
            model = None

        if model is None:
            if callable(opts):

                from configs import options as OPT  # pylint: disable=import-outside-toplevel

                cache_key = OPT._db_cache_key(db, opts.__name__)
                if cache_key in OPT._dynamic_options_cache:
                    cached_result = OPT._dynamic_options_cache[cache_key]
                    if len(cached_result) == 0:
                        OPT.clear_options_cache()

                try:
                    opts_list = opts(db) or []
                except Exception:
                    import traceback  # pylint: disable=import-outside-toplevel

                    traceback.print_exc()
                    opts_list = []
            else:
                opts_list = opts or []
            model = Gtk.ListStore(str, str)
            for option in opts_list:
                s = str(option)
                s_norm = " ".join(s.strip().lower().split())
                model.append([s, s_norm])
            UI_MODEL_CACHE[key] = model

        return model

    @staticmethod
    def register_combobox_on_toplevel(combo: Gtk.ComboBox, toplevel: Gtk.Widget) -> None:
        lst = getattr(toplevel, "_all_comboboxes", None)
        if lst is None:
            lst = []
            setattr(toplevel, "_all_comboboxes", lst)
        lst.append(combo)

    def lazy_attach_model(self, combo: Gtk.ComboBox, db: DbReadBase, opts) -> None:
        if getattr(combo, "_lazy_attached", False):
            return
        model = self.ensure_options_model(db, opts)
        combo.set_model(model)
        combo.set_entry_text_column(0)

        entry = combo.get_child()
        if entry and isinstance(entry, Gtk.Entry):
            setup_entry_completion(entry, model)

        combo._lazy_attached = True

    @staticmethod
    def lazy_detach_model(combo: Gtk.ComboBox) -> None:
        try:
            entry = combo.get_child()
            if entry and hasattr(entry, "get_completion"):
                comp = entry.get_completion()
                if comp:
                    entry.set_completion(None)
        except Exception:
            pass
        try:
            combo.set_model(None)
        except Exception:
            pass
        combo._lazy_attached = False
