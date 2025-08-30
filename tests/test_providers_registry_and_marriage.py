from __future__ import annotations

import importlib
import sys
import types

import pytest


def _purge(*mods: str) -> None:
    for m in mods:
        sys.modules.pop(m, None)


def test_marriage_provider_columns_reflect_settings(monkeypatch):
    _purge("providers", "providers.marriage")
    import providers.marriage as marriage

    monkeypatch.setattr(marriage, "get_marriage_columns", lambda: 7, raising=True)
    form = marriage.get_marriage_ui_form()
    assert isinstance(form, dict)
    assert form.get("columns") == 7


def test_providers_registry_rejects_invalid_form():
    _purge("providers", "providers.__init__")
    impl = importlib.import_module("providers.__init__")

    with pytest.raises(RuntimeError):
        impl._form_obj_from({"a": 1, "b": 2})  # type: ignore[attr-defined]

    with pytest.raises(RuntimeError):
        impl._form_obj_from({"id": "bad", "title": "Bad"})
