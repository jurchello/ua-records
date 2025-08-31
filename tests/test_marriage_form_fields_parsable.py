from __future__ import annotations

import pytest


def _iter_fields():
    from forms.forms.marriage.config import FORM_EXPANDED

    form = FORM_EXPANDED["marriage"]
    for tab in form.get("tabs", []):
        for frame in tab.get("frames", []):
            for f in frame.get("fields", []):
                yield f


def _get_field_group(field):
    """Get group name from field ID for progress tracking."""
    field_id = field.get("id", "")
    if not field_id:
        return "unknown"

    parts = field_id.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return parts[0]


# Group fields by prefix for better progress tracking
_grouped_fields = {}
for field in _iter_fields():
    group = _get_field_group(field)
    _grouped_fields.setdefault(group, []).append(field)

# Create parametrized test with group info
_test_params = []
for group_name, fields in _grouped_fields.items():
    for i, field in enumerate(fields):
        field_with_group = dict(field)
        field_with_group["_test_group"] = group_name
        field_with_group["_group_index"] = i + 1
        field_with_group["_group_total"] = len(fields)
        _test_params.append(field_with_group)


@pytest.mark.parametrize(
    "field",
    _test_params,
    ids=lambda f: f"{f.get('_test_group', 'unknown')}_{f.get('id', 'unknown').split('.')[-1]}[{f.get('_group_index', 0)}/{f.get('_group_total', 0)}]",
)
def test_all_marriage_fields_are_settable(field):
    t = field.get("type")
    fid = field.get("id")

    if not isinstance(t, str) or not isinstance(fid, str):
        return
    if "." not in fid:
        return  # пропускаємо некваліфіковані id

    prefix, rest = fid.split(".", 1)

    # Підтримувані типи для цього smoke-тесту
    supported = {
        "entry",
        "text",
        "textarea",
        "select",
        "date",
        "checkbox",
        "person",
        "place",
        "citation",
    }
    if t not in supported:
        return

    from forms.forms.marriage.form_state import FormState

    st = FormState()

    # Генерація простих валідних значень для запису
    if t in {"entry", "text", "textarea", "select"}:
        value = "x"
    elif t == "date":
        value = "1900-01-01"
    elif t == "checkbox":
        value = True
    elif t in {"person", "place", "citation"}:
        # Для DnD-полів достатньо словника-обгортки без object
        value = {"handle": "H", "gramps_id": "G"}
    else:
        value = "x"

    st.set(prefix, rest, value, allow_log=False)

    # Прогрес по групах (зручно у виводі pytest -s)
    group_name = field.get("_test_group", "unknown")
    group_index = field.get("_group_index", 0)
    group_total = field.get("_group_total", 0)
    field_name = fid.split(".")[-1]

    if group_index == 1:
        print(f"\n📋 Starting {group_name}: {group_total} fields")

    if group_index % 5 == 0 or group_index == group_total:
        progress = f"{group_index}/{group_total}"
        percent = f"{group_index / group_total * 100:.0f}%"
        print(f"   {group_name}: {progress} ({percent}) - current: {field_name}")
