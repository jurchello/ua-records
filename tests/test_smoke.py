from typing import Any, cast
from pytest import MonkeyPatch
import form_gramplet as mod


def test_formgramplet_build_gui(monkeypatch: MonkeyPatch) -> None:
    def _noop_init(self: mod.Gramplet, gui: Any, nav_group: int = 0) -> None:
        self.gui = gui
    monkeypatch.setattr(mod.Gramplet, "__init__", _noop_init, raising=True)

    class DummyContainer:
        def get_children(self) -> list[object]: return []
        def remove(self, _child: object) -> None: ...
        def add(self, _child: object) -> None: ...

    class DummyGui:
        def get_container_widget(self) -> DummyContainer:
            return DummyContainer()

    gramplet = mod.FormGramplet(cast(Any, DummyGui()))
    gramplet.init()
    assert gramplet.model is not None
