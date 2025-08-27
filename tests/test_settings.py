from __future__ import annotations
import types
from pathlib import Path
from typing import Any, cast, Generator
import sys

import pytest

# ---------- helpers to install fake modules ----------
class _FakeConfigManager:
    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        self.saved = False
    def register(self, key: str, default: Any) -> None:
        self._data.setdefault(key, default)
    def get(self, key: str) -> Any:
        return self._data.get(key)
    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
    def load(self) -> None:
        pass
    def save(self) -> None:
        self.saved = True

def _install_fake_gramps(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # gramps.gen.config
    cfg_mod = types.ModuleType("gramps.gen.config")
    config_holder = types.SimpleNamespace()
    def register_manager(_name: str) -> _FakeConfigManager:
        return _FakeConfigManager()
    config_holder.register_manager = register_manager
    setattr(cfg_mod, 'config', config_holder)
    sys.modules["gramps.gen.config"] = cfg_mod

    # gramps.gen.const
    const_mod = types.ModuleType("gramps.gen.const")
    setattr(const_mod, 'USER_DATA', str(tmp_path))
    def get_translator(*args: Any, **kwargs: Any) -> types.SimpleNamespace:
        def gettext(s: str) -> str:
            return s
        return types.SimpleNamespace(gettext=gettext)
    def gettext(s: str) -> str:
        return s
    setattr(const_mod, 'GRAMPS_LOCALE', types.SimpleNamespace(
        get_addon_translator=get_translator,
        translation=types.SimpleNamespace(gettext=gettext),
    ))
    sys.modules["gramps.gen.const"] = const_mod

    # gramps.gen.plug.menu
    menu_mod = types.ModuleType("gramps.gen.plug.menu")
    class _BaseOption:
        def __init__(self, _label: str, value: Any, *args: Any, **kwargs: Any) -> None:
            self._value = value
        def get_value(self) -> Any: return self._value
        def set_value(self, v: Any) -> None: self._value = v
        def set_help(self, _txt: str) -> None: ...
    class EnumeratedListOption(_BaseOption):
        def __init__(self, label: str, value: Any) -> None:
            super().__init__(label, value)
            self._items: list[tuple[str, str]] = []
        def add_item(self, value: str, label: str) -> None:
            self._items.append((value, label))
    class StringOption(_BaseOption): ...
    class NumberOption(_BaseOption):
        def __init__(self, label: str, value: int, _min: int, _max: int) -> None:
            super().__init__(label, int(value))
    setattr(menu_mod, 'EnumeratedListOption', EnumeratedListOption)
    setattr(menu_mod, 'StringOption', StringOption)
    setattr(menu_mod, 'NumberOption', NumberOption)
    sys.modules["gramps.gen.plug.menu"] = menu_mod

    # gramps.gen.plug._gramplet
    gram_mod = types.ModuleType("gramps.gen.plug._gramplet")
    class _GUIStub:
        def get_container_widget(self) -> Any:
            def get_children() -> list[Any]:
                return []
            def remove(child: Any) -> None:
                pass
            def add(widget: Any) -> None:
                pass
            return types.SimpleNamespace(
                get_children=get_children,
                remove=remove,
                add=add,
            )
    class Gramplet:
        def __init__(self, gui: _GUIStub, _nav: int = 0) -> None:
            self.gui = gui
            self._added: list[Any] = []
        def add_option(self, opt: Any) -> None:
            self._added.append(opt)
        def update(self) -> None:
            pass
    setattr(gram_mod, 'Gramplet', Gramplet)
    setattr(gram_mod, 'GUIStub', _GUIStub)
    sys.modules["gramps.gen.plug._gramplet"] = gram_mod

    # ---- gi & Gtk/GObject fakes ----
    gi_mod = types.ModuleType("gi")
    def require_version(*args: Any, **kwargs: Any) -> None:
        pass
    setattr(gi_mod, 'require_version', require_version)
    sys.modules["gi"] = gi_mod

    repo_mod = types.ModuleType("gi.repository")
    sys.modules["gi.repository"] = repo_mod

    class _GtkWindow:
        def __init__(self, *a: Any, **k: Any) -> None: ...
        @staticmethod
        def list_toplevels() -> list[Any]:
            return []
    class _GtkBox:
        def __init__(self, *a: Any, **k: Any) -> None: ...
        def pack_start(self, *_a: Any, **_k: Any) -> None: ...
        def show_all(self) -> None: ...
    class _GtkListStore:
        def __init__(self, *_t: Any) -> None: ...
    class _GtkTreeView:
        def __init__(self, *a: Any, **k: Any) -> None: ...
        def append_column(self, *_a: Any, **_k: Any) -> int: return 0
    class _GtkCellRenderer: ...
    class _GtkCellRendererText(_GtkCellRenderer): ...
    class _GtkTreeViewColumn:
        def __init__(self, *a: Any, **k: Any) -> None: ...
    class _GtkScrolledWindow:
        def __init__(self) -> None: ...
        def set_policy(self, *_a: Any, **_k: Any) -> None: ...
        def set_vexpand(self, *_a: Any, **_k: Any) -> None: ...
        def add(self, *_a: Any, **_k: Any) -> None: ...

    class _GtkPolicyType:
        AUTOMATIC = 0
    class _GtkOrientation:
        VERTICAL = 1

    gtk_mod = types.SimpleNamespace(
        Window=_GtkWindow,
        Box=_GtkBox,
        ListStore=_GtkListStore,
        TreeView=_GtkTreeView,
        CellRenderer=_GtkCellRenderer,
        CellRendererText=_GtkCellRendererText,
        TreeViewColumn=_GtkTreeViewColumn,
        ScrolledWindow=_GtkScrolledWindow,
        PolicyType=_GtkPolicyType,
        Orientation=_GtkOrientation,
    )
    # зареєструвати як підмодуль і як атрибут пакета gi.repository
    sys.modules["gi.repository.Gtk"] = cast(Any, gtk_mod)
    setattr(repo_mod, "Gtk", gtk_mod)

    # --- GObject fake ---
    gobject_mod = types.SimpleNamespace(
        TYPE_STRING=object(),
        TYPE_INT=object(),
        TYPE_OBJECT=object(),
    )
    sys.modules["gi.repository.GObject"] = cast(Any, gobject_mod)
    setattr(repo_mod, "GObject", gobject_mod)

@pytest.fixture()
def fake_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Generator[None, Any, None]:
    _install_fake_gramps(monkeypatch, tmp_path)
    # reload our modules after fakes are in place
    for mod_name in [
        "settings.settings_manager",
        "settings.settings_ui",
        "UARecords",
    ]:
        if mod_name in sys.modules:
            del sys.modules[mod_name]
    yield

# ---------- tests ----------
def test_config_defaults_and_save(fake_env: Any) -> None:
    from settings.settings_manager import SettingsManager
    cfg = SettingsManager()
    assert cfg.get_ai_provider() == "disabled"
    assert cfg.get_ai_model() == ""
    assert cfg.get_ai_api_key() == ""
    assert cfg.get_birth_columns() == 3
    assert cfg.get_death_columns() == 3
    assert cfg.get_marriage_columns() == 3
    assert cfg.get_form_density() == "compact"
    assert cfg.get_person_name_length() == 30
    assert cfg.get_place_title_length() == 30
    assert cfg.get_citation_text_length() == 30
    assert not cfg.is_ai_available()

    cfg.set_ai_provider("openai")
    cfg.set_ai_model("gpt-4o-mini")
    cfg.set_ai_api_key("secret")
    assert cfg.is_ai_available()

    cfg.set_birth_columns(4)
    cfg.set_death_columns(2)
    cfg.set_marriage_columns(5)
    cfg.set_form_density("normal")
    cfg.set_person_name_length(42)
    cfg.set_place_title_length(55)
    cfg.set_citation_text_length(60)

    assert cfg.get_birth_columns() == 4
    assert cfg.get_death_columns() == 2
    assert cfg.get_marriage_columns() == 5
    assert cfg.get_form_density() == "normal"
    assert cfg.get_person_name_length() == 42
    assert cfg.get_place_title_length() == 55
    assert cfg.get_citation_text_length() == 60

def test_settings_ui_builds_options(fake_env: Any) -> None:
    from settings.settings_manager import SettingsManager
    from settings.settings_ui import SettingsUI
    cfg = SettingsManager()
    ui = SettingsUI(cfg)
    opts = ui.build_options()
    assert len(opts) == 10
    assert opts[0].get_value() == "disabled"
    assert opts[3].get_value() == 3
    assert opts[6].get_value() == "compact"

def test_gramplet_save_roundtrip(fake_env: Any) -> None:
    import UARecords as fg
    from gramps.gen.plug._gramplet import GUIStub

    g = fg.UARecords(cast(Any, GUIStub)())
    g.build_options()
    assert len(g.opts_cache) == 10

    g.opts_cache[0].set_value("openai")
    g.opts_cache[1].set_value("gpt-4o-mini")
    g.opts_cache[2].set_value("secret")
    g.opts_cache[3].set_value(4)
    g.opts_cache[4].set_value(2)
    g.opts_cache[5].set_value(5)
    g.opts_cache[6].set_value("normal")
    g.opts_cache[7].set_value(42)
    g.opts_cache[8].set_value(55)
    g.opts_cache[9].set_value(60)

    g.save_options()

    cfg = g.settings_manager
    assert cfg.get_ai_provider() == "openai"
    assert cfg.get_ai_model() == "gpt-4o-mini"
    assert cfg.get_ai_api_key() == "secret"
    assert cfg.get_birth_columns() == 4
    assert cfg.get_death_columns() == 2
    assert cfg.get_marriage_columns() == 5
    assert cfg.get_form_density() == "normal"
    assert cfg.get_person_name_length() == 42
    assert cfg.get_place_title_length() == 55
    assert cfg.get_citation_text_length() == 60