import pickle
import sys
import types

import pytest


def install_env_stubs():
    for k in list(sys.modules):
        if k in {
            "gi",
            "gi.repository",
            "gi.repository.Gtk",
            "gi.repository.GLib",
            "gi.repository.Gdk",
            "gramps",
            "gramps.gen",
            "gramps.gen.display",
            "gramps.gen.display.name",
            "gramps.gen.display.place",
            "gramps.gen.lib",
            "gramps.gui",
            "gramps.gui.ddtargets",
            "configs.constants",
        } or k.startswith("gramps."):
            sys.modules.pop(k, None)

    gi = types.ModuleType("gi")
    gi.require_version = lambda *a, **k: None
    sys.modules["gi"] = gi
    repo = types.ModuleType("gi.repository")
    sys.modules["gi.repository"] = repo

    class _Widget:
        def __init__(self):
            self.label = None

        def override_background_color(self, *a, **k):
            pass

        def drag_dest_set(self, *a, **k):
            pass

        def connect(self, *a, **k):
            return 1

        def drag_source_set(self, *a, **k):
            pass

    class _Label:
        def __init__(self):
            self._t = ""

        def set_markup(self, s):
            self._t = s

        def set_text(self, s):
            self._t = s

        def get_text(self):
            return self._t

    class _Button:
        def set_opacity(self, v):
            pass

        def set_sensitive(self, v):
            pass

    class _SelectionData:
        def __init__(self):
            self._target = None
            self._data = b""

        def set(self, _t, _fmt, data):
            self._data = data

        def get_target(self):
            return None

        def get_data(self):
            return self._data

    class _Gdk:
        class DragContext: ...

        class RGBA:
            def parse(self, s):
                pass

        StateFlags = types.SimpleNamespace(NORMAL=0)
        ModifierType = types.SimpleNamespace(BUTTON1_MASK=1)

    class _GLib:
        @staticmethod
        def idle_add(fn, *a, **k):
            try:
                fn()
            except:
                pass
            return 1

    Gtk = types.SimpleNamespace(Widget=_Widget, Label=_Label, Button=_Button, SelectionData=_SelectionData)
    Gdk = _Gdk
    GLib = _GLib
    sys.modules["gi.repository.Gtk"] = Gtk
    sys.modules["gi.repository.Gdk"] = Gdk
    sys.modules["gi.repository.GLib"] = GLib
    setattr(repo, "Gtk", Gtk)
    setattr(repo, "Gdk", Gdk)
    setattr(repo, "GLib", GLib)

    gramps = types.ModuleType("gramps")
    gramps.__path__ = []
    sys.modules["gramps"] = gramps
    gen = types.ModuleType("gramps.gen")
    gen.__path__ = []
    sys.modules["gramps.gen"] = gen

    display_pkg = types.ModuleType("gramps.gen.display")
    display_pkg.__path__ = []
    sys.modules["gramps.gen.display"] = display_pkg
    name_mod = types.ModuleType("gramps.gen.display.name")
    place_mod = types.ModuleType("gramps.gen.display.place")

    class _Disp:
        def display(self, *a, **k):
            return "Displayed"

    setattr(name_mod, "displayer", _Disp())
    setattr(place_mod, "displayer", _Disp())
    sys.modules["gramps.gen.display.name"] = name_mod
    sys.modules["gramps.gen.display.place"] = place_mod

    lib_mod = types.ModuleType("gramps.gen.lib")

    class Person:
        def get_primary_name(self):
            return types.SimpleNamespace(get_name=lambda: "Test Person")

    class Place:
        def get_title(self):
            return "Test Place"

    class Citation:
        def __init__(self):
            self.page = "p. 1"

    setattr(lib_mod, "Person", Person)
    setattr(lib_mod, "Place", Place)
    setattr(lib_mod, "Citation", Citation)
    sys.modules["gramps.gen.lib"] = lib_mod

    gui_pkg = types.ModuleType("gramps.gui")
    gui_pkg.__path__ = []
    sys.modules["gramps.gui"] = gui_pkg
    dd_mod = types.ModuleType("gramps.gui.ddtargets")

    class _Target:
        def target(self):
            return object()

    class DdTargets:
        PERSON_LINK = _Target()
        PLACE_LINK = _Target()
        CITATION_LINK = _Target()

    setattr(dd_mod, "DdTargets", DdTargets)
    sys.modules["gramps.gui.ddtargets"] = dd_mod

    const = types.ModuleType("configs.constants")
    setattr(const, "COLOR_EMPTY_DND", "#ffffff")
    setattr(const, "COLOR_FILLED_DND", "#eeeeee")

    def _plen():
        return 30

    def _tlen():
        return 30

    def _clen():
        return 30

    setattr(const, "get_person_name_length", _plen)
    setattr(const, "get_place_title_length", _tlen)
    setattr(const, "get_citation_text_length", _clen)
    sys.modules["configs.constants"] = const


@pytest.fixture(autouse=True)
def _env():
    install_env_stubs()
    yield


from gramps.gen.lib import Person as GPerson, Place as GPlace, Citation as GCitation


class FakeDB:
    def __init__(self, p, pl, c):
        self._p = p
        self._pl = pl
        self._c = c

    def get_person_from_handle(self, _h):
        return self._p

    def get_place_from_handle(self, _h):
        return self._pl

    def get_citation_from_handle(self, _h):
        return self._c


class DBState:
    def __init__(self, db):
        self.db = db


class UIState: ...


def test_elide_and_decorate_success_person(monkeypatch):
    from gi.repository import Gtk

    from ui.drag_drop_adapter import DragDropAdapter

    db = FakeDB(p=GPerson(), pl=GPlace(), c=GCitation())
    ada = DragDropAdapter(DBState(db), UIState())
    w = Gtk.Widget()
    w.label = Gtk.Label()
    ada._decorate_success(w, "John Smith", markup_kind="u")
    assert "<u>John Smith</u>" in w.label.get_text()
    assert ada._elide("abcdef", 6) == "abcdef"
    assert ada._elide("abcdef", 5).endswith("…")


def test_decode_payload_for_person_place_citation():
    from gi.repository import Gtk

    from ui.drag_drop_adapter import Citation as DDACitationClass
    from ui.drag_drop_adapter import (
        DragDropAdapter,
    )
    from ui.drag_drop_adapter import Person as DDAPersonClass
    from ui.drag_drop_adapter import Place as DDAPlaceClass

    # Use the same classes that DragDropAdapter imports
    db = FakeDB(p=DDAPersonClass(), pl=DDAPlaceClass(), c=DDACitationClass())
    ada = DragDropAdapter(DBState(db), UIState())
    sd = Gtk.SelectionData()

    matrix = [
        ("person-link", "P1", "person", DDAPersonClass),
        ("place-link", "L1", "place", DDAPlaceClass),
        ("citation-link", "C1", "citation", DDACitationClass),
    ]
    for tag, handle, target, _expect_type in matrix:
        payload = (tag, None, handle, None)
        sd.set(None, 8, pickle.dumps(payload))
        h, obj = ada._decode_payload(sd, target)
        assert h == handle
        assert obj is not None
