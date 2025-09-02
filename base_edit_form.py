from __future__ import annotations

import re
from typing import Any

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position

from gi.repository import Gdk, GLib, Gtk
from gramps.gui.ddtargets import DdTargets

from configs.constants import (
    FORM_WINDOW_ALLOW_VSCROLL,
    FORM_WINDOW_ANCHOR,
    FORM_WINDOW_KEEP_ABOVE,
    FORM_WINDOW_MAX_HEIGHT,
    FORM_WINDOW_MODE,
    FORM_WINDOW_PER_FORM,
    FORM_WINDOW_REMEMBER_POSITION,
    FORM_WINDOW_SKIP_PAGER,
    FORM_WINDOW_SKIP_TASKBAR,
    FORM_WINDOW_TYPE_HINT,
    get_tab_mode,
    sync_label_mode_from_density,
    sync_tab_mode_from_density,
)
from lookups.providers import clear_options_cache, set_runtime_db
from services.geom_prefs import load_pos, save_pos
from services.id_collector import IdCollector
from services.state_collector import StateCollector
from services.validator_base import ValidatorBase
from services.work_context import WorkContext
from settings.settings_manager import get_settings_manager
from uhelpers.density_helper import get_density_settings
from ui.data_row import DataRow
from ui.drag_drop_adapter import DragDropAdapter
from ui.shared_cache import UI_MODEL_CACHE
from providers import FORM_REGISTRY

try:
    Gtk.Settings.get_default().set_property("gtk-enable-animations", False)
except (AttributeError, TypeError):
    pass


