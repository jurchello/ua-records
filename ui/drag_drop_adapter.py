from __future__ import annotations

import pickle
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position

from gi.repository import Gdk, GLib, Gtk
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.lib import Citation, Person, Place
from gramps.gui.ddtargets import DdTargets

from configs.constants import (
    COLOR_EMPTY_DND,
    COLOR_FILLED_DND,
    get_citation_text_length,
    get_person_name_length,
    get_place_title_length,
)

if TYPE_CHECKING:
    from gramps.gen.db.dbapi import DbState, UiState


class DragDropAdapter:

    _TARGETS = {
        "person": DdTargets.PERSON_LINK,
        "place": DdTargets.PLACE_LINK,
        "citation": DdTargets.CITATION_LINK,
    }

    def __init__(self, dbstate: DbState, uistate: UiState) -> None:
        self.db = dbstate.db
        self.uistate = uistate
        self.dbstate = dbstate
        self._current_drag_source: tuple[object, str, Gtk.Widget] | None = None

    def _on_drag_begin(
        self,
        widget: Gtk.Widget,
        _drag_context: Gdk.DragContext,
        _target_type: str,
    ) -> None:
        try:
            field_id = getattr(widget, "field_id", None)
            data_row = getattr(widget, "_data_row", None)
            if field_id and data_row:
                self._current_drag_source = (data_row, field_id, widget)
            else:
                self._current_drag_source = None
        except Exception:
            self._current_drag_source = None

    def setup_dnd(self, widget: Gtk.Widget, target_type: str, drop_callback: Callable) -> None:
        dd = self._TARGETS.get(target_type)
        targets = [dd.target()] if dd else []

        widget.drag_dest_set(Gtk.DestDefaults.ALL, targets, Gdk.DragAction.COPY)
        widget.connect("drag-data-received", drop_callback, target_type)

        widget.drag_source_set(Gdk.ModifierType.BUTTON1_MASK, targets, Gdk.DragAction.COPY)
        widget.connect("drag-begin", self._on_drag_begin, target_type)
        widget.connect("drag-data-get", self._on_drag_data_get, target_type)

    def handle_drop(
        self,
        widget: Gtk.Widget,
        drag_context: Gdk.DragContext,
        _x: int,
        _y: int,
        data: Gtk.SelectionData,
        _info: int,
        time: int,
        target_type: str,
        store_callback: Callable[[str, Person | Place | Citation], None],
    ) -> None:
        ok = False
        try:
            handle, obj = self._decode_payload(data, target_type)
            if obj is None:
                drag_context.finish(False, False, time)
                return

            store_callback(handle, obj)

            if isinstance(obj, Person):

                name = name_displayer.display(obj) or ""
                self._decorate_success(widget, self._elide(name, get_person_name_length()), markup_kind="u")
            elif isinstance(obj, Place):

                title = place_displayer.display(self.dbstate.db, obj) or ""
                self._decorate_success(widget, self._elide(title, get_place_title_length()), markup_kind="i")
            elif isinstance(obj, Citation):

                txt = obj.page or "(без сторінки)"
                self._decorate_success(
                    widget,
                    f"Цитата: {self._elide(txt, get_citation_text_length())}",
                    markup_kind="u",
                )

            ok = True

        except Exception:
            pass

        drag_context.finish(ok, False, time)

        try:
            src_info = getattr(self, "_current_drag_source", None)
            self._current_drag_source = None

            if not ok or not src_info:
                return

            if not isinstance(src_info, (tuple, list)) or len(src_info) != 3:
                return

            src_row, src_field_id, src_widget = src_info  # pylint: disable=unpacking-non-sequence
            dst_row = getattr(widget, "_data_row", None)
            dst_field_id = getattr(widget, "field_id", None)

            if not dst_row or not dst_field_id or (src_row is dst_row and src_field_id == dst_field_id):
                return

            def _clear_source():
                if src_field_id in src_row.handles:
                    del src_row.handles[src_field_id]
                if src_field_id in src_row.objects:
                    del src_row.objects[src_field_id]

                if hasattr(src_widget, "label"):
                    src_widget.label.set_text(getattr(src_widget, "default_text", "Перетягніть сюди об'єкт"))
                if hasattr(src_widget, "override_background_color"):
                    rgba = Gdk.RGBA()
                    rgba.parse(COLOR_EMPTY_DND)
                    src_widget.override_background_color(Gtk.StateFlags.NORMAL, rgba)
                if hasattr(src_widget, "clear_button"):
                    src_widget.clear_button.set_opacity(0.0)
                    src_widget.clear_button.set_sensitive(False)

                if hasattr(src_row, "_trigger_sync") and callable(src_row._trigger_sync):
                    src_row._trigger_sync()
                if hasattr(dst_row, "_trigger_sync") and callable(dst_row._trigger_sync):
                    dst_row._trigger_sync()
                return False

            GLib.idle_add(_clear_source)

        except Exception:
            pass

    def _on_drag_data_get(
        self,
        widget: Gtk.Widget,
        _drag_context: Gdk.DragContext,
        data: Gtk.SelectionData,
        _info: int,
        _time: int,
        target_type: str,
    ) -> None:
        try:
            field_id = getattr(widget, "field_id", None)
            if not field_id:
                return

            data_row = getattr(widget, "_data_row", None)
            if not data_row:
                parent = widget.get_parent()
                while parent and not hasattr(parent, "_data_row"):
                    parent = parent.get_parent()
                if parent:
                    data_row = parent._data_row

            if not data_row:
                return

            handle = data_row.handles.get(field_id)
            if not handle:
                return

            self._current_drag_source = (data_row, field_id, widget)

            tag_map = {"person": "person-link", "place": "place-link", "citation": "citation-link"}
            tag = tag_map.get(target_type)
            if not tag:
                return

            payload = (tag, None, handle, None)
            serialized = pickle.dumps(payload)
            data.set(data.get_target(), 8, serialized)

        except Exception:
            pass

    def _decode_payload(self, data: Gtk.SelectionData, target_type: str) -> tuple[str, Any | None]:
        try:
            raw = data.get_data()
            payload = pickle.loads(raw)
            if not isinstance(payload, (list, tuple)) or len(payload) < 3:
                return "", None
            tag, _, handle = payload[0], payload[1], payload[2]
            if not isinstance(handle, str):
                return "", None
        except Exception:
            return "", None

        if tag == "person-link" and target_type == "person":
            obj = self.db.get_person_from_handle(handle)
            return handle, obj if isinstance(obj, Person) else None
        if tag == "place-link" and target_type == "place":
            obj = self.db.get_place_from_handle(handle)
            return handle, obj if isinstance(obj, Place) else None
        if tag == "citation-link" and target_type == "citation":
            obj = self.db.get_citation_from_handle(handle)
            return handle, obj if isinstance(obj, Citation) else None

        return "", None

    @staticmethod
    def _elide(text: str, maxlen: int) -> str:
        return text if len(text) <= maxlen else text[: maxlen - 1] + "…"

    def _decorate_success(self, widget: Gtk.Widget, text: str, *, markup_kind: str = "u") -> None:
        # label
        lbl = getattr(widget, "label", None)
        if isinstance(lbl, Gtk.Label):
            try:
                if markup_kind == "i":
                    lbl.set_markup(f"<i>{text}</i>")
                elif markup_kind == "u":
                    lbl.set_markup(f"<u>{text}</u>")
                else:
                    lbl.set_text(text)
            except Exception:
                lbl.set_text(text)

        # clear_button
        clr = getattr(widget, "clear_button", None)
        if isinstance(clr, Gtk.Button):
            try:
                clr.set_opacity(1.0)
                clr.set_sensitive(True)
            except Exception:
                pass

        self._set_dnd_background(widget, has_object=True)

    def _set_dnd_background(self, widget: Gtk.Widget, has_object: bool) -> None:
        rgba = Gdk.RGBA()
        color = COLOR_FILLED_DND if has_object else COLOR_EMPTY_DND
        try:
            if isinstance(color, str):
                rgba.parse(color)
                widget.override_background_color(Gtk.StateFlags.NORMAL, rgba)
            elif isinstance(color, Gdk.RGBA):
                widget.override_background_color(Gtk.StateFlags.NORMAL, color)
        except Exception:
            pass
