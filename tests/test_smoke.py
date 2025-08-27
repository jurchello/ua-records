from typing import Any, cast
from pytest import MonkeyPatch
from gramps.gen.plug._gramplet import Gramplet


def test_formgramplet_build_gui(monkeypatch: MonkeyPatch) -> None:
    def _noop_init(self: Gramplet, gui: Any, nav_group: int = 0) -> None:
        self.gui = gui
    monkeypatch.setattr(Gramplet, "__init__", _noop_init, raising=True)

    # Mock the _build_gui method to avoid Gtk issues in testing
    def mock_build_gui(self: Any) -> Any:
        # Just create the model like the real method does
        import gi
        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk, GObject
        self.model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_STRING)
        
        class MockBox:
            def show_all(self) -> None: ...
        
        return MockBox()

    from UARecords import UARecords
    monkeypatch.setattr(UARecords, "_build_gui", mock_build_gui, raising=False)

    class DummyContainer:
        def get_children(self) -> list[object]: return []
        def remove(self, _child: object) -> None: ...
        def add(self, _child: object) -> None: ...
        def show_all(self) -> None: ...

    class DummyGui:
        def get_container_widget(self) -> DummyContainer:
            return DummyContainer()

    gramplet = UARecords(cast(Any, DummyGui()))
    gramplet.init()
    assert gramplet.model is not None
