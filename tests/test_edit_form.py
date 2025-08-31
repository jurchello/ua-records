import sys
import types

import pytest


def _install_minimal_env():
    for k in list(sys.modules):
        if k in {"base_edit_form", "providers", "edit_form"}:
            sys.modules.pop(k, None)

    base_edit_form_mod = types.ModuleType("base_edit_form")

    class BaseEditForm:
        def __init__(self, *, dbstate, uistate, form_id):
            self.dbstate = dbstate
            self.uistate = uistate
            self.form_id = form_id

    setattr(base_edit_form_mod, "BaseEditForm", BaseEditForm)
    sys.modules["base_edit_form"] = base_edit_form_mod

    providers_mod = types.ModuleType("providers")

    class _State:
        def __init__(self):
            self.touched = True

    class _Validator:
        def __init__(self, state):
            self.state = state

    class _Processor:
        def __init__(self, work_context, dbstate, uistate):
            self.work_context = work_context
            self.db = dbstate
            self.ui = uistate

    calls = {"ai_builder": [], "reconciler": []}

    def _ai_factory(db):
        calls["ai_builder"].append(db)
        return {"ai": "ok", "db": db}

    def _reconciler_factory(db):
        calls["reconciler"].append(db)
        return {"reconciler": "ok", "db": db}

    def _form_fn():
        return {
            "id": "x",
            "title": "X",
            "columns": 2,
            "tabs": [{"id": "t1", "frames": [{"fields": [{"id": "a", "type": "entry"}]}]}],
        }

    setattr(
        providers_mod,
        "FORM_REGISTRY",
        {
            "x": {
                "id": "x",
                "title": "X",
                "list_label": "X list",
                "form": _form_fn,
                "form_state": _State,
                "validator_class": _Validator,
                "processor_factory": _Processor,
                "ai_builder_factory": _ai_factory,
                "reconciler_factory": _reconciler_factory,
            }
        },
    )
    sys.modules["providers"] = providers_mod
    return calls


class _DB:
    def __init__(self):
        self.db = object()


class _UI:
    pass


def test_edit_form_provider_hooks():
    calls = _install_minimal_env()
    from edit_form import EditForm

    dbs, uis = _DB(), _UI()
    ef = EditForm(dbstate=dbs, uistate=uis, form_id="x")

    cfg = ef.get_form_config()
    assert isinstance(cfg, dict) and cfg.get("id") == "x" and cfg.get("columns") == 2

    st = ef.make_form_state()
    assert getattr(st, "touched", False) is True

    v = ef.make_validator(st)
    assert getattr(v, "state", None) is st

    aib = ef.make_ai_builder()
    rec = ef.get_reconciler()
    assert aib and aib["db"] is dbs.db
    assert rec and rec["db"] is dbs.db
    assert calls["ai_builder"] == [dbs.db]
    assert calls["reconciler"] == [dbs.db]

    # Тепер processor очікує WorkContext, але в тесті ми передаємо просто state
    # Це буде оновлено коли буде реальний WorkContext
    proc = ef.make_processor(st)
    assert getattr(proc, "work_context", None) is st and proc.db is dbs and proc.ui is uis


def test_edit_form_unknown_id_raises():
    _install_minimal_env()
    from edit_form import EditForm

    with pytest.raises(KeyError):
        EditForm(dbstate=_DB(), uistate=_UI(), form_id="nope")
