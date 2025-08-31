from __future__ import annotations
from typing import Any, Iterable, List

import gi
gi.require_version("Gtk", "3.0") # pylint: disable=wrong-import-position
from gi.repository import Gtk

from services.work_context import WorkContext

class ValidationIssue:
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message


class ValidatorBase:
    def __init__(self, ctx: WorkContext) -> None:
        self.ctx = ctx
        self.issues: List[ValidationIssue] = []

    def add(self, field: str, message: str) -> None:
        self.issues.append(ValidationIssue(field, message))

    def ok(self) -> bool:
        return not self.issues

    def result_messages(self) -> List[str]:
        return [f"{i.field}: {i.message}" if i.field else i.message for i in self.issues]

    def _has_attr(self, dc: Any, name: str) -> bool:
        return dc is not None and (hasattr(dc, name) or (isinstance(dc, dict) and name in dc))

    def _get_attr(self, dc: Any, name: str) -> Any:
        if dc is None:
            return None
        if isinstance(dc, dict):
            return dc.get(name)
        return getattr(dc, name, None)

    def _is_empty(self, v: Any) -> bool:
        if v is None:
            return True
        if isinstance(v, str):
            return v == ""
        return False

    def _nonempty(self, v: Any) -> bool:
        return not self._is_empty(v)

    def _any_nonempty(self, vals: Iterable[Any]) -> bool:
        for v in vals:
            if self._nonempty(v):
                return True
        return False

    def validate_age_dc(
        self, dc: Any, *, field: str = "age", lo: int = 0, hi: int = 120, field_path: str = "", label: str = ""
    ) -> None:
        if not self._has_attr(dc, field):
            return
        v = self._get_attr(dc, field)
        if self._is_empty(v):
            return
        if not isinstance(v, int):
            self.add(field_path or field, f"{label}: вік має бути цілим числом")
            return
        if not lo <= v <= hi:
            self.add(field_path or field, f"{label}: вік має бути від {lo} до {hi}")

    def validate_choice_dc(
        self, dc: Any, *, field: str, allowed: Iterable[Any], field_path: str = "", label: str = ""
    ) -> None:
        if not self._has_attr(dc, field):
            return
        v = self._get_attr(dc, field)
        if self._is_empty(v):
            return
        if v not in set(allowed):
            self.add(field_path or field, f"{label}: значення має бути з дозволеного переліку")

    def validate_int_range_dc(
        self, dc: Any, *, field: str, lo: int, hi: int, field_path: str = "", label: str = ""
    ) -> None:
        if not self._has_attr(dc, field):
            return
        v = self._get_attr(dc, field)
        if self._is_empty(v):
            return
        if not isinstance(v, int):
            self.add(field_path or field, f"{label}: значення має бути цілим числом")
            return
        if not lo <= v <= hi:
            self.add(field_path or field, f"{label}: значення має бути {lo}..{hi}")

    def validate_min_identity_dc(
        self,
        dc: Any,
        *,
        person_field: str = "person",
        name_fields: Iterable[str] = (),
        surname_fields: Iterable[str] = (),
        allow_empty: bool = False,
        field_path: str = "",
        label: str = "",
    ) -> None:
        if allow_empty:
            return
        person = None
        if self._has_attr(dc, person_field):
            pv = self._get_attr(dc, person_field)
            if isinstance(pv, dict) and pv.get("object") is not None:
                person = pv.get("object")
        names = [self._get_attr(dc, n) for n in name_fields if self._has_attr(dc, n)]
        surnames = [self._get_attr(dc, s) for s in surname_fields if self._has_attr(dc, s)]
        if not self._any_nonempty([person] + names + surnames):
            self.add(field_path or person_field, f"{label}: потрібно вказати персону, імʼя або прізвище")

    def validate(self) -> List[ValidationIssue]:
        return self.issues

    def show_errors(self, parent=None, title: str = "Помилки валідації") -> bool:
        if not self.issues:
            return False
        text = "\n".join("• " + m for m in self.result_messages()) or "Невідомі помилки"
        try:
            dialog = Gtk.MessageDialog(
                parent=parent, flags=0, type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, message_format=title
            )
            dialog.format_secondary_text(text)
            dialog.run()
            dialog.destroy()
        except Exception:
            try:
                print(title)
                print(text)
            except Exception:
                pass
        return True
