from typing import Protocol, Any
from gi.repository import Gtk

class GUIStub(Protocol):
    def get_container_widget(self) -> Gtk.Container: ...
    dbstate: Any
    uistate: Any
    textview: Any
    data: list[str]
    force_update: bool
    title: str
    def add_gui_option(self, option: Any) -> tuple[Any, Any]: ...
    def set_has_data(self, value: bool) -> None: ...
    def link(self, text: str, link_type: str, data: Any,
             size: int | None = ..., tooltip: str | None = ...) -> None: ...

class Gramplet:
    gui: GUIStub
    def __init__(self, gui: GUIStub, nav_group: int = ...) -> None: ...
    def init(self) -> None: ...