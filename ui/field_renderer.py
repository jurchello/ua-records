from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Tuple

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Pango", "1.0")  # pylint: disable=wrong-import-position

from gi.repository import Gdk, GLib, Gtk, Pango
from gi.repository import GdkPixbuf
from gramps.gen.display.name import displayer as name_displayer
from gramps.gen.display.place import displayer as place_displayer
from gramps.gen.errors import WindowActiveError
from gramps.gui.editors import EditCitation, EditPerson, EditPlace

from configs.constants import (
    COLOR_EMPTY_DND,
    COLOR_EMPTY_INPUT,
    COLOR_FILLED_INPUT,
    get_citation_text_length,
    get_dnd_default,
    get_dnd_rules,
    get_label_mode,
    get_person_name_length,
    get_place_title_length,
)
from uhelpers.gtk_helpers import parse_bool_from_string, setup_entry_completion

DbState = Any
UiState = Any
DragDropAdapter = Any


class FieldRenderer:

    def __init__(
        self,
        *,
        dbstate: DbState,
        uistate: UiState,
        dnd_adapter: DragDropAdapter,
        model_manager,
        toplevel: Gtk.Widget,
        widgets: Dict[str, Gtk.Widget],
        objects: Dict[str, object],
        handles: Dict[str, str],
        defaults: Dict[str, str],
        types: Dict[str, str],
        changed_handlers: Dict[str, int],
        data_row=None,
    ) -> None:
        self.dbstate = dbstate
        self.uistate = uistate
        self.dnd_adapter = dnd_adapter
        self.model_manager = model_manager
        self._toplevel = toplevel
        self._checkbox_css_provider = None
        self._help_css_provider = None
        self.labels: Dict[str, Gtk.Label] = {}
        self.label_boxes: Dict[str, Gtk.Widget] = {}
        self.widgets = widgets
        self.objects = objects
        self.handles = handles
        self.defaults = defaults
        self.types = types
        self.changed_handlers = changed_handlers
        self.data_row = data_row
        self._entry_sel_provider = None
        self._field_specs = {}
        self._creation_index = 0
        self._row_grid = None
        self._frame_pairs = 1
        self._grid_adjusted = False
        self._label_size_groups = []
        self._widget_size_groups = []
        self._span_widgets = []

    @staticmethod
    def prepare_rows(fields: List[List[dict]]) -> List[List[dict]]:
        out: List[List[dict]] = []
        for sr in fields:
            cur: List[dict] = []
            for f in sr:
                cur.append(f)
                if f.get("span_rest"):
                    out.append(cur)
                    cur = []
            if cur:
                out.append(cur)
        return out

    @staticmethod
    def _count_pairs(subrow: List[dict]) -> int:
        total = 0
        for f in subrow:
            if f.get("type") == "spacer":
                total += int(f.get("span_pairs", 1))
            else:
                total += 1
        return total

    def set_field_specs(self, field_specs: Dict[str, dict]) -> None:
        self._field_specs = field_specs or {}

    def set_layout_context(self, row_grid: Gtk.Grid, frame_pairs: int) -> None:
        self._row_grid = row_grid
        self._frame_pairs = max(1, int(frame_pairs or 1))
        if row_grid:
            row_grid.connect("size-allocate", self._on_grid_size_allocate)

    def max_pairs_in_frame(self, rows: List[List[dict]]) -> int:
        return max((self._count_pairs(sr) for sr in rows), default=1)

    def _on_grid_size_allocate(self, _grid: Gtk.Grid, allocation: Gdk.Rectangle) -> None:
        if getattr(self, "_grid_adjusted", False):
            return
        if self._frame_pairs <= 1:
            return

        available = allocation.width - 50
        for entry in getattr(self, "_span_widgets", []):
            if isinstance(entry, Gtk.Entry):
                entry.set_size_request(available, 30)
                entry.set_hexpand(True)
        self._grid_adjusted = True

    def render_rows(
        self,
        rows: List[List[dict]],
        row_grid: Gtk.Grid,
        frame_pairs: int,
        background_color: str | Gdk.RGBA | None,
        label_size_groups: List[Gtk.SizeGroup],
        widget_size_groups: List[Gtk.SizeGroup],
    ) -> None:
        self._label_size_groups = label_size_groups or []
        self._widget_size_groups = widget_size_groups or []
        current_row = 0
        for subrow in rows:
            current_row = self._render_subrow(
                subrow,
                row_grid,
                current_row,
                frame_pairs,
                background_color,
                label_size_groups,
                widget_size_groups,
            )

    def _render_subrow(
        self,
        subrow: List[dict],
        row_grid: Gtk.Grid,
        current_row: int,
        frame_pairs: int,
        background_color: str | Gdk.RGBA | None,
        label_size_groups: List[Gtk.SizeGroup],
        widget_size_groups: List[Gtk.SizeGroup],
    ) -> int:
        sub_pairs = self._count_pairs(subrow)
        current_col = 0

        for field in subrow:
            ftype = field["type"]
            if ftype == "spacer":
                current_col = self._render_spacer(row_grid, current_row, current_col, field, background_color)
                continue

            current_col = self._render_field(
                row_grid=row_grid,
                row=current_row,
                col=current_col,
                sub_pairs=sub_pairs,
                frame_pairs=frame_pairs,
                field=field,
                background_color=background_color,
                label_size_groups=label_size_groups,
                widget_size_groups=widget_size_groups,
            )

        return current_row + 1

    def _render_spacer(self, _row_grid, row, col, field, background_color) -> int:
        field_id = field.get("id") or f"__sp_{row}_{col}"
        field["id"] = field_id

        row_h = int(field.get("row_height", 0))

        label_fill = Gtk.Box()
        label_fill.set_can_focus(False)
        label_fill.set_sensitive(False)
        label_fill.set_hexpand(True)
        label_fill.set_halign(Gtk.Align.FILL)
        if row_h > 0:
            label_fill.set_size_request(-1, row_h)
        self._apply_background(label_fill, background_color)

        widget_fill = Gtk.Box()
        widget_fill.set_can_focus(False)
        widget_fill.set_sensitive(False)
        widget_fill.set_hexpand(True)
        widget_fill.set_halign(Gtk.Align.FILL)
        if row_h > 0:
            widget_fill.set_size_request(-1, row_h)

        self.types[field_id] = "spacer"
        dummy_label = Gtk.Label(label="")
        self.labels[field_id] = dummy_label
        self.label_boxes[field_id] = label_fill
        self.widgets[field_id] = widget_fill

        meta = self._field_specs.get(field_id, {})
        meta["_creation_index"] = self._creation_index
        self._creation_index += 1

        return col + 1

    def _ensure_help_css(self) -> None:
        if getattr(self, "_help_css_provider", None):
            return
        css = b"""
        .help-btn {
            padding: 0;
            border-width: 0;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
        self._help_css_provider = provider

    def _attach_help(self, widget: Gtk.Widget, field: Dict[str, str], label_text: str) -> Gtk.Widget:
        help_text = field.get("help") or field.get("help_text") or ""
        if not isinstance(help_text, str) or not help_text.strip():
            return widget

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        box.set_hexpand(widget.get_hexpand())
        box.set_halign(Gtk.Align.FILL)

        # Keep widget expanding
        widget.set_hexpand(True)
        box.pack_start(widget, True, True, 0)
        self._ensure_help_css()

        # load original pixbuf once (no scaling yet)
        orig_pix = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.path.dirname(__file__), "assets", "help.png"))

        img = Gtk.Image()  # will set scaled pixbuf later

        btn = Gtk.Button()
        btn.set_image(img)
        btn.set_relief(Gtk.ReliefStyle.NONE)
        btn.set_focus_on_click(False)
        btn.set_tooltip_text("Help")
        btn.get_style_context().add_class("help-btn")

        # no fixed size; we will scale to parent container height
        btn.set_halign(Gtk.Align.CENTER)
        btn.set_valign(Gtk.Align.CENTER)
        btn.set_margin_start(4)

        def _scale_icon_to_alloc(_box_widget, allocation):
            try:
                # target size ~60% of row height, with bounds
                target = max(16, min(48, int(allocation.height * 0.6)))
                if target <= 0:
                    return
                scaled = orig_pix.scale_simple(target, target, GdkPixbuf.InterpType.BILINEAR)
                img.set_from_pixbuf(scaled)
                # keep button slightly larger than image so it doesn't clip
                btn.set_size_request(target + 4, target + 4)
            except Exception:
                pass

        # react to size changes of the HBox that contains the field and the help button
        def _on_size_allocate(widget, allocation):
            _scale_icon_to_alloc(widget, allocation)
        box.connect("size-allocate", _on_size_allocate)

        btn = Gtk.Button()
        btn.set_image(img)
        btn.set_relief(Gtk.ReliefStyle.NONE)
        btn.set_focus_on_click(False)
        btn.set_tooltip_text("Help")
        btn.set_size_request(20, 20)
        btn.set_halign(Gtk.Align.CENTER)
        btn.set_valign(Gtk.Align.CENTER)
        btn.set_margin_top(0)
        btn.set_margin_bottom(0)
        btn.set_margin_start(0)
        btn.set_margin_end(0)
        btn.get_style_context().add_class("help-btn")

        def _open_help(_btn):
            title = label_text or (field.get("id") or "Help")
            self._show_help_dialog(title, help_text)

        btn.connect("clicked", _open_help)
        box.pack_start(btn, False, False, 0)
        return box

    def _show_help_dialog(self, title: str, help_text: str) -> None:
        dlg = Gtk.Dialog(
            title=title,
            transient_for=self._toplevel.get_toplevel() if self._toplevel else None,
            flags=0,
        )
        dlg.add_button("OK", Gtk.ResponseType.OK)
        dlg.set_modal(True)
        dlg.set_destroy_with_parent(True)
        dlg.set_default_response(Gtk.ResponseType.OK)
        dlg.set_resizable(True)
        try:
            dlg.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        except Exception:
            pass

        content = dlg.get_content_area()
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_min_content_width(480)
        scrolled.set_min_content_height(320)

        lbl = Gtk.Label()
        lbl.set_use_markup(True)
        lbl.set_line_wrap(True)
        lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        lbl.set_xalign(0.0)
        lbl.set_halign(Gtk.Align.FILL)
        lbl.set_selectable(True)
        lbl.set_margin_top(8)
        lbl.set_margin_bottom(8)
        lbl.set_margin_start(8)
        lbl.set_margin_end(8)

        markup = self._render_help_markup(help_text)
        try:
            lbl.set_markup(markup)
        except Exception:
            lbl.set_text(help_text)

        scrolled.add(lbl)
        content.add(scrolled)
        content.show_all()

        # Close on focus-out (click outside)
        def _close_on_focus_out(_w, _e):
            try:
                dlg.destroy()
            except Exception:
                pass
            return False

        dlg.connect("focus-out-event", _close_on_focus_out)

        dlg.connect("response", lambda d, r: d.destroy())
        dlg.show_all()

    def _render_help_markup(self, text: str) -> str:
        # Lightweight markdown-like to Pango markup
        s = text or ""
        # Escape
        s = GLib.markup_escape_text(s)

        # Bold: **...**
        s = s.replace("&ast;&ast;", "**")  # undo escape for asterisks if any
        try:
            s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
            # Italic: *...*
            s = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", s)
            # Underline: __...__
            s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)
        except Exception:
            pass

        # Lists: lines starting with - or *
        lines = s.splitlines()
        out = []
        for ln in lines:
            stripped = ln.lstrip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                out.append("• " + stripped[2:])
            else:
                out.append(ln)
        s = "\n".join(out)

        # Paragraphs: double newlines -> extra spacing (use simple <span> + newline)
        paragraphs = s.split("\n\n")
        paragraphs = [p.strip() for p in paragraphs]
        s = "\n\n".join(paragraphs)

        return s

    def _render_field(
        self,
        *,
        row_grid: Gtk.Grid,
        row: int,
        col: int,
        sub_pairs: int,
        frame_pairs: int,
        field: Dict[str, str],
        background_color: str | Gdk.RGBA | None,
        label_size_groups: List[Gtk.SizeGroup],
        widget_size_groups: List[Gtk.SizeGroup],
    ) -> int:
        field_id = field["id"]
        field_type = field["type"]
        label_text, tooltip_text = self._label_for_field(field, field_id)

        self.types[field_id] = field_type
        if "default" in field:
            self.defaults[field_id] = field.get("default")

        is_checkbox = field_type in ("check", "checkbox")
        inline_checkbox = is_checkbox and bool(field.get("inline_label", True))

        # Build label box (also for inline checkboxes so reflow works)
        allow_wrap = is_checkbox  # allow wrapping text for checkboxes in label if needed
        label_box, label_widget = self._build_label_box(
            "" if inline_checkbox else label_text,
            background_color,
            allow_wrap=allow_wrap,
            tooltip_text=(None if inline_checkbox else tooltip_text),
        )
        self.labels[field_id] = label_widget if not inline_checkbox else Gtk.Label()  # placeholder for inline
        self.label_boxes[field_id] = label_box
        meta = self._field_specs.get(field_id, {})
        meta["_creation_index"] = self._creation_index
        self._creation_index += 1
        row_grid.attach(label_box, col * 2, row, 1, 1)
        if self._frame_pairs > 1 and col < len(label_size_groups):
            label_size_groups[col].add_widget(label_widget)

        # Create the actual widget
        if is_checkbox:
            # For inline checkboxes, the checkbutton carries the visible text
            if inline_checkbox:
                check_label, _ = self._label_for_field(field, field_id)
                widget = self._create_check_widget({**field, "label": check_label}, inline_label=True)
            else:
                widget = self._create_check_widget(field, inline_label=False)
        else:
            try:
                widget = self._create_widget_for_field(field, field_type, background_color)
            except Exception:
                widget = None

        if widget is None:
            widget = Gtk.Label(label=f"[unsupported: {field_type}]")
            self.types[field_id] = f"unknown({field_type})"

        # Wrap widget with help button if help/help_text present
        widget = self._attach_help(widget, field, label_text)

        span_rest = bool(field.get("span_rest"))
        widget.set_halign(Gtk.Align.FILL)
        widget.set_hexpand(span_rest)
        self.widgets[field_id] = widget
        widget_span = self._calc_widget_span(span_rest, col, frame_pairs)
        row_grid.attach(widget, col * 2 + 1, row, widget_span, 1)

        if (not span_rest) and col < len(widget_size_groups):
            widget_size_groups[col].add_widget(widget)

        # Show by default — ConditionManager may hide later
        label_box.show()
        widget.show()

        return sub_pairs if span_rest else (col + 1)

    def _pair_span_for(self, spec: dict, col: int) -> int:
        frame_pairs = self._frame_pairs

        sp = 0
        span_pairs = spec.get("span_pairs")
        if isinstance(span_pairs, dict):
            sp = int(span_pairs.get(str(frame_pairs), span_pairs.get("default", 0)) or 0)
        elif isinstance(span_pairs, int):
            sp = span_pairs

        if sp <= 0 and bool(spec.get("span_rest")):
            sp = frame_pairs - col

        if sp <= 0:
            sp = 1

        return max(1, min(sp, frame_pairs - col))

    @staticmethod
    def _calc_widget_span(span_rest: bool, col: int, frame_pairs: int) -> int:
        if not span_rest:
            return 1
        return max(1, 2 * (frame_pairs - col) - 1)

    def _order_key_for(self, field_id: str) -> int:
        spec = self._field_specs.get(field_id, {})
        order = spec.get("order")
        cols = self._frame_pairs

        result = 10_000  # default

        if isinstance(order, dict):
            if str(cols) in order:
                result = int(order[str(cols)])
            elif "default" in order:
                result = int(order["default"])
        elif isinstance(order, str):
            mapping = {}
            for tok in (t.strip() for t in order.split(",") if t.strip()):
                if tok.startswith("c") and ".o" in tok:
                    left, right = tok.split(".o", 1)
                    try:
                        c = int(left[1:])
                        o = int(right)
                        mapping[c] = o
                    except Exception:
                        pass
            result = mapping.get(cols, result)
        else:
            result = int(spec.get("_creation_index", 10_000))

        return result

    def reflow(self) -> None:
        if not self._row_grid:
            return
        for ch in list(self._row_grid.get_children()):
            self._row_grid.remove(ch)
        items = []
        skipped_no_labels = 0
        skipped_not_visible = 0
        skipped_cols_rule = 0
        for fid, _ in self.widgets.items():
            if fid not in self.labels or fid not in self.label_boxes:
                skipped_no_labels += 1
                continue

            spec = self._field_specs.get(fid, {})
            cols_rule = spec.get("show_when_cols_in")
            if isinstance(cols_rule, (list, tuple, set)):
                if self._frame_pairs not in set(int(x) for x in cols_rule):
                    skipped_cols_rule += 1
                    continue

            label_box = self.label_boxes[fid]
            widget = self.widgets[fid]
            if not (label_box.get_visible() and widget.get_visible()):
                skipped_not_visible += 1
                continue
            items.append(fid)
        items.sort(key=self._order_key_for)
        row = 0
        col = 0
        frame_pairs = self._frame_pairs
        for fid in items:
            field_spec = self._field_specs.get(fid, {})
            pair_span = self._pair_span_for(field_spec, col)
            widget_span = 1 if pair_span == 1 else (2 * pair_span - 1)
            label_box = self.label_boxes[fid]
            widget = self.widgets[fid]
            label_box.show()
            widget.show()
            self._row_grid.attach(label_box, col * 2, row, 1, 1)
            self._row_grid.attach(widget, col * 2 + 1, row, widget_span, 1)

            # Add to SizeGroups for alignment
            if self._frame_pairs > 1 and hasattr(self, "_label_size_groups") and col < len(self._label_size_groups):
                label_widget = self.labels.get(fid)
                if label_widget:
                    self._label_size_groups[col].add_widget(label_widget)

            span_rest = pair_span > 1
            if hasattr(self, "_widget_size_groups") and (not span_rest) and col < len(self._widget_size_groups):
                self._widget_size_groups[col].add_widget(widget)

            col += pair_span
            if col >= frame_pairs:
                col = 0
                row += 1
        self._row_grid.show_all()

    def _label_for_field(self, field: Dict[str, str], fallback_id: str) -> tuple[str, str | None]:
        labels = field.get("labels")
        if isinstance(labels, dict) and labels:
            mode = (get_label_mode() or "middle").lower()
            text = (
                labels.get(mode)
                or labels.get("default")
                or labels.get("long")
                or labels.get("middle")
                or labels.get("short")
            )
            tooltip = labels.get("long") or labels.get("default") or text
            return text or fallback_id, tooltip
        base = field.get("label", fallback_id)
        return base, None

    def _build_label_box(
        self,
        label_text: str,
        background_color: str | Gdk.RGBA | None,
        allow_wrap: bool,
        tooltip_text: str | None = None,
    ) -> Tuple[Gtk.Box, Gtk.Label]:
        label = Gtk.Label()
        label.set_use_markup(True)
        label.set_margin_end(5)
        escaped = GLib.markup_escape_text(label_text or "")
        label.set_markup(f"<b><span foreground='black'>{escaped}</span></b>")

        if getattr(self, "_frame_pairs", 1) == 1:
            label.set_line_wrap(False)
            label.set_ellipsize(Pango.EllipsizeMode.END)
            label.set_width_chars(22)

        if allow_wrap:
            label.set_line_wrap(True)
            label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
            label.set_ellipsize(Pango.EllipsizeMode.NONE)
        else:
            label.set_line_wrap(False)
            label.set_ellipsize(Pango.EllipsizeMode.NONE)

        if tooltip_text:
            label.set_tooltip_text(tooltip_text)

        label.set_xalign(1.0)
        label.set_halign(Gtk.Align.END)
        label.set_valign(Gtk.Align.CENTER)
        label.set_hexpand(False)
        label.set_margin_end(5)

        label_box = Gtk.Box()
        label_box.set_halign(Gtk.Align.END)
        label_box.set_hexpand(False)
        self._apply_background(label_box, background_color)
        label_box.pack_start(label, True, True, 0)
        return label_box, label

    def _create_widget_for_field(
        self,
        field: Dict[str, str],
        field_type: str,
        background_color: str | Gdk.RGBA | None,
    ) -> Gtk.Widget:
        if field_type == "entry":
            return self._create_entry_widget(field, background_color)
        if field_type in ("person", "place", "citation"):
            return self._create_dnd_widget(field, field_type)
        if field_type in ("check", "checkbox"):
            return self._create_check_widget(field, inline_label=False)
        return Gtk.Label(label=f"Unknown type: {field_type}")

    # ---------- Entry / Combo -----------

    def _create_entry_widget(self, field: Dict[str, str], background_color: str | Gdk.RGBA | None) -> Gtk.Widget:
        field_id = field["id"]
        input_widget = Gtk.EventBox()
        input_widget.set_border_width(4)

        input_widget.set_size_request(-1, 36)
        input_widget.set_hexpand(False)

        if "options" in field:
            opts = field["options"]
            use_combobox = field.get("use_combobox", False)

            if use_combobox:
                combo = Gtk.ComboBox.new_with_entry()
                combo.set_entry_text_column(0)
                combo.set_hexpand(field.get("span_rest", False))
                if field.get("span_rest"):
                    combo.set_size_request(-1, 30)
                else:
                    width_px = get_person_name_length() * 8
                    if self._frame_pairs == 1:
                        combo.set_size_request(-1, 30)
                    else:
                        combo.set_size_request(width_px, 30)

                model = self.model_manager.ensure_options_model(self.dbstate.db, opts)
                combo.set_model(model)
                combo.set_entry_text_column(0)

                default_text = field.get("default", "") or ""
                entry = combo.get_child()
                if entry and isinstance(entry, Gtk.Entry):
                    entry.set_text(default_text)
                    if not field.get("span_rest"):
                        entry.set_max_width_chars(get_person_name_length())

                    if self._frame_pairs == 1 and not field.get("span_rest"):
                        entry.set_width_chars(1)

                    setup_entry_completion(entry, model)

                    hid = entry.connect("changed", self._on_entry_changed, input_widget)
                    self.changed_handlers[field_id] = hid

                input_widget.default_text = default_text

                GLib.idle_add(self._on_entry_changed, entry, input_widget)
                color = COLOR_FILLED_INPUT if default_text.strip() else background_color
                self._apply_background(input_widget, color)

                input_widget.add(combo)
                if entry and isinstance(entry, Gtk.Entry):
                    input_widget.input = entry
            else:
                # Entry with EntryCompletion

                entry = Gtk.Entry()
                entry.set_hexpand(field.get("span_rest", False))  # Тільки span_rest розтягується
                if field.get("span_rest"):
                    entry.set_hexpand(True)
                    input_widget.set_halign(Gtk.Align.FILL)
                    entry.set_width_chars(1)
                    entry.set_max_width_chars(-1)
                    entry.set_size_request(-1, 30)
                    if self._frame_pairs > 1:
                        if not hasattr(self, "_span_widgets"):
                            self._span_widgets = []
                        self._span_widgets.append(entry)
                else:
                    width_px = get_person_name_length() * 8
                    if self._frame_pairs == 1:
                        entry.set_size_request(-1, 30)
                        entry.set_width_chars(1)
                    else:
                        entry.set_size_request(width_px, 30)
                    entry.set_max_width_chars(get_person_name_length())
                default_text = field.get("default", "") or ""
                entry.set_text(default_text)
                input_widget.default_text = default_text

                model = self.model_manager.ensure_options_model(self.dbstate.db, opts)
                setup_entry_completion(entry, model)

                GLib.idle_add(self._on_entry_changed, entry, input_widget)
                color = COLOR_FILLED_INPUT if default_text.strip() else background_color
                self._apply_background(input_widget, color)

                hid = entry.connect("changed", self._on_entry_changed, input_widget)
                self.changed_handlers[field_id] = hid

                input_widget.add(entry)
                input_widget.input = entry

        else:
            entry = Gtk.Entry()
            entry.set_hexpand(field.get("span_rest", False))
            if field.get("span_rest"):
                entry.set_hexpand(True)
                input_widget.set_halign(Gtk.Align.FILL)
                entry.set_width_chars(1)
                entry.set_max_width_chars(-1)
                entry.set_size_request(-1, 30)
                if self._frame_pairs > 1:
                    if not hasattr(self, "_span_widgets"):
                        self._span_widgets = []
                    self._span_widgets.append(entry)
            else:
                width_px = get_person_name_length() * 8
                if self._frame_pairs == 1:
                    entry.set_size_request(-1, 30)
                    entry.set_width_chars(1)
                else:
                    entry.set_size_request(width_px, 30)
                entry.set_max_width_chars(get_person_name_length())
            default_text = field.get("default", "") or ""
            entry.set_text(default_text)
            input_widget.default_text = default_text

            GLib.idle_add(self._on_entry_changed, entry, input_widget)
            color = COLOR_FILLED_INPUT if default_text.strip() else background_color
            self._apply_background(input_widget, color)

            entry.connect("changed", self._on_entry_changed, input_widget)
            input_widget.add(entry)
            input_widget.input = entry

        input_widget.queue_draw()
        return input_widget

    def _on_entry_changed(self, entry: Gtk.Entry, eventbox: Gtk.EventBox) -> None:
        text = entry.get_text() if entry else ""
        color = COLOR_FILLED_INPUT if (text or "").strip() else COLOR_EMPTY_INPUT
        self._apply_background(eventbox, color)

    # ---------- DnD link widgets -----------

    def _create_dnd_widget(self, field: Dict[str, str], field_type: str) -> Gtk.EventBox:
        field_id = field["id"]
        default_id = field.get("default")

        dnd_widget = self._create_link_widget(field_id, field_type)

        dnd_widget._data_row = self.data_row
        dnd_widget.field_id = field_id
        dnd_widget.field_type = field_type
        dnd_widget.default_id = default_id

        self.dnd_adapter.setup_dnd(dnd_widget, field_type, self._make_drop_callback(field_id, field_type))

        if default_id:
            try:
                obj = None
                if field_type == "place":
                    obj = self.dbstate.db.get_place_from_gramps_id(default_id)
                elif field_type == "person":
                    obj = self.dbstate.db.get_person_from_gramps_id(default_id)
                elif field_type == "citation":
                    obj = self.dbstate.db.get_citation_from_gramps_id(default_id)

                if obj:
                    handle = obj.get_handle()
                    self._store_drop_data(field_id, handle, obj)

                    if field_type == "place":

                        title = place_displayer.display(self.dbstate.db, obj) or ""
                        if len(title) > get_place_title_length():
                            title = title[: get_place_title_length() - 1] + "…"
                        dnd_widget.label.set_markup(f"<u>{title}</u>")
                    elif field_type == "person":

                        name = name_displayer.display(obj) or ""
                        if len(name) > get_person_name_length():
                            name = name[: get_person_name_length() - 1] + "…"
                        dnd_widget.label.set_markup(f"<u>{name}</u>")
                    elif field_type == "citation":

                        txt = getattr(obj, "page", "") or "(no page)"
                        if len(txt) > get_citation_text_length():
                            txt = txt[: get_citation_text_length() - 1] + "…"
                        dnd_widget.label.set_markup(f"<u>Citation: {txt}</u>")

                    self.dnd_adapter._set_dnd_background(dnd_widget, has_object=True)
                    dnd_widget.clear_button.set_opacity(1.0)
                    dnd_widget.clear_button.set_sensitive(True)
                    dnd_widget.queue_draw()
            except Exception:
                pass

        return dnd_widget

    def _update_drag_cursor(self, eventbox: Gtk.EventBox, *, has_object: bool) -> None:
        try:
            eventbox._has_object = bool(has_object)
            if not has_object and eventbox.get_window():
                eventbox.get_window().set_cursor(None)
        except Exception:
            pass

    def _create_link_widget(self, field_id: str, field_type: str) -> Gtk.EventBox:
        rule = None
        for r in get_dnd_rules():
            m = r.get("match", {})
            matched = False
            fid = m.get("field_id")
            if isinstance(fid, dict):
                if "equals" in fid and field_id == fid["equals"]:
                    matched = True
                if "endswith" in fid and field_id.endswith(fid["endswith"]):
                    matched = True
                if "startswith" in fid and field_id.startswith(fid["startswith"]):
                    matched = True
            ftype = m.get("field_type")
            if isinstance(ftype, dict):
                if "equals" in ftype and field_type == ftype["equals"]:
                    matched = matched or True
            if matched:
                rule = r
                break

        default_text = (rule or get_dnd_default())["placeholder"]

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox.set_size_request(-1, 28)  # Fix height to match label
        hbox.set_hexpand(True)

        label = Gtk.Label(label=default_text, xalign=0)
        label.set_use_markup(True)
        label.set_width_chars(1)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_size_request(-1, 28)
        label.set_valign(Gtk.Align.CENTER)
        label.set_vexpand(False)

        eventbox_for_label = Gtk.EventBox()
        eventbox_for_label.add(label)
        eventbox_for_label.set_visible_window(True)  # Need visible window for clicks
        eventbox_for_label.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        eventbox_for_label.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 0, 0, 0))  # Transparent

        # Drag grip
        drag_handle = Gtk.Label()
        drag_handle.set_text("∷")
        drag_handle.set_size_request(20, -1)
        drag_handle.set_halign(Gtk.Align.CENTER)
        drag_handle.set_valign(Gtk.Align.CENTER)
        drag_handle.set_tooltip_text("Drag to move object")
        drag_handle.set_markup('<span color="#666666" size="large"> ∷ </span>')

        drag_handle.connect(
            "enter-notify-event",
            lambda w, e: (w.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.FLEUR)) if w.get_window() else None),
        )
        drag_handle.connect(
            "leave-notify-event",
            lambda w, e: w.get_window().set_cursor(None) if w.get_window() else None,
        )
        drag_handle.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)

        clear_button = Gtk.Button()
        clear_button.set_label("×")
        clear_button.set_size_request(28, 28)
        clear_button.set_tooltip_text("Clear")
        clear_button.set_opacity(0.0)  # Start invisible
        clear_button.set_sensitive(False)

        hbox.pack_start(drag_handle, False, False, 2)
        hbox.pack_start(eventbox_for_label, False, False, 0)
        hbox.pack_start(Gtk.Label(), True, True, 0)  # spacer
        hbox.pack_start(clear_button, False, False, 0)

        eventbox = Gtk.EventBox()
        eventbox.add(hbox)
        eventbox.set_visible_window(True)
        eventbox.set_border_width(4)
        eventbox.set_size_request(-1, 36)
        eventbox.set_hexpand(True)

        rgba = Gdk.RGBA()
        rgba.parse(COLOR_EMPTY_DND)
        eventbox.override_background_color(Gtk.StateFlags.NORMAL, rgba)

        eventbox.label = label
        eventbox.field_id = field_id
        eventbox.clear_button = clear_button
        eventbox.default_text = default_text
        eventbox.hbox = hbox
        eventbox.drag_handle = drag_handle

        eventbox._has_object = False

        def _on_enter(w, _e):
            if getattr(w, "_has_object", False) and w.get_window():
                w.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.FLEUR))

        def _on_leave(w, _e):
            if w.get_window():
                w.get_window().set_cursor(None)

        eventbox.connect("enter-notify-event", _on_enter)
        eventbox.connect("leave-notify-event", _on_leave)
        eventbox.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | Gdk.EventMask.LEAVE_NOTIFY_MASK)

        clear_button.connect("clicked", self._on_clear_field, eventbox)
        eventbox_for_label.connect("button-press-event", self._on_click)
        eventbox_for_label.field_id = field_id
        eventbox_for_label.field_type = field_type
        return eventbox

    # ---------- Checkbox -----------

    def _create_check_widget(self, field: Dict[str, str], inline_label: bool) -> Gtk.CheckButton:
        chk = Gtk.CheckButton.new_with_label(field.get("label", "")) if inline_label else Gtk.CheckButton()

        self._ensure_checkbox_css()
        chk.get_style_context().add_class("check-large")
        chk.set_size_request(-1, 32)

        if inline_label:
            lbl = chk.get_child()
            if isinstance(lbl, Gtk.Label):
                lbl.set_line_wrap(True)
                lbl.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                lbl.set_xalign(0.0)
                max_chars = int(field.get("max_label_chars", 0) or 0)
                if max_chars > 0:
                    lbl.set_max_width_chars(max_chars)
            if not field.get("label"):
                txt, _ = self._label_for_field(field, field.get("id", ""))
                chk.set_label(txt or "")

        raw_default = field.get("default", False)
        default_bool = parse_bool_from_string(raw_default)
        chk.set_active(default_bool)
        self.defaults[field["id"]] = default_bool

        tip = field.get("tooltip")
        if not tip and isinstance(field.get("labels"), dict):
            tip = field["labels"].get("long")
        if tip:
            chk.set_tooltip_text(str(tip))

        return chk

    def _ensure_checkbox_css(self) -> None:
        if self._checkbox_css_provider:
            return
        css = b"""
        .check-large check {
            min-width: 20px;
            min-height: 20px;
        }
        .check-large {
            padding-top: 2px;
            padding-bottom: 2px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER,
        )
        self._checkbox_css_provider = provider

    def _apply_background(self, widget: Gtk.Widget, color: str | Gdk.RGBA | None) -> None:
        if isinstance(color, str):
            rgba = Gdk.RGBA()
            rgba.parse(color)
        elif isinstance(color, Gdk.RGBA):
            rgba = color
        else:
            return

        widget.override_background_color(Gtk.StateFlags.NORMAL, rgba)

        if not self._entry_sel_provider:
            css = b"#form-entry selection { background-color: #d0d0d0; color: #222; }"
            self._entry_sel_provider = Gtk.CssProvider()
            self._entry_sel_provider.load_from_data(css)

        if isinstance(widget, Gtk.EventBox):
            child = widget.get_child()

            def _style_entry(entry: Gtk.Entry):
                entry.override_background_color(Gtk.StateFlags.NORMAL, rgba)
                entry.set_name("form-entry")
                ctx = entry.get_style_context()
                try:
                    ctx.add_provider(self._entry_sel_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
                except Exception:
                    Gtk.StyleContext.add_provider_for_screen(
                        Gdk.Screen.get_default(),
                        self._entry_sel_provider,
                        Gtk.STYLE_PROVIDER_PRIORITY_USER,
                    )

            if isinstance(child, Gtk.ComboBox):
                entry = child.get_child()
                if entry and isinstance(entry, Gtk.Entry):
                    _style_entry(entry)
            elif isinstance(child, Gtk.Entry):
                _style_entry(child)

    def _on_clear_field(self, _button: Gtk.Button, eventbox: Gtk.EventBox) -> None:
        field_id = eventbox.field_id
        self.objects.pop(field_id, None)
        self.handles.pop(field_id, None)
        eventbox.label.set_text(eventbox.default_text)
        rgba = Gdk.RGBA()
        rgba.parse(COLOR_EMPTY_DND)
        eventbox.override_background_color(Gtk.StateFlags.NORMAL, rgba)
        eventbox.clear_button.set_opacity(0.0)
        eventbox.clear_button.set_sensitive(False)

        self._update_drag_cursor(eventbox, has_object=False)

        if hasattr(eventbox, "_data_row") and eventbox._data_row and hasattr(eventbox._data_row, "_trigger_sync"):
            try:
                eventbox._data_row._trigger_sync()
            except Exception:
                pass

    def _make_drop_callback(self, field_id: str, field_type: str):
        def callback(widget, drag_context, x, y, data, info, time, _user_data):
            self.dnd_adapter.handle_drop(
                widget,
                drag_context,
                x,
                y,
                data,
                info,
                time,
                field_type,
                lambda handle, obj: self._store_drop_data(field_id, handle, obj),
            )

        return callback

    def _store_drop_data(self, field_id: str, handle: str, obj: object) -> None:
        self.handles[field_id] = handle
        self.objects[field_id] = obj

        widget = self.widgets.get(field_id)
        if isinstance(widget, Gtk.EventBox):
            self._update_drag_cursor(widget, has_object=True)

        # Trigger live-sync update after DnD
        if self.data_row and hasattr(self.data_row, "_trigger_sync") and callable(self.data_row._trigger_sync):
            self.data_row._trigger_sync()

    def _on_click(self, widget: Gtk.Widget, event: Gdk.Event) -> bool | None:
        if event.type != Gdk.EventType.BUTTON_PRESS or event.button != 1:
            return
        field_id = getattr(widget, "field_id", None)
        field_type = getattr(widget, "field_type", None) or self.types.get(field_id)
        handle = self.handles.get(field_id)
        if not (field_id and field_type and handle):
            return
        try:
            if field_type == "place":
                obj = self.dbstate.db.get_place_from_handle(handle)
                if obj:
                    EditPlace(self.dbstate, self.uistate, [], obj)
            elif field_type == "citation":
                obj = self.dbstate.db.get_citation_from_handle(handle)
                if obj:
                    EditCitation(self.dbstate, self.uistate, [], obj)
            elif field_type == "person":
                obj = self.dbstate.db.get_person_from_handle(handle)
                if obj:
                    EditPerson(self.dbstate, self.uistate, [], obj)
        except WindowActiveError:
            return
