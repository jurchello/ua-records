from __future__ import annotations

from typing import Any, Dict, List

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position

from gi.repository import GLib, Gtk


class ConditionManager:
    """


    - "show_when": {"var": "<field_id>", "equals": "..."} |
                   {"var": "<field_id>", "in": ["..."]} |
                   {"var": "<field_id>", "not_in": ["..."]} |
                   {"var": "<field_id>", "truthy": true}
    """

    def __init__(
        self,
        *,
        widgets: Dict[str, Gtk.Widget],
        labels: Dict[str, Gtk.Label],
        label_boxes: Dict[str, Gtk.Widget],
        field_defs: List[List[Dict[str, Any]]] | List[Dict[str, Any]],
        get_cols=None,
    ) -> None:
        self.widgets = widgets
        self.labels = labels
        self.label_boxes = label_boxes
        self._fields: List[Dict[str, Any]] = self._flatten_fields(field_defs)
        self._by_var: Dict[str, List[Dict[str, Any]]] = {}
        self._id_alias: Dict[str, str] = {}
        self._wired_vars: set[str] = set()
        self._on_visibility_changed = None
        self._get_cols = get_cols or (lambda: 1)

    @staticmethod
    def _flatten_fields(
        field_defs: List[List[Dict[str, Any]]] | List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        if not field_defs:
            return []
        if field_defs and isinstance(field_defs[0], dict):
            return list(field_defs)
        return [f for row in field_defs for f in row if isinstance(f, dict)]

    def _resolve_id(self, short_id: str) -> str:
        if short_id in self._id_alias:
            return self._id_alias[short_id]

        if short_id in self.widgets or short_id in self.labels or short_id in self.label_boxes:
            self._id_alias[short_id] = short_id
            return short_id

        candidates = []
        for key in self.widgets.keys():
            if key.endswith("." + short_id) or key.endswith("_" + short_id):
                candidates.append(key)

        if candidates:
            real = candidates[0]
            self._id_alias[short_id] = real
            return real

        self._id_alias[short_id] = short_id
        return short_id

    def _get_widget(self, field_id: str) -> Gtk.Widget | None:
        return self.widgets.get(self._resolve_id(field_id))

    def _get_label(self, field_id: str) -> Gtk.Label | None:
        return self.labels.get(self._resolve_id(field_id))

    def _get_label_box(self, field_id: str) -> Gtk.Widget | None:
        return self.label_boxes.get(self._resolve_id(field_id))

    def set_visibility_changed_callback(self, cb):
        self._on_visibility_changed = cb

    def init_rules(self) -> None:
        for f in self._fields:
            show_when = f.get("show_when")
            label_vars = f.get("label_variants")

            if isinstance(show_when, dict) and "var" in show_when:
                self._by_var.setdefault(show_when["var"], []).append(f)

            if isinstance(label_vars, dict):
                lv_var = f.get("label_var") or f.get("variant_var")
                if lv_var:
                    self._by_var.setdefault(lv_var, []).append(f)

        for var in self._by_var:
            self._wire(var)

        GLib.idle_add(self.apply_all)

        if callable(self._on_visibility_changed):
            GLib.idle_add(self._on_visibility_changed)

    def evaluate(self) -> bool:
        return self.apply_all()

    def apply_all(self) -> bool:
        changed = False

        for var in list(self._by_var.keys()):
            current = self._get_value(var)
            for f in self._by_var.get(var, []):
                changed |= self._apply_visibility_full(f, current)
                self._apply_label_variant(f.get("id"), f, var, current)

        for f in self._fields:
            if not isinstance(f, dict):
                continue
            has_var = isinstance(f.get("show_when"), dict) and "var" in f["show_when"]
            has_cols = f.get("show_when_cols_in") or f.get("hide_when_cols_in")
            if (not has_var) and has_cols:
                changed |= self._apply_visibility_full(f, "")

        if changed and callable(self._on_visibility_changed):
            try:
                self._on_visibility_changed()
            except Exception:
                pass

        return False

    def _wire(self, var: str) -> None:
        if var in self._wired_vars:
            return

        w = self._get_widget(var)
        if not w:
            return

        child = w.get_child() if isinstance(w, Gtk.EventBox) else w

        def _defer_apply(*_a):
            GLib.idle_add(self.apply_all)
            return False

        if isinstance(child, Gtk.Entry):
            child.connect("changed", _defer_apply)
        elif isinstance(child, Gtk.CheckButton):
            child.connect("toggled", _defer_apply)
        elif isinstance(child, Gtk.ComboBox):
            child.connect("changed", _defer_apply)
            entry = child.get_child()
            if isinstance(entry, Gtk.Entry):
                entry.connect("changed", _defer_apply)

        self._wired_vars.add(var)

    def _cols_ok(self, field_def: Dict[str, Any]) -> bool:
        cols = int(self._get_cols() or 1)
        allow = field_def.get("show_when_cols_in")
        deny = field_def.get("hide_when_cols_in")
        if isinstance(allow, (list, tuple, set)) and allow:
            if cols not in set(int(x) for x in allow):
                return False
        if isinstance(deny, (list, tuple, set)) and deny:
            if cols in set(int(x) for x in deny):
                return False
        return True

    def _get_value(self, field_id: str) -> str:
        w = self._get_widget(field_id)
        if not w:
            return ""

        child = w.get_child() if isinstance(w, Gtk.EventBox) else w

        if isinstance(child, Gtk.CheckButton):
            return "1" if child.get_active() else ""

        if isinstance(child, Gtk.Entry):
            return (self._get_text_value(child) or "").strip()

        if isinstance(child, Gtk.ComboBox):
            entry = child.get_child()
            if isinstance(entry, Gtk.Entry):
                return (self._get_text_value(entry) or "").strip()
            try:
                get_active_text = getattr(child, "get_active_text", None)
                if callable(get_active_text):
                    txt = get_active_text() or ""
                    return txt.strip()
            except Exception:
                pass
            try:
                it = child.get_active_iter()
                if it:
                    model = child.get_model()
                    val = model[it][0]
                    return (val or "").strip()
            except Exception:
                pass
            return ""

        return ""

    def _get_text_value(self, widget):
        if isinstance(widget, Gtk.Entry):
            return widget.get_text() or ""
        if isinstance(widget, Gtk.EventBox) and hasattr(widget, "input") and isinstance(widget.input, Gtk.Entry):
            return widget.input.get_text() or ""
        if isinstance(widget, Gtk.CheckButton):
            return "1" if widget.get_active() else ""
        return ""

    def _apply_for_var(self, var: str) -> bool:
        current = self._get_value(var)
        changed_any = False
        for f in self._by_var.get(var, []):
            fid = f.get("id")
            if not fid:
                continue
            if self._apply_visibility(fid, f.get("show_when"), current):  # повертає bool
                changed_any = True
            self._apply_label_variant(fid, f, var, current)
        return changed_any

    def _apply_visibility_full(self, field_def: Dict[str, Any], current_var_value: str) -> bool:
        fid = field_def.get("id")
        if not fid:
            return False

        label_box = self._get_label_box(fid)
        widget = self._get_widget(fid)
        if not label_box or not widget:
            return False

        rule = field_def.get("show_when")
        var_ok = True
        if isinstance(rule, dict) and "var" in rule:
            if "equals" in rule:
                var_ok = current_var_value == str(rule["equals"])
            elif "in" in rule:
                var_ok = current_var_value in list(rule["in"])
            elif "not_in" in rule:
                var_ok = current_var_value not in list(rule["not_in"])
            elif "truthy" in rule:
                falsy = {"", "0", "false", "no", "n", "off"}
                var_ok = current_var_value.lower() not in falsy if current_var_value else False

        cols_ok = self._cols_ok(field_def)

        visible = bool(var_ok and cols_ok)

        before = label_box.get_visible() and widget.get_visible()
        if visible:
            try:
                label_box.show()
                widget.show()
            except Exception:
                pass
        else:
            try:
                label_box.hide()
                widget.hide()
            except Exception:
                pass
        return bool(before != visible)

    def _apply_visibility(self, field_id: str, rule: Dict[str, Any] | None, current: str) -> bool:
        label_box = self._get_label_box(field_id)
        widget = self._get_widget(field_id)
        if not label_box or not widget:
            return False

        prev_label = bool(label_box.get_visible())
        prev_widget = bool(widget.get_visible())

        if not rule or not isinstance(rule, dict) or "var" not in rule:
            visible = True
        else:
            visible = True
            if "equals" in rule:
                visible = current == str(rule["equals"])
            elif "in" in rule:
                visible = current in list(rule["in"])
            elif "not_in" in rule:
                visible = current not in list(rule["not_in"])
            elif "truthy" in rule:
                falsy_values = {"", "0", "false", "no", "n", "off"}
                visible = current.lower() not in falsy_values if current else False

        try:
            if visible:
                label_box.show()
                widget.show()
            else:
                label_box.hide()
                widget.hide()
        except Exception:
            pass

        return (prev_label != visible) or (prev_widget != visible)

    def _apply_label_variant(self, field_id: str, field_def: Dict[str, Any], var: str, current: str) -> None:
        lbl = self._get_label(field_id)
        if not lbl:
            return
        variants = field_def.get("label_variants")
        if not isinstance(variants, dict):
            return

        _ = field_def.get("label_var") or field_def.get("variant_var") or var

        new_text = variants.get(current) or variants.get("default")
        if not new_text:
            return

        escaped = GLib.markup_escape_text(new_text)
        lbl.set_markup(f"<b><span foreground='black'>{escaped}</span></b>")
