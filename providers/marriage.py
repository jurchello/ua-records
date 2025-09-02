from __future__ import annotations

from typing import Any, Dict, Mapping, cast

from forms.forms.marriage.config import FORM_EXPANDED
from forms.forms.marriage.form_state import FormState
from forms.forms.marriage.validator import MarriageValidator
from forms.forms.marriage.processor import MarriageProcessor


def get_marriage_columns() -> int:
    try:
        # pylint: disable=import-outside-toplevel
        from settings.settings_manager import get_settings_manager

        return get_settings_manager().get_marriage_columns()
    except Exception:
        return 3


_FORM_MAP: Mapping[str, Dict[str, Any]] = cast(Mapping[str, Dict[str, Any]], FORM_EXPANDED)
_MARRIAGE_DEF: Dict[str, Any] = cast(Dict[str, Any], _FORM_MAP.get("marriage", {}))


def get_marriage_ui_form() -> Dict[str, Any]:
    base: Dict[str, Any] = dict(_MARRIAGE_DEF)
    base["columns"] = get_marriage_columns()
    return base


PROVIDER: Dict[str, Any] = {
    "id": _MARRIAGE_DEF.get("id", "marriage"),
    "title": _MARRIAGE_DEF.get("title", "Форма шлюбу"),
    "list_label": _MARRIAGE_DEF.get("list_label") or _MARRIAGE_DEF.get("title", "Форма шлюбу"),
    "form": get_marriage_ui_form,
    "form_state": FormState,
    "validator": MarriageValidator,
    "processor": MarriageProcessor,
}
