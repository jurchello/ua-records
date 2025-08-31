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
            "gramps.gen.plug",
            "gramps.gen.plug.menu",
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
    gramps_gen_plug = types.ModuleType("gramps.gen.plug")
    gramps_gen_plug.__path__ = []
    sys.modules["gramps.gen.plug"] = gramps_gen_plug

    menu_mod = types.ModuleType("gramps.gen.plug.menu")

    class _BaseOption:
        def __init__(self, _label, value, *a, **k):
            self._value = value

        def get_value(self):
            return self._value

        def set_value(self, v):
            self._value = v

        def set_help(self, _):
            pass

    class EnumeratedListOption(_BaseOption):
        def __init__(self, label, value):
            super().__init__(label, value)
            self._items = []

        def add_item(self, value, label):
            self._items.append((value, label))

    class StringOption(_BaseOption): ...

    class NumberOption(_BaseOption):
        def __init__(self, label, value, _min=0, _max=9999):
            super().__init__(label, int(value))

    class BooleanOption(_BaseOption):
        def __init__(self, label, value):
            super().__init__(label, bool(value))

    setattr(menu_mod, "EnumeratedListOption", EnumeratedListOption)
    setattr(menu_mod, "StringOption", StringOption)
    setattr(menu_mod, "NumberOption", NumberOption)
    setattr(menu_mod, "BooleanOption", BooleanOption)
    sys.modules["gramps.gen.plug.menu"] = menu_mod

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
    sys.modules["gi.repository.GObject"] = types.SimpleNamespace()
    setattr(repo_mod, "GObject", sys.modules["gi.repository.GObject"])

    class _GtkListStore:
        def __init__(self, *a, **k):
            pass

    gtk_mod = types.SimpleNamespace(ListStore=_GtkListStore)
    sys.modules["gi.repository.Gtk"] = gtk_mod  # type: ignore
    setattr(repo_mod, "Gtk", gtk_mod)

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
            self._ai_provider = "disabled"
            self._ai_model = ""
            self._ai_api_key = ""
            self._birth = 3
            self._death = 3
            self._marriage = 3
            self._density = "compact"
            self._tab_density = "normal"
            self._window_mode = "transient"
            self._window_keep_above = False
            self._person_len = 30
            self._place_len = 30
            self._citation_len = 30

        def get_ai_provider(self):
            return self._ai_provider

        def set_ai_provider(self, v):
            self._ai_provider = v

        def get_ai_model(self):
            return self._ai_model

        def set_ai_model(self, v):
            self._ai_model = v

        def get_ai_api_key(self):
            return self._ai_api_key

        def set_ai_api_key(self, v):
            self._ai_api_key = v

        def get_birth_columns(self):
            return self._birth

        def set_birth_columns(self, v):
            self._birth = int(v)

        def get_death_columns(self):
            return self._death

        def set_death_columns(self, v):
            self._death = int(v)

        def get_marriage_columns(self):
            return self._marriage

        def set_marriage_columns(self, v):
            self._marriage = int(v)

        def get_form_density(self):
            return self._density

        def set_form_density(self, v):
            self._density = v

        def get_person_name_length(self):
            return self._person_len

        def set_person_name_length(self, v):
            self._person_len = int(v)

        def get_place_title_length(self):
            return self._place_len

        def set_place_title_length(self, v):
            self._place_len = int(v)

        def get_citation_text_length(self):
            return self._citation_len

        def set_citation_text_length(self, v):
            self._citation_len = int(v)

        def get_tab_density(self):
            return self._tab_density

        def set_tab_density(self, v):
            self._tab_density = v

        def get_window_mode(self):
            return self._window_mode

        def set_window_mode(self, v):
            self._window_mode = v

        def get_window_keep_above(self):
            return self._window_keep_above

        def set_window_keep_above(self, v):
            self._window_keep_above = bool(v)

    _singleton = SettingsManager()

    def get_settings_manager():
        return _singleton

    setattr(sm, "SettingsManager", SettingsManager)
    setattr(sm, "get_settings_manager", get_settings_manager)
    sys.modules["settings.settings_manager"] = sm

    sui = types.ModuleType("settings.settings_ui")
    from gramps.gen.plug import menu as _menu

    class SettingsUI:
        def __init__(self, manager):
            self.m = manager

        def build_options(self):
            opts = []
            opts.append(_menu.EnumeratedListOption("ai_provider", self.m.get_ai_provider()))
            opts.append(_menu.StringOption("ai_model", self.m.get_ai_model()))
            opts.append(_menu.StringOption("ai_api_key", self.m.get_ai_api_key()))
            opts.append(_menu.NumberOption("birth_columns", self.m.get_birth_columns()))
            opts.append(_menu.NumberOption("death_columns", self.m.get_death_columns()))
            opts.append(_menu.NumberOption("marriage_columns", self.m.get_marriage_columns()))
            opts.append(_menu.EnumeratedListOption("density", self.m.get_form_density()))
            opts.append(_menu.EnumeratedListOption("tab_density", self.m.get_tab_density()))
            opts.append(_menu.EnumeratedListOption("window_mode", self.m.get_window_mode()))
            opts.append(_menu.BooleanOption("window_keep_above", self.m.get_window_keep_above()))
            opts.append(_menu.NumberOption("person_name_length", self.m.get_person_name_length()))
            opts.append(_menu.NumberOption("place_title_length", self.m.get_place_title_length()))
            opts.append(_menu.NumberOption("citation_text_length", self.m.get_citation_text_length()))
            return opts

    setattr(sui, "SettingsUI", SettingsUI)
    sys.modules["settings.settings_ui"] = sui


