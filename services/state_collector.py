from __future__ import annotations

import re
from typing import TYPE_CHECKING

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gtk

if TYPE_CHECKING:
    from form_state_base import FormStateBase

    from ui.data_row import DataRow


class StateCollector:

    @staticmethod
    def _is_spacer_field(field_id: str) -> bool:
        """
        - "sp1", "_sp1", "__sp2"
        """
        if not isinstance(field_id, str):
            return False
        fid = field_id.strip()
        if not fid:
            return False

        return re.search(r"(?:^|_)sp\d*$", fid) is not None

    @staticmethod
    def collect_row(row: "DataRow", state: "FormStateBase", allow_log: bool = True) -> None:
        def _prefix_and_key(field_id: str) -> tuple[str, str]:
            raw = StateCollector._extract_raw_key(field_id, row.prefix or "")
            if isinstance(raw, str) and "." in raw:
                head, tail = raw.split(".", 1)
                return head, tail
            return (row.prefix or "", raw)

        for field_id, container in row.widgets.items():
            if StateCollector._is_spacer_field(field_id):
                continue
            value = StateCollector._value_from_widget(container)
            if value is None:
                continue
            prefix, key = _prefix_and_key(field_id)
            state.set(prefix=prefix, key=key, value=value, allow_log=allow_log)
        obj_keys = set(row.handles.keys()) | set(row.objects.keys())
        for field_id in obj_keys:
            if StateCollector._is_spacer_field(field_id):
                continue
            handle = row.handles.get(field_id)
            obj = row.objects.get(field_id)
            if obj is None and handle:
                ftype = row.types.get(field_id)
                try:
                    if ftype == "place":
                        obj = row.dbstate.db.get_place_from_handle(handle)
                    elif ftype == "person":
                        obj = row.dbstate.db.get_person_from_handle(handle)
                    elif ftype == "citation":
                        obj = row.dbstate.db.get_citation_from_handle(handle)
                except Exception:
                    obj = None
            if not handle and obj is None:
                continue
            prefix, key = _prefix_and_key(field_id)
            payload = {}
            if handle:
                payload["handle"] = handle
            if obj is not None:
                payload["object"] = obj
            state.set(prefix=prefix, key=key, value=payload, allow_log=allow_log)

    # -------- helpers --------

    @staticmethod
    def _prefix_and_key_from_spec_or_id(row: "DataRow", _spec: dict, field_id: str) -> tuple[str, str]:
        raw = StateCollector._extract_raw_key(field_id, row.prefix or "")
        if isinstance(raw, str) and "." in raw:
            head, tail = raw.split(".", 1)
            return head, tail
        return (row.prefix or "", raw)

    @staticmethod
    def _extract_raw_key(field_id: str, prefix: str | None) -> str:
        if not prefix:
            return field_id
        expected = f"{prefix}_"
        if field_id.startswith(expected):
            return field_id[len(expected) :]
        return field_id

    @staticmethod
    def _value_from_widget(container: Gtk.Widget) -> str | bool | float | None:
        child = container.get_child() if isinstance(container, Gtk.EventBox) else container

        if isinstance(child, Gtk.Entry):
            s = child.get_text().strip()
            return s or None

        if isinstance(child, Gtk.ComboBoxText):
            text = child.get_active_text()
            return text.strip() if text else None

        if isinstance(child, Gtk.ComboBox):
            entry = child.get_child()
            if isinstance(entry, Gtk.Entry):
                s = entry.get_text().strip()
                return s or None
            model = child.get_model()
            it = child.get_active_iter()
            return model[it][0].strip() if model and it else None

        if isinstance(child, (Gtk.Switch, Gtk.CheckButton)):
            return bool(child.get_active())

        if isinstance(child, Gtk.SpinButton):
            return float(child.get_value())

        return None
