from __future__ import annotations

from typing import Any, Dict

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position

from gi.repository import Gdk, Gtk
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.display.place import displayer as place_displayer

from configs.constants import (
    COLOR_EMPTY_DND,
    COLOR_EMPTY_INPUT,
    COLOR_FILLED_INPUT,
    get_citation_text_length,
    get_person_name_length,
    get_place_title_length,
)
from uhelpers.gtk_helpers import parse_bool_from_string


class ResetManager:

    @staticmethod
    def _apply_background(eventbox: Gtk.EventBox, filled: bool) -> None:
        color = COLOR_FILLED_INPUT if filled else COLOR_EMPTY_INPUT
        rgba = Gdk.RGBA()
        rgba.parse(color)
        eventbox.override_background_color(Gtk.StateFlags.NORMAL, rgba)
        child = eventbox.get_child()
        if isinstance(child, Gtk.ComboBox):
            entry = child.get_child()
            if entry and isinstance(entry, Gtk.Entry):
                entry.override_background_color(Gtk.StateFlags.NORMAL, rgba)
        elif isinstance(child, Gtk.Entry):
            child.override_background_color(Gtk.StateFlags.NORMAL, rgba)

    def _apply_dnd_by_gramps_id(
        self,
        dbstate: Any,
        field_id: str,
        field_type: str,
        gramps_id: str,
        eventbox: Gtk.EventBox,
        handles: Dict[str, str],
        objects: Dict[str, object],
    ) -> None:
        obj = None
        if field_type == "place":
            obj = dbstate.db.get_place_from_gramps_id(gramps_id)
        elif field_type == "person":
            obj = dbstate.db.get_person_from_gramps_id(gramps_id)
        elif field_type == "citation":
            obj = dbstate.db.get_citation_from_gramps_id(gramps_id)

        if not obj:
            self._clear_dnd_eventbox(eventbox, handles, objects)
            return

        handle = obj.get_handle()
        handles[field_id] = handle
        objects[field_id] = obj

        if field_type == "place":
            title = place_displayer.display(dbstate.db, obj)
            if len(title) > get_place_title_length():
                title = title[: get_place_title_length() - 1] + "…"
            eventbox.label.set_markup(f"<u>{title}</u>")
        elif field_type == "person":
            name = name_displayer.display(obj)
            if len(name) > get_person_name_length():
                name = name[: get_person_name_length() - 1] + "…"
            eventbox.label.set_markup(f"<u>{name}</u>")
        elif field_type == "citation":
            txt = obj.page or "(без сторінки)"
            if len(txt) > get_citation_text_length():
                txt = txt[: get_citation_text_length() - 1] + "…"
            eventbox.label.set_markup(f"<u>Цитата: {txt}</u>")

        eventbox.clear_button.set_opacity(1.0)
        eventbox.clear_button.set_sensitive(True)
        eventbox.queue_draw()

    @staticmethod
    def _clear_dnd_eventbox(eventbox: Gtk.EventBox, handles: Dict[str, str], objects: Dict[str, object]) -> None:
        field_id = eventbox.field_id
        objects.pop(field_id, None)
        handles.pop(field_id, None)
        eventbox.label.set_text(eventbox.default_text)
        rgba = Gdk.RGBA()
        rgba.parse(COLOR_EMPTY_DND)
        eventbox.override_background_color(Gtk.StateFlags.NORMAL, rgba)
        eventbox.clear_button.set_opacity(0.0)
        eventbox.clear_button.set_sensitive(False)

    def reset_to_defaults(
        self,
        *,
        widgets: Dict[str, Gtk.Widget],
        types: Dict[str, str],  # pylint: disable=unused-argument
        defaults: Dict[str, object],
        changed_handlers: Dict[str, int],
        dbstate: Any,
        handles: Dict[str, str],
        objects: Dict[str, object],
    ) -> None:
        for field_id, container in widgets.items():
            child = container.get_child() if isinstance(container, Gtk.EventBox) else container

            # Checkbox
            if isinstance(container, Gtk.CheckButton):
                raw_default = defaults.get(field_id, False)
                default_bool = parse_bool_from_string(raw_default)
                container.set_active(default_bool)
                continue

            # Entry / ComboBox
            if isinstance(child, (Gtk.ComboBox, Gtk.Entry)):
                default_text = str(getattr(container, "default_text", "") or "")
                hid = changed_handlers.get(field_id)

                if isinstance(child, Gtk.ComboBox):
                    entry = child.get_child()
                    if entry and isinstance(entry, Gtk.Entry):
                        if hid is not None:
                            entry.handler_block(hid)
                        entry.set_text(default_text)
                        if hasattr(child, "set_active"):
                            child.set_active(-1)
                        if hid is not None:
                            entry.handler_unblock(hid)
                        self._apply_background(container, filled=bool(default_text.strip()))
                else:  # Gtk.Entry
                    if hid is not None:
                        child.handler_block(hid)
                    child.set_text(default_text)
                    if hid is not None:
                        child.handler_unblock(hid)
                    self._apply_background(container, filled=bool(default_text.strip()))
                continue

            # DnD EventBox
            if isinstance(container, Gtk.EventBox) and hasattr(container, "field_type"):
                default_val = defaults.get(field_id)
                if isinstance(default_val, str) and default_val.strip():
                    gramps_id = default_val.strip()
                    self._apply_dnd_by_gramps_id(
                        dbstate=dbstate,
                        field_id=field_id,
                        field_type=container.field_type,
                        gramps_id=gramps_id,
                        eventbox=container,
                        handles=handles,
                        objects=objects,
                    )
                else:
                    self._clear_dnd_eventbox(container, handles, objects)
                continue
