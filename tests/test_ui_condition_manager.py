import sys
import types

import pytest


def install_gi_stubs():
    for k in list(sys.modules):
        if k in {"gi", "gi.repository", "gi.repository.Gtk", "gi.repository.GLib"}:
            sys.modules.pop(k, None)
    gi = types.ModuleType("gi")
    gi.require_version = lambda *a, **k: None
    sys.modules["gi"] = gi
    repo = types.ModuleType("gi.repository")
    sys.modules["gi.repository"] = repo

    class _Widget:
        def __init__(self):
            self._visible = True

        def show(self):
            self._visible = True

        def hide(self):
            self._visible = False

        def get_child(self):
            return None

        def get_visible(self):
            return self._visible

        def connect(self, *a, **k):
            return 1  # no-op signal connect

    class _Label(_Widget):
        def __init__(self):
            super().__init__()
            self._markup = ""

        def set_markup(self, s):
            self._markup = s

        def get_text(self):
            return self._markup

    class _Entry(_Widget):
        def __init__(self):
            super().__init__()
            self._t = ""

        def set_text(self, s):
            self._t = s

        def get_text(self):
            return self._t

    class _Check(_Widget):
        def __init__(self):
            super().__init__()
            self._a = False

        def set_active(self, b):
            self._a = bool(b)

        def get_active(self):
            return self._a

    class _Combo(_Widget):
        def __init__(self, child=None, items=None):
            super().__init__()
            self._child = child
            self._items = items or []
            self._active_idx = 0 if self._items else -1

        def get_child(self):
            return self._child

        def get_active_text(self):
            if 0 <= self._active_idx < len(self._items):
                return self._items[self._active_idx]
            return ""

        def set_active_index(self, i):
            self._active_idx = i

        def get_model(self):
            return self._items

        def get_active_iter(self):
            return (self._active_idx,) if 0 <= self._active_idx < len(self._items) else None

        def __getitem__(self, it):
            return self._items[it[0]]

    class _EventBox(_Widget):
        def __init__(self, child=None):
            super().__init__()
            self._child = child

        def get_child(self):
            return self._child

    Gtk = types.SimpleNamespace(
        Widget=_Widget, Label=_Label, Entry=_Entry, CheckButton=_Check, ComboBox=_Combo, EventBox=_EventBox
    )
    sys.modules["gi.repository.Gtk"] = Gtk
    setattr(repo, "Gtk", Gtk)

    class _GLib:
        @staticmethod
        def idle_add(fn, *a, **k):
            try:
                fn()
            except:
                pass
            return 1

        @staticmethod
        def markup_escape_text(s):
            return s

    sys.modules["gi.repository.GLib"] = _GLib
    setattr(repo, "GLib", _GLib)


@pytest.fixture(autouse=True)
def _gi():
    install_gi_stubs()
    # Clean up any previously loaded ui modules to avoid state pollution
    import sys

    for module_name in list(sys.modules.keys()):
        if module_name.startswith("ui."):
            del sys.modules[module_name]
    yield


def test_condition_manager_visibility_and_label_variants():
    from gi.repository import Gtk

    from ui.condition_manager import ConditionManager

    class VisBox:
        def __init__(self):
            self._v = False

        def show(self):
            self._v = True

        def hide(self):
            self._v = False

        def get_visible(self):
            return self._v

    v = Gtk.Entry()
    v.set_text("x")
    dep_widget = VisBox()
    lbl = Gtk.Label()
    box = VisBox()

    widgets = {"gender": v, "name": dep_widget}
    labels = {"name": lbl}
    boxes = {"name": box}

    fields = [
        {
            "id": "name",
            "show_when": {"var": "gender", "in": ["man"]},
            "label_variants": {"man": "His name", "default": "Name"},
        }
    ]

    cm = ConditionManager(widgets=widgets, labels=labels, label_boxes=boxes, field_defs=fields)
    cm.init_rules()
    cm.apply_all()
    assert dep_widget.get_visible() is False and box.get_visible() is False

    v.set_text("man")
    cm.apply_all()
    assert dep_widget.get_visible() is True and box.get_visible() is True
    assert "His name" in lbl.get_text()


def test_condition_manager_equals_notin_truthy_and_id_resolution():
    from gi.repository import Gtk

    from ui.condition_manager import ConditionManager

    class VisBox:
        def __init__(self):
            self._v = False

        def show(self):
            self._v = True

        def hide(self):
            self._v = False

        def get_visible(self):
            return self._v

    gate = Gtk.Entry()
    gate.set_text("no")
    a = VisBox()
    la = Gtk.Label()
    ba = VisBox()
    b = VisBox()
    lb = Gtk.Label()
    bb = VisBox()
    c = VisBox()
    lc = Gtk.Label()
    bc = VisBox()

    widgets = {"prefix_var": gate, "x.a": a, "x_b": b, "c": c}
    labels = {"x.a": la, "x_b": lb, "c": lc}
    boxes = {"x.a": ba, "x_b": bb, "c": bc}
    fields = [
        {"id": "a", "show_when": {"var": "prefix_var", "equals": "yes"}},
        {"id": "b", "show_when": {"var": "prefix_var", "not_in": ["no", "0"]}},
        {"id": "c", "show_when": {"var": "prefix_var", "truthy": True}},
    ]
    cm = ConditionManager(widgets=widgets, labels=labels, label_boxes=boxes, field_defs=fields)
    cm.init_rules()
    cm.apply_all()
    assert a.get_visible() is False
    assert b.get_visible() is False
    assert c.get_visible() is False

    gate.set_text("yes")
    cm.apply_all()
    assert a.get_visible() is True
    assert b.get_visible() is True
    assert c.get_visible() is True


def test_condition_manager_flatten_fields_matrix_and_list():
    from ui.condition_manager import ConditionManager

    f1 = [{"id": "a"}, {"id": "b"}]
    f2 = [[{"id": "a"}], [{"id": "b"}]]
    assert [x["id"] for x in ConditionManager._flatten_fields(f1)] == ["a", "b"]
    assert [x["id"] for x in ConditionManager._flatten_fields(f2)] == ["a", "b"]