class DummyGui:
    def get_container_widget(self):
        return types.SimpleNamespace(get_children=lambda: [], remove=lambda _c: None, add=lambda _c: None)


@pytest.fixture()
def fake_env(tmp_path: Path):
    _install_minimal_stubs(tmp_path)
    for mod_name in ["UARecords"]:
        sys.modules.pop(mod_name, None)
    return None


def test_gramplet_save_roundtrip(monkeypatch, fake_env):
    import UARecords as fg

    g = fg.UARecords(DummyGui())
    g.build_options()
    # Should have 13 options with all new window settings
    assert len(g.opts_cache) == 13

    assert g.opts_cache[0].get_value() == "disabled"
    assert g.opts_cache[3].get_value() == 3
    assert g.opts_cache[6].get_value() == "compact"
    assert g.opts_cache[7].get_value() == "normal"  # tab_density
    assert g.opts_cache[8].get_value() == "transient"  # window_mode
    assert g.opts_cache[9].get_value() == False  # window_keep_above

    g.opts_cache[0].set_value("openai")
    g.opts_cache[1].set_value("gpt-4o-mini")
    g.opts_cache[2].set_value("secret")
    g.opts_cache[3].set_value(4)
    g.opts_cache[4].set_value(2)
    g.opts_cache[5].set_value(5)
    g.opts_cache[6].set_value("normal")
    g.opts_cache[7].set_value("spacious")  # tab_density
    g.opts_cache[8].set_value("modal")  # window_mode
    g.opts_cache[9].set_value(True)  # window_keep_above
    g.opts_cache[10].set_value(42)  # person_name_length
    g.opts_cache[11].set_value(55)  # place_title_length
    g.opts_cache[12].set_value(60)  # citation_text_length

    monkeypatch.setattr(fg.UARecords, "_refresh_open_forms", lambda self: None, raising=True)
    g.save_options()
    cfg = g.settings_manager
    assert cfg.get_ai_provider() == "openai"
    assert cfg.get_ai_model() == "gpt-4o-mini"
    assert cfg.get_ai_api_key() == "secret"
    assert cfg.get_birth_columns() == 4
    assert cfg.get_death_columns() == 2
    assert cfg.get_marriage_columns() == 5
    assert cfg.get_form_density() == "normal"
    assert cfg.get_tab_density() == "spacious"
    assert cfg.get_window_mode() == "modal"
    assert cfg.get_window_keep_above() == True
    assert cfg.get_person_name_length() == 42
    assert cfg.get_place_title_length() == 55
    assert cfg.get_citation_text_length() == 60
