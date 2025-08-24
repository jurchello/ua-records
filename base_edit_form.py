from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import gi
gi.require_version("Gtk", "3.0")  # pylint: disable=wrong-import-position
from gi.repository import Gtk

if TYPE_CHECKING:
    from gramps.gen.db.dbapi import DbState, UiState
else:
    DbState = Any
    UiState = Any


class BaseEditForm(Gtk.Window):

    def __init__(self, *, dbstate: DbState, uistate: UiState, form_id: str) -> None:
        super().__init__(title="Form")
        self.dbstate: DbState = dbstate
        self.uistate: UiState = uistate
        self.form_id: str = form_id

        self.set_default_size(640, 480)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box)

    def _on_refresh_options(self, _event: Optional[object]) -> None:
        pass

    def refresh_options(self, event: Optional[object] = None) -> None:
        self._on_refresh_options(event)

    def show(self) -> None:
        self.show_all()