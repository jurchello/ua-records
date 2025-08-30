from __future__ import annotations

from typing import Any

from base_edit_form import BaseEditForm
from providers import FORM_REGISTRY


class EditForm(BaseEditForm):
    def __init__(self, *, dbstate: Any, uistate: Any, form_id: str) -> None:
        self._provider = FORM_REGISTRY.get(form_id)
        if not self._provider:
            raise KeyError(f"Unknown form_id: {form_id}")
        super().__init__(dbstate=dbstate, uistate=uistate, form_id=form_id)

    def get_form_config(self) -> dict:
        form_cfg = self._provider["form"]
        return form_cfg() if callable(form_cfg) else form_cfg

    def make_state(self):
        return self._provider["state_class"]()

    def make_validator(self, state):
        return self._provider["validator_class"](state)

    def make_ai_builder(self):
        fac = self._provider.get("ai_builder_factory")
        return fac(self.dbstate.db) if fac else None

    def get_reconciler(self):
        fac = self._provider.get("reconciler_factory")
        return fac(self.dbstate.db) if fac else None

    def make_processor(self, state):
        return self._provider["processor_factory"](state, self.dbstate, self.uistate)
