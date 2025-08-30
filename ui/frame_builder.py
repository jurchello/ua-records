from __future__ import annotations

import gi

gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
gi.require_version("Gdk", "3.0")  # pylint: disable=wrong-import-position

from gi.repository import Gdk, GLib, Gtk

from uhelpers.density_helper import get_density_settings


class FrameBuilder:

    @staticmethod
    def _apply_background(widget: Gtk.Widget, color: str | Gdk.RGBA | None) -> None:
        if not color:
            return
        if isinstance(color, str):
            rgba = Gdk.RGBA()
            rgba.parse(color)
        else:
            rgba = color
        widget.override_background_color(Gtk.StateFlags.NORMAL, rgba)

    def build_frame_and_grid(
        self,
        group_title: str | None,
        background_color: str | Gdk.RGBA | None,
    ) -> tuple[Gtk.Frame, Gtk.Grid]:
        density = get_density_settings()

        frame = Gtk.Frame()
        frame.set_shadow_type(Gtk.ShadowType.IN)
        frame.set_margin_top(density["frame_margin_top"])
        frame.set_margin_bottom(density["frame_margin_bottom"])
        frame.set_margin_start(density["frame_margin_start"])
        frame.set_margin_end(density["frame_margin_end"])

        if group_title:
            title_lbl = Gtk.Label()
            title_lbl.set_use_markup(True)
            safe = GLib.markup_escape_text(group_title)
            title_lbl.set_markup(f"<b>{safe}</b>")
            title_lbl.set_halign(Gtk.Align.START)
            frame.set_label_widget(title_lbl)
            frame.set_label_align(0.02, 0.5)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=density["vbox_spacing"])
        vbox.set_margin_top(density["vbox_margin_top"])
        vbox.set_margin_bottom(density["vbox_margin_bottom"])
        vbox.set_margin_start(density["vbox_margin_start"])
        vbox.set_margin_end(density["vbox_margin_end"])
        self._apply_background(vbox, background_color)
        frame.add(vbox)

        row_grid = Gtk.Grid(column_spacing=density["row_grid_spacing"], row_spacing=density["row_grid_spacing"])
        vbox.pack_start(row_grid, True, True, 0)

        return frame, row_grid