class BaseEditForm(Gtk.Window):

    def __init__(self, *, dbstate: Any, uistate: Any, form_id: str) -> None:
        super().__init__()

        self._drag_tab_switch_delay_ms: int = 250
        self._tab_hover_timer: int | None = None
        self._tab_switch_tid: int | None = None
        self._is_closing: bool = False

        self.dbstate = dbstate
        self.uistate = uistate
        self.form_id = form_id
        self._tab_labels = {}
        self._tabs_specs = {}
        self._notebook = None

        self._live_signal_ids: list[tuple[Gtk.Widget, int]] = []

        set_runtime_db(self.dbstate.db)
        clear_options_cache()

        self.rows: list[DataRow] = []
        self.form_state = self.make_form_state()
        self.work_context = WorkContext()

        form_config = self.get_form_config()
        title = form_config.get("title", form_id)
        self.set_title(f"🇺🇦 UARecords — {title}")
        self.set_default_size(1000, 600)

        self._pos_applied: bool = False

        if FORM_WINDOW_REMEMBER_POSITION:
            self.connect("map-event", self._on_map_event_apply_position)

        self.dnd_adapter = DragDropAdapter(dbstate, uistate)
        self._tabs_specs: dict[str, dict] = {}
        self._build_gui(form_config)

        self.connect("delete-event", self._on_delete_event)

    def _on_map_event_apply_position(self, _widget: Gtk.Window, _event: Gdk.Event) -> bool:
        if self._pos_applied or not FORM_WINDOW_REMEMBER_POSITION:
            return False
        try:
            rec = load_pos(self.form_id if FORM_WINDOW_PER_FORM else "__default__")
            if not rec:
                self._pos_applied = True
                return False

            anchor = str(rec.get("anchor") or FORM_WINDOW_ANCHOR).lower()
            x_off = int(rec.get("x", 0))
            y_off = int(rec.get("y", 0))

            w, h = self.get_size()

            screen = self.get_screen()
            sw = screen.get_width()
            sh = screen.get_height()

            if anchor == "topleft":
                x, y = x_off, y_off
            elif anchor == "topright":
                x, y = max(0, sw - x_off - w), y_off
            elif anchor == "bottomleft":
                x, y = x_off, max(0, sh - y_off - h)
            elif anchor == "bottomright":
                x, y = max(0, sw - x_off - w), max(0, sh - y_off - h)
            else:
                x, y = x_off, y_off

            x = max(0, min(x, max(0, sw - w)))
            y = max(0, min(y, max(0, sh - h)))

            self.move(int(x), int(y))
        except Exception:
            pass
        finally:
            self._pos_applied = True
        return False

    def _apply_window_behavior(self) -> None:
        """
        - keep_above
        - window type hint
        - skip taskbar/pager
        """

        try:
            mode = get_settings_manager().get_window_mode()
        except Exception:
            mode = FORM_WINDOW_MODE or "transient"
        mode = mode.lower()

        # Set window type hint based on mode
        hint_map = {
            "normal": Gdk.WindowTypeHint.NORMAL,
            "dialog": Gdk.WindowTypeHint.DIALOG,
            "utility": Gdk.WindowTypeHint.UTILITY,
        }
        try:
            if mode == "detached":
                self.set_type_hint(Gdk.WindowTypeHint.NORMAL)
            else:
                self.set_type_hint(hint_map.get(FORM_WINDOW_TYPE_HINT, Gdk.WindowTypeHint.DIALOG))
        except Exception:
            pass

        try:
            if self.get_modal():
                self.set_modal(False)
        except Exception:
            pass

        try:
            self.set_transient_for(None)
        except Exception:
            pass

        try:
            self.set_destroy_with_parent(False)
        except Exception:
            pass

        parent = None
        if mode == "detached":
            pass
        elif mode in ("transient", "modal"):
            parent = self._guess_gramps_main_window()
            if parent:
                try:
                    self.set_transient_for(parent)
                    self.set_destroy_with_parent(True)
                except Exception:
                    pass
            if mode == "modal":
                try:
                    self.set_modal(True)
                except Exception:
                    pass

        try:
            keep_above = get_settings_manager().get_window_keep_above()
        except Exception:
            keep_above = bool(FORM_WINDOW_KEEP_ABOVE)

        try:
            self.set_keep_above(keep_above)
        except Exception:
            pass

        try:
            self.set_skip_taskbar_hint(bool(FORM_WINDOW_SKIP_TASKBAR))
        except Exception:
            pass
        try:
            self.set_skip_pager_hint(bool(FORM_WINDOW_SKIP_PAGER))
        except Exception:
            pass

    def _guess_gramps_main_window(self) -> Gtk.Window | None:
        try:
            cand = getattr(self.uistate, "window", None)
            if isinstance(cand, Gtk.Window):
                return cand
            if hasattr(cand, "get_toplevel"):
                tl = cand.get_toplevel()
                if isinstance(tl, Gtk.Window):
                    return tl
        except Exception:
            pass

        try:
            for w in Gtk.Window.list_toplevels():
                if isinstance(w, Gtk.Window):
                    title = ""
                    try:
                        title = w.get_title() or ""
                    except Exception:
                        title = ""
                    if "gramps" in title.lower():
                        return w
        except Exception:
            pass

        try:
            for w in Gtk.Window.list_toplevels():
                if isinstance(w, Gtk.Window) and w.is_active():
                    return w
        except Exception:
            pass

        return None

    def get_form_config(self) -> dict:
        raise NotImplementedError

    def make_form_state(self):
        raise NotImplementedError

    def make_validator(self, form_state):
        raise NotImplementedError

    def make_ai_builder(self):
        raise NotImplementedError

    def get_reconciler(self):
        raise NotImplementedError

    def make_processor(self, work_context):
        raise NotImplementedError

    def _build_gui(self, form_config: dict) -> None:

        density = get_density_settings()
        cols = int(form_config.get("columns", 3))

        label_size_groups = []
        widget_size_groups = []
        for _ in range(cols):
            label_size_groups.append(Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL))
            widget_size_groups.append(Gtk.SizeGroup(mode=Gtk.SizeGroupMode.HORIZONTAL))

        main_vbox = Gtk.VBox(spacing=10)
        main_vbox.set_margin_top(density["grid_margin"])
        main_vbox.set_margin_bottom(density["grid_margin"])
        main_vbox.set_margin_left(density["grid_margin"])
        main_vbox.set_margin_right(density["grid_margin"])

        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        notebook.set_hexpand(True)
        notebook.set_vexpand(True)
        notebook.set_scrollable(True)
        self._notebook = notebook

        self._create_tabs(notebook, form_config, cols, label_size_groups, widget_size_groups, density)

        content_widget: Gtk.Widget = notebook
        try:
            allow_scroll = bool(FORM_WINDOW_ALLOW_VSCROLL)
            max_h = int(FORM_WINDOW_MAX_HEIGHT or 0)
            if allow_scroll and max_h > 0:
                scrolled = Gtk.ScrolledWindow()
                scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
                scrolled.set_hexpand(True)
                scrolled.set_vexpand(True)

                if hasattr(scrolled, "set_max_content_height"):
                    scrolled.set_max_content_height(max_h)
                    if hasattr(scrolled, "set_propagate_natural_height"):
                        scrolled.set_propagate_natural_height(True)
                else:
                    scrolled.set_size_request(-1, max_h)
                    scrolled.set_vexpand(False)

                scrolled.add(notebook)
                content_widget = scrolled
            else:
                try:
                    notebook.set_size_request(-1, -1)
                except Exception:
                    pass
                notebook.set_hexpand(True)
                notebook.set_vexpand(True)
        except Exception:
            content_widget = notebook

        buttons_box = self._create_buttons(density)

        main_vbox.pack_start(content_widget, True, True, 0)
        main_vbox.pack_start(buttons_box, False, False, 0)

        self.add(main_vbox)
        self._apply_window_behavior()
        self.show_all()
        self._enable_live_sync()

    def _tab_at_pos(self, notebook: Gtk.Notebook, x: int, y: int) -> int:
        """Find which tab is at given coordinates."""
        for i in range(notebook.get_n_pages()):
            child = notebook.get_nth_page(i)
            tab_label = notebook.get_tab_label(child)
            if tab_label:
                allocation = tab_label.get_allocation()
                if (
                    allocation.x <= x <= allocation.x + allocation.width
                    and allocation.y <= y <= allocation.y + allocation.height
                ):
                    return i
        return -1

    def _enable_tab_switch_on_drag(self, notebook: Gtk.Notebook, delay_ms: int | None = None) -> None:
        if delay_ms is None:
            delay_ms = getattr(self, "_drag_tab_switch_delay_ms", 100)
        self._drag_tab_switch_delay_ms = delay_ms

        try:
            notebook.drag_dest_set(Gtk.DestDefaults.MOTION, [], Gdk.DragAction.COPY)
        except Exception:
            pass

        if getattr(self, "_tab_hover_timer", None):
            try:
                GLib.source_remove(self._tab_hover_timer)
            except Exception:
                pass
            self._tab_hover_timer = None

        def on_drag_motion(widget: Gtk.Notebook, _context: Gdk.DragContext, x: int, y: int, _time: int) -> bool:
            try:
                page = self._tab_at_pos(widget, x, y)
                cur = widget.get_current_page()
                if page >= 0 and page != cur:
                    if getattr(self, "_tab_hover_timer", None):
                        try:
                            GLib.source_remove(self._tab_hover_timer)
                        except Exception:
                            pass
                        self._tab_hover_timer = None

                    def _switch():
                        try:
                            widget.set_current_page(page)
                        finally:
                            self._tab_hover_timer = None
                        return False

                    self._tab_hover_timer = GLib.timeout_add(self._drag_tab_switch_delay_ms, _switch)
            except Exception:
                pass
            return False

        def on_drag_leave(_widget: Gtk.Notebook, _context: Gdk.DragContext, _time: int) -> None:
            if getattr(self, "_tab_hover_timer", None):
                try:
                    GLib.source_remove(self._tab_hover_timer)
                except Exception:
                    pass
                self._tab_hover_timer = None

        notebook.connect("drag-motion", on_drag_motion)
        notebook.connect("drag-leave", on_drag_leave)

    def _setup_drag_tab_autoswitch(self, notebook: Gtk.Notebook) -> None:
        self._tab_switch_tid: int | None = None

        def _hook_all_labels() -> None:
            n = notebook.get_n_pages()
            for idx in range(n):
                self._wrap_tab_label_for_dnd(notebook, idx)

        _hook_all_labels()

        def _on_page_added(nb, _child, page_num):
            try:
                self._wrap_tab_label_for_dnd(nb, int(page_num))
            except Exception:
                pass

        notebook.connect("page-added", _on_page_added)

    def _wrap_tab_label_for_dnd(self, notebook: Gtk.Notebook, page_index: int) -> None:

        child = notebook.get_nth_page(page_index)
        if not child:
            return

        tab_widget = notebook.get_tab_label(child)
        if tab_widget is None:
            title = None
            try:
                title = notebook.get_tab_label_text(child)
            except Exception:
                title = None
            if not title:
                title = f"Tab {page_index + 1}"
            lbl = Gtk.Label(label=title)
            lbl.show()
            notebook.set_tab_label(child, lbl)
            tab_widget = lbl
        else:
            if isinstance(tab_widget, Gtk.EventBox) and getattr(tab_widget, "_ua_autoswitch_wrapped", False):
                inner = tab_widget.get_child()
                if isinstance(inner, Gtk.Widget):
                    tab_widget = inner

        targets = [
            DdTargets.PERSON_LINK.target(),
            DdTargets.PLACE_LINK.target(),
            DdTargets.CITATION_LINK.target(),
        ]
        tab_widget.drag_dest_set(Gtk.DestDefaults.MOTION, targets, Gdk.DragAction.COPY)
        tab_widget._tab_index = page_index

        def _cancel():
            self._cancel_tab_switch_timer()

        def on_drag_motion(widget: Gtk.Widget, _context: Gdk.DragContext, _x: int, _y: int, _time: int) -> bool:
            idx = getattr(widget, "_tab_index", -1)
            if idx < 0:
                _cancel()
                return True
            cur = notebook.get_current_page()
            if cur == idx:
                _cancel()
                return True

            _cancel()

            def _fire():
                try:
                    if notebook.get_current_page() != idx:
                        notebook.set_current_page(idx)
                finally:
                    self._tab_switch_tid = None
                return False

            self._tab_switch_tid = GLib.timeout_add(250, _fire)
            return True

        def on_drag_leave(_widget: Gtk.Widget, _context: Gdk.DragContext, _time: int) -> None:
            _cancel()

        tab_widget.connect("drag-motion", on_drag_motion)
        tab_widget.connect("drag-leave", on_drag_leave)

    def _tab_idx_at_pos(self, x: int, y: int) -> int | None:
        nb = getattr(self, "_notebook", None)
        if not nb:
            return None

        n = nb.get_n_pages()
        for i in range(n):
            child = nb.get_nth_page(i)
            if not child:
                continue
            tab = nb.get_tab_label(child)
            if not tab or not tab.get_visible():
                continue

            try:
                ok, lx, ly = nb.translate_coordinates(tab, x, y)
            except Exception:
                ok = False

            if not ok:
                continue

            alloc = tab.get_allocation()
            if 0 <= lx < alloc.width and 0 <= ly < alloc.height:
                return i

        return None

    def _cancel_tab_switch_timer(self) -> None:
        if getattr(self, "_tab_switch_tid", None):
            try:
                GLib.source_remove(self._tab_switch_tid)
            except Exception:
                pass
            self._tab_switch_tid = None

    def _enable_live_sync(self) -> None:

        def _resync(*_a):
            try:
                snap = self.collect_snapshot_dict()
                self.form_state.update_from_dict(snap)
            except Exception:
                pass

        for w, hid in getattr(self, "_live_signal_ids", []):
            try:
                w.handler_disconnect(hid)
            except Exception:
                pass
        self._live_signal_ids = []

        for row in self.rows:
            row._trigger_sync = _resync

            for w in row.widgets.values():
                entry = None
                if isinstance(w, Gtk.EventBox):
                    child = w.get_child()
                    if isinstance(child, Gtk.ComboBox):
                        entry = child.get_child()
                    elif isinstance(child, Gtk.Entry):
                        entry = child
                elif isinstance(w, Gtk.Entry):
                    entry = w

                if isinstance(entry, Gtk.Entry):
                    hid = entry.connect("changed", lambda _e, _row=row: _resync())
                    self._live_signal_ids.append((entry, hid))

                # CheckButton
                if isinstance(w, Gtk.CheckButton):
                    hid = w.connect("toggled", lambda _b, _row=row: _resync())
                    self._live_signal_ids.append((w, hid))

                if isinstance(w, Gtk.EventBox) and hasattr(w, "clear_button"):
                    try:
                        hid_c = w.clear_button.connect("clicked", lambda *_a, _row=row: _resync())
                        self._live_signal_ids.append((w.clear_button, hid_c))
                        hid_d = w.connect("drag-data-received", lambda *_a, _row=row: GLib.idle_add(_resync))
                        self._live_signal_ids.append((w, hid_d))
                    except Exception:
                        pass

    def _create_tabs(
        self,
        notebook: Gtk.Notebook,
        form_config: dict,
        cols: int,
        label_size_groups: list[Gtk.SizeGroup],
        widget_size_groups: list[Gtk.SizeGroup],
        density: dict,
    ) -> None:
        for t_idx, tab_config in enumerate(form_config.get("tabs", [])):
            tab_name = tab_config.get("title", tab_config.get("id", f"Tab {t_idx+1}"))
            tab_grid = self._create_tab_grid(density)
            current_row = 0

            for f_idx, frame_config in enumerate(tab_config.get("frames", [])):
                prefix = frame_config.get("prefix") or self._infer_prefix(frame_config, tab_config, f_idx)
                fields = frame_config.get("fields", [])
                row = DataRow(
                    tab_grid,
                    current_row,
                    dbstate=self.dbstate,
                    uistate=self.uistate,
                    dnd_adapter=self.dnd_adapter,
                    fields=self._prefix_fields(fields, prefix, cols),
                    group_title=frame_config.get("title", ""),
                    prefix=prefix,
                    background_color=self._parse_color(
                        frame_config.get("background_color", "Gdk.RGBA(0.95, 0.98, 0.95, 0.0)")
                    ),
                    label_size_groups=label_size_groups,
                    widget_size_groups=widget_size_groups,
                    columns=cols,
                )
                self.rows.append(row)
                current_row += 1

            tab_id = tab_config.get("id", f"tab_{t_idx+1}")
            self._tabs_specs[tab_id] = tab_config
            label = Gtk.Label()
            label.set_use_markup(True)
            label.set_xalign(0.0)
            titles = tab_config.get("titles", {})

            label_text = titles.get(get_tab_mode()) or titles.get("default") or tab_name
            tooltip_text = titles.get("long") or titles.get("default") or tab_name

            label = Gtk.Label()
            label.set_use_markup(True)
            label.set_xalign(0.0)
            label.set_markup(GLib.markup_escape_text(label_text))
            label.set_tooltip_text(tooltip_text)

            self._tab_labels[tab_id] = label
            notebook.append_page(tab_grid, label)
        self._update_tab_titles(cols)

    def _update_tab_titles(self, _cols_unused: int) -> None:
        for tab_id, label in self._tab_labels.items():
            spec = self._tabs_specs.get(tab_id, {})
            titles = spec.get("titles", {})
            base = spec.get("title", spec.get("id", tab_id))
            mode = get_tab_mode()
            text = titles.get(mode) or titles.get("default") or base
            try:
                label.set_markup(GLib.markup_escape_text(text))
                label.set_tooltip_text(titles.get("long") or titles.get("default") or base)
                label.queue_draw()
            except Exception:
                pass

    def _infer_prefix(self, frame_config: dict, tab_config: dict, f_idx: int) -> str:
        def _head_from_id(s: str) -> str | None:
            if isinstance(s, str) and "." in s:
                return s.split(".", 1)[0]
            return None

        for fld in frame_config.get("fields", []):
            t = fld.get("type")
            fid = fld.get("id")
            if t in {"entry", "person", "place", "citation", "checkbox", "check"}:
                head = _head_from_id(fid)
                if head:
                    return head
        tab_id = tab_config.get("id", "tab")
        return f"{tab_id}_{f_idx+1}"

    def _create_tab_grid(self, density: dict) -> Gtk.Grid:
        """Create a grid for a tab with proper spacing."""
        grid = Gtk.Grid(
            column_spacing=density["grid_column_spacing"],
            row_spacing=density["grid_row_spacing"],
            margin=10,
        )
        return grid

    def _parse_color(self, color_str: str) -> Gdk.RGBA:
        """Parse color string to Gdk.RGBA object."""
        if isinstance(color_str, str) and color_str.startswith("Gdk.RGBA"):
            # Extract numbers from "Gdk.RGBA(0.98, 0.94, 0.85, 0.3)"

            numbers = re.findall(r"[\d.]+", color_str)
            if len(numbers) == 4:
                return Gdk.RGBA(float(numbers[0]), float(numbers[1]), float(numbers[2]), float(numbers[3]))
        # Default color
        return Gdk.RGBA(0.95, 0.98, 0.95, 0.0)

    def _create_buttons(self, density: dict) -> Gtk.Box:
        """Create buttons box."""
        btn_save = Gtk.Button(label="Зберегти")
        btn_save.set_margin_top(density["button_margin_top"])
        btn_save.set_halign(Gtk.Align.END)
        btn_save.connect("clicked", self._on_save)

        btn_copy = Gtk.Button(label="Копіювати Gramps ID")
        btn_copy.set_margin_top(density["button_margin_top"])
        btn_copy.set_halign(Gtk.Align.END)
        btn_copy.connect("clicked", self._on_copy_ids)

        btn_reset = Gtk.Button(label="Швидкий рестарт")
        btn_reset.set_margin_top(density["button_margin_top"])
        btn_reset.set_halign(Gtk.Align.END)
        btn_reset.connect("clicked", self._on_reset)

        btn_refresh = Gtk.Button(label="Оновити списки + Рестарт")
        btn_refresh.set_margin_top(density["button_margin_top"])
        btn_refresh.set_halign(Gtk.Align.END)
        btn_refresh.connect("clicked", self._on_refresh_options)

        buttons_box = Gtk.Box(spacing=10)
        buttons_box.set_halign(Gtk.Align.END)
        buttons_box.pack_start(btn_refresh, False, False, 0)
        buttons_box.pack_start(btn_reset, False, False, 0)
        buttons_box.pack_start(btn_copy, False, False, 0)
        buttons_box.pack_start(btn_save, False, False, 0)

        return buttons_box

    def _prefix_fields(self, fields: list[dict], prefix: str, cols: int) -> list[list[dict]]:
        if not fields:
            return []

        flat: list[dict] = fields if (fields and isinstance(fields[0], dict)) else [f for row in fields for f in row]

        prefixed = []
        for f in flat:
            fid = f.get("id")
            if isinstance(fid, str) and fid:
                f = {**f, "id": f"{prefix}_{fid}"}
            prefixed.append(f)

        return [prefixed[i : i + cols] for i in range(0, len(prefixed), cols)]

    def _on_copy_ids(self, _button: Gtk.Button) -> None:

        def _gid_from_obj(o: object) -> str | None:
            try:
                if o and hasattr(o, "get_gramps_id"):
                    s = (o.get_gramps_id() or "").strip()
                    return s or None
            except Exception:
                pass
            return None

        def _gid_from_handle(field_type: str, handle: str) -> str | None:
            try:
                if not handle:
                    return None
                if field_type == "person":
                    obj = self.dbstate.db.get_person_from_handle(handle)
                elif field_type == "place":
                    obj = self.dbstate.db.get_place_from_handle(handle)
                elif field_type == "citation":
                    obj = self.dbstate.db.get_citation_from_handle(handle)
                else:
                    obj = None
                return _gid_from_obj(obj)
            except Exception:
                return None

        ids: set[str] = set()

        try:
            if getattr(self, "state", None):
                ids |= IdCollector.collect_from_state(self.form_state)
        except Exception:
            pass

        for row in self.rows:
            for field_id, handle in row.handles.items():
                obj = row.objects.get(field_id)
                gid = _gid_from_obj(obj)
                if not gid:
                    ftype = row.types.get(field_id) or ""
                    gid = _gid_from_handle(ftype, handle)
                if gid:
                    ids.add(gid)

        try:
            temp_state = self.make_form_state()
            for row in self.rows:
                StateCollector.collect_row(row, temp_state, allow_log=False)
            ids |= IdCollector.collect_from_state(temp_state)
        except Exception:
            pass

        text = IdCollector.to_text(ids)
        if text:
            clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
            clipboard.set_text(text, -1)
            clipboard.store()
            self._show_info_dialog("Скопійовано Gramps ID:", text)
        else:
            self._show_info_dialog("Немає даних", "Немає об'єктів із Gramps ID для копіювання.")

    def _on_refresh_options(self, button: Gtk.Button | None) -> None:
        if button:
            button.set_sensitive(False)
        clear_options_cache()
        UI_MODEL_CACHE.clear()

        get_settings_manager.cache_clear()
        sync_label_mode_from_density()
        sync_tab_mode_from_density()

        # Update tab titles with new mode
        if hasattr(self, "_notebook"):
            self._update_tab_titles(getattr(self, "_current_cols", 3))

        try:
            w, _ = self.get_size()
            x, y = self.get_position()
        except Exception:
            w = x = y = None
        new_win = self.__class__(dbstate=self.dbstate, uistate=self.uistate, form_id=self.form_id)
        if w and w > 0:
            new_win.resize(w, -1)  # Keep width, let GTK calculate height
        if x is not None and y is not None:
            new_win.move(x, y)
        self.destroy()

    def _on_reset(self, _button: Gtk.Button) -> None:
        self._reset_form_to_config_defaults()

    def _reset_form_to_config_defaults(self) -> None:
        self.form_state = self.make_form_state()
        gdk_win = self.get_window()
        if gdk_win:
            gdk_win.freeze_updates()
        try:
            for row in self.rows:
                row.reset_to_defaults()
        finally:
            if gdk_win:
                gdk_win.thaw_updates()
            self.queue_draw()

    def _on_save(self, _button: Gtk.Button) -> None:
        self.work_context.reset()
        self.form_state = self.make_form_state()
        self.form_state.update_from_dict(self.collect_snapshot_dict())
        self.work_context.form_state = self.form_state
        self.work_context.db = self.dbstate.db

        # 1) Валідація через провайдера (показує діалог і виходить, якщо є помилки)
        if not self._run_validation_via_provider():
            print("[on_save] Валідація не пройдена — збереження перервано.")
            return

        # 2) Створюємо процесор
        processor = None
        try:
            processor = self.make_processor(self.work_context)
        except Exception as e:
            print(f"[on_save] Помилка створення процесора: {e}")

        if not processor:
            print("[on_save] Процесор відсутній. Метод спрацював, але реалізація ще не готова (no-op).")
            self._show_info_dialog("Збереження", "Обробник змін поки не налаштований.")
            return
        
        # 3) STAGE: рахуємо різниці (baseline/after/ops/errors)
        try:
            staging = processor.stage()
            print(f"[on_save] STAGE готово: ops={len(staging.ops)}, errors={len(staging.errors)}")
        except Exception as e:
            print(f"[on_save] Помилка підготовки змін (stage): {e}")
            self._show_info_dialog("Помилка", f"Не вдалося підготувати зміни: {e}")
            return

        # 4) Якщо HV-валідація знайшла помилки — показуємо й зупиняємось
        if staging.errors:
            msg = "Знайдено помилки у графі змін:\n• " + "\n• ".join(staging.errors[:10])
            if len(staging.errors) > 10:
                msg += f"\n… та ще {len(staging.errors) - 10}"
            self._show_info_dialog("Помилки перевірки змін", msg)
            print("[on_save] Є помилки HV-графа — commit заборонено.")
            return
        
        # 5) REVIEW UI: показуємо діалог з різницями (дві колонки: Було / Стане) і беремо вибір користувача
        try:
            try:
                from ui.ui_review import run_review_dialog  # твій діалог підтвердження
            except Exception:
                # Заглушка, якщо діалог ще не реалізовано
                def run_review_dialog(_parent, stg):
                    print("[ui_review] Заглушка: приймаємо всі зміни автоматично (немає реалізації діалогу).")
                    return [op.id for op in stg.ops]

            accepted_ids = run_review_dialog(self, staging) or []
            print(f"[on_save] Користувач прийняв {len(accepted_ids)} змін(и).")
        except Exception as e:
            print(f"[on_save] Помилка під час review: {e}")
            self._show_info_dialog("Помилка", f"Не вдалося показати/обробити перегляд змін: {e}")
            return

        if not accepted_ids:
            print("[on_save] Зміни не прийняті (порожній вибір) — нічого не робимо.")
            self._show_info_dialog("Зміни скасовано", "Ви не обрали жодної зміни для застосування.")
            return

        # 6) Формуємо прийнятий target-стан (accepted_after) лише з підтверджених змін
        try:
            accepted_after = processor.accept_selection(staging, accepted_ids)
            print(f"[on_save] Сформовано accepted_after: {len(accepted_after)} об'єкт(и).")
        except Exception as e:
            print(f"[on_save] Помилка застосування вибору (accept_selection): {e}")
            self._show_info_dialog("Помилка", f"Не вдалося застосувати вибір змін: {e}")
            return

        # 7) COMMIT: застосовуємо в БД (може бути заглушка, що лише друкує повідомлення)
        try:
            processor.commit(accepted_after)
            print("[on_save] Commit виконано (або заглушка нічого не зробила).")
            self._show_info_dialog("Готово", "Зміни застосовано.")
        except NotImplementedError:
            print("[on_save] commit() ще не реалізовано — no-op.")
            self._show_info_dialog("Інформація", "Застосування змін поки не реалізоване.")
        except Exception as e:
            print(f"[on_save] Помилка під час commit: {e}")
            self._show_info_dialog("Помилка", f"Не вдалося застосувати зміни: {e}")
            return
        finally:

        self.work_context.reset()    
        self.destroy()

    def _run_validation_via_provider(self) -> bool:
        try:
            prov = FORM_REGISTRY.get(self.form_id)
            if not prov:
                self._show_info_dialog("Помилка", f"Провайдер для форми '{self.form_id}' не знайдено")
                return False

            validator = prov.get("validator")
            if not validator:
                return True  # Немає валідатора - пропускаємо перевірки

            validator = validator(self.work_context)
            issues = validator.validate()

            if issues:
                validator.show_errors(self)
                return False
            return True
        except Exception as e:
            try:
                tmp = ValidatorBase(self.work_context)
                tmp.add("", f"Помилка валідації: {e}")
                tmp.show_errors(self)
            except Exception:
                pass
            return False

    def _show_info_dialog(self, title: str, message: str) -> None:
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()

    def _on_delete_event(self, *_a):
        if FORM_WINDOW_REMEMBER_POSITION:
            try:
                x, y = self.get_position()
                w, h = self.get_size()
                screen = self.get_screen()
                sw = screen.get_width()
                sh = screen.get_height()

                anchor = (FORM_WINDOW_ANCHOR or "topleft").lower()
                if anchor == "topleft":
                    x_off, y_off = x, y
                elif anchor == "topright":
                    x_off, y_off = max(0, sw - (x + w)), y
                elif anchor == "bottomleft":
                    x_off, y_off = x, max(0, sh - (y + h))
                elif anchor == "bottomright":
                    x_off, y_off = max(0, sw - (x + w)), max(0, sh - (y + h))
                else:
                    x_off, y_off = x, y

                save_pos(
                    self.form_id if FORM_WINDOW_PER_FORM else "__default__",
                    anchor,
                    int(x_off),
                    int(y_off),
                )
            except Exception:
                pass

        for wdg, hid in getattr(self, "_live_signal_ids", []):
            try:
                wdg.handler_disconnect(hid)
            except Exception:
                pass
        self._live_signal_ids = []

        self._is_closing = True

        for cb in getattr(self, "_all_comboboxes", ()):
            for hid in getattr(cb, "_signal_ids_", ()):
                try:
                    cb.handler_block(hid)
                except Exception:
                    pass

            try:
                child = cb.get_child()  # Gtk.Entry
                if child and hasattr(child, "get_completion"):
                    comp = child.get_completion()
                    if comp:
                        child.set_completion(None)
            except Exception:
                pass

            try:
                cb.set_model(None)
            except Exception:
                pass

        return False

    def collect_snapshot_dict(self) -> dict:
        temp_state = self.make_form_state()
        for row in self.rows:
            StateCollector.collect_row(row, temp_state, allow_log=False)
        return temp_state.to_dict()

    def show(self) -> None:
        self.show_all()
