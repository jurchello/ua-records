from __future__ import annotations

import sys
import types
from pathlib import Path

import pytest


def _install_minimal_stubs(tmp_path: Path) -> None:
    for k in list(sys.modules):
        if k in {
            "gramps",
            "gramps.gen",
            "gramps.gen.plug._gramplet",
            "gi",
            "gi.repository",
            "gi.repository.GObject",
            "gi.repository.Gtk",
            "providers",
            "base_edit_form",
            "edit_form",
            "ulogging",
            "ulogging.autoinit",
            "settings",
            "settings.settings_manager",
            "settings.settings_ui",
            "UARecords",
        } or k.startswith("gramps."):
            sys.modules.pop(k, None)

    gramps_pkg = types.ModuleType("gramps")
    gramps_pkg.__path__ = []
    sys.modules["gramps"] = gramps_pkg
    gramps_gen = types.ModuleType("gramps.gen")
    gramps_gen.__path__ = []
    sys.modules["gramps.gen"] = gramps_gen

    gram_mod = types.ModuleType("gramps.gen.plug._gramplet")

    class Gramplet:
        def __init__(self, gui, _nav=0):
            self.gui = gui

        def add_option(self, _opt):
            pass

        def update(self):
            pass

    setattr(gram_mod, "Gramplet", Gramplet)
    sys.modules["gramps.gen.plug._gramplet"] = gram_mod

    gi_mod = types.ModuleType("gi")
    gi_mod.require_version = lambda *a, **k: None
    sys.modules["gi"] = gi_mod
    repo_mod = types.ModuleType("gi.repository")
    sys.modules["gi.repository"] = repo_mod

    class _GtkListStore:
        def __init__(self, *a, **k):
            pass

    gtk_mod = types.SimpleNamespace(ListStore=_GtkListStore)
    sys.modules["gi.repository.Gtk"] = gtk_mod  # type: ignore
    setattr(repo_mod, "Gtk", gtk_mod)
    sys.modules["gi.repository.GObject"] = types.SimpleNamespace()
    setattr(repo_mod, "GObject", sys.modules["gi.repository.GObject"])

    providers_mod = types.ModuleType("providers")
    providers_mod.__path__ = []
    setattr(
        providers_mod,
        "FORM_REGISTRY",
        {
            "birth": {"title": "Birth record", "list_label": "Birth"},
            "death": {"title": "Death record", "list_label": "Death"},
        },
    )
    sys.modules["providers"] = providers_mod

    base_edit_form_mod = types.ModuleType("base_edit_form")

    class BaseEditForm: ...

    setattr(base_edit_form_mod, "BaseEditForm", BaseEditForm)
    sys.modules["base_edit_form"] = base_edit_form_mod

    edit_form_mod = types.ModuleType("edit_form")

    class EditForm:
        def __init__(self, *a, **k):
            pass

        def show(self):
            pass

    setattr(edit_form_mod, "EditForm", EditForm)
    sys.modules["edit_form"] = edit_form_mod

    ulogging_pkg = types.ModuleType("ulogging")
    ulogging_pkg.__path__ = []
    sys.modules["ulogging"] = ulogging_pkg
    autoinit_mod = types.ModuleType("ulogging.autoinit")

    class _LogChan:
        def debug(self, *a, **k):
            pass

        def info(self, *a, **k):
            pass

        def warning(self, *a, **k):
            pass

        def error(self, *a, **k):
            pass

        def critical(self, *a, **k):
            pass

    class _Logger:
        def channel(self, _name):
            return _LogChan()

    setattr(autoinit_mod, "logger", _Logger())
    sys.modules["ulogging.autoinit"] = autoinit_mod

    settings_pkg = types.ModuleType("settings")
    settings_pkg.__path__ = []
    sys.modules["settings"] = settings_pkg
    sm = types.ModuleType("settings.settings_manager")

    class SettingsManager:
        def __init__(self):
            self._marriage = 3

        def get_marriage_columns(self):
            return self._marriage

        def set_marriage_columns(self, v):
            self._marriage = int(v)

    _singleton = SettingsManager()

    def get_settings_manager():
        return _singleton

    setattr(sm, "SettingsManager", SettingsManager)
    setattr(sm, "get_settings_manager", get_settings_manager)
    sys.modules["settings.settings_manager"] = sm

    sui = types.ModuleType("settings.settings_ui")

    class SettingsUI:
        def __init__(self, manager):
            self.m = manager

        def build_options(self):
            return []

    setattr(sui, "SettingsUI", SettingsUI)
    sys.modules["settings.settings_ui"] = sui


@pytest.fixture()
def fake_env(tmp_path: Path):
    _install_minimal_stubs(tmp_path)
    for mod_name in ["UARecords"]:
        sys.modules.pop(mod_name, None)
    return None


def test_formgramplet_build_gui(monkeypatch, fake_env):
    from gramps.gen.plug._gramplet import Gramplet

    def _noop_init(self, gui, nav_group=0):
        self.gui = gui

    monkeypatch.setattr(Gramplet, "__init__", _noop_init, raising=True)

    import gi

    from UARecords import UARecords

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk  # type: ignore

    def mock_build_gui(self):
        self.model = Gtk.ListStore()

        class _Box:
            def show_all(self):
                pass

        return _Box()

    monkeypatch.setattr(UARecords, "_build_gui", mock_build_gui, raising=False)

    class DummyContainer:
        def get_children(self):
            return []

        def remove(self, _child):
            pass

        def add(self, _child):
            pass

        def show_all(self):
            pass

    class DummyGui:
        def get_container_widget(self):
            return DummyContainer()

    gramplet = UARecords(DummyGui())
    gramplet.init()
    assert getattr(gramplet, "model", None) is not None
