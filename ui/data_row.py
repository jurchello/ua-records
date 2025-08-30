from __future__ import annotations

from typing import TYPE_CHECKING

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gdk, Gtk

from ui.condition_manager import ConditionManager
from ui.field_renderer import FieldRenderer
from ui.frame_builder import FrameBuilder
from ui.model_manager import ModelManager
from ui.reset_manager import ResetManager

if TYPE_CHECKING:
    from gramps.gen.db.dbapi import DbState, UiState
    from ui.drag_drop_adapter import DragDropAdapter


class DataRow:

    def __init__(
        self,
        grid: Gtk.Grid,
        row: int,
        *,
        dbstate: DbState,
        uistate: UiState,
        dnd_adapter: DragDropAdapter,
        fields: list[list[dict[str, str]]],
        group_title: str | None = None,
        prefix: str | None = None,
        background_color: str | Gdk.RGBA | None = None,
        label_size_groups: list[Gtk.SizeGroup] | None = None,
        widget_size_groups: list[Gtk.SizeGroup] | None = None,
        columns: int | None = None,
    ) -> None:
        self._grid = grid
        self._toplevel = grid.get_toplevel()
        self.prefix: str | None = prefix
        self.dbstate: DbState = dbstate
        self.uistate: UiState = uistate
        self.dnd_adapter: DragDropAdapter = dnd_adapter

        self.changed_handlers: dict[str, int] = {}
        self.widgets: dict[str, Gtk.Widget] = {}
        self.objects: dict[str, object] = {}
        self.handles: dict[str, str] = {}
        self.defaults: dict[str, str] = {}
        self.types: dict[str, str] = {}
        self._field_specs: dict[str, dict] = {}

        self.frame_builder = FrameBuilder()
        self.model_manager = ModelManager()
        self.reset_manager = ResetManager()
        self.field_renderer = FieldRenderer(
            dbstate=dbstate,
            uistate=uistate,
            dnd_adapter=dnd_adapter,
            model_manager=self.model_manager,
            toplevel=self._toplevel,
            widgets=self.widgets,
            objects=self.objects,
            handles=self.handles,
            defaults=self.defaults,
            data_row=self,
            types=self.types,
            changed_handlers=self.changed_handlers,
        )

        frame, row_grid = self.frame_builder.build_frame_and_grid(group_title, background_color)
        self._row_grid = row_grid

        for sub in fields:
            for f in sub:
                self._field_specs[f["id"]] = f

        self.field_renderer.set_field_specs(self._field_specs)
        rows = self.field_renderer.prepare_rows(fields)

        # Use provided columns setting or calculate from layout as fallback
        if columns is not None:
            frame_pairs = max(1, columns)
        else:
            frame_pairs = self.field_renderer.max_pairs_in_frame(rows)

        self._frame_pairs = frame_pairs
        self.field_renderer.set_layout_context(self._row_grid, self._frame_pairs)

        self.field_renderer.render_rows(
            rows,
            row_grid,
            frame_pairs,
            background_color,
            label_size_groups or [],
            widget_size_groups or [],
        )

        cond = ConditionManager(
            widgets=self.field_renderer.widgets,
            labels=self.field_renderer.labels,
            label_boxes=self.field_renderer.label_boxes,
            field_defs=fields,
            get_cols=lambda: self._frame_pairs,
        )
        cond.set_visibility_changed_callback(self.field_renderer.reflow)
        cond.init_rules()
        self._condition_manager = cond
        self._condition_manager.evaluate()

        self.field_renderer.reflow()

        grid.attach(frame, 0, row, 8, 1)

    def reset_to_defaults(self, _profile: object | None = None) -> None:
        self.reset_manager.reset_to_defaults(
            widgets=self.widgets,
            types=self.types,
            defaults=self.defaults,
            changed_handlers=self.changed_handlers,
            dbstate=self.dbstate,
            handles=self.handles,
            objects=self.objects,
        )

    def _trigger_sync(self) -> None:
        try:
            toplevel = self._grid.get_toplevel()
            if hasattr(toplevel, "collect_snapshot_dict") and getattr(toplevel, "state", None) is not None:
                snap = toplevel.collect_snapshot_dict()
                toplevel.state.update_from_dict(snap)
        except Exception:
            pass
