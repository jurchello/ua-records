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
    
    # Extract first part as group
    parts = field_id.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return parts[0]


# Group fields by prefix for better progress tracking
_grouped_fields = {}
for field in _iter_fields():
    group = _get_field_group(field)
    if group not in _grouped_fields:
        _grouped_fields[group] = []
    _grouped_fields[group].append(field)

# Create parametrized test with group info
_test_params = []
for group_name, fields in _grouped_fields.items():
    for i, field in enumerate(fields):
        # Add group info to field for test naming
        field_with_group = dict(field)
        field_with_group["_test_group"] = group_name
        field_with_group["_group_index"] = i + 1
        field_with_group["_group_total"] = len(fields)
        _test_params.append(field_with_group)


@pytest.mark.parametrize("field", _test_params, 
                        ids=lambda f: f"{f.get('_test_group', 'unknown')}_{f.get('id', 'unknown').split('.')[-1]}[{f.get('_group_index', 0)}/{f.get('_group_total', 0)}]")
def test_all_marriage_fields_are_settable(field):
    t = field.get("type")
    mp = field.get("model_path") or field.get("id")  # Use id as fallback
    if not isinstance(t, str) or not isinstance(mp, str):
        return
    if "." not in mp:
        return
    prefix, rest = mp.split(".", 1)
    if t not in {"entry", "person", "place", "citation"}:
        return
    from forms.forms.marriage.form_state import FormState

    st = FormState()
    value = "x"
    st.set(prefix, rest, value, allow_log=False)
    
    # Print progress for groups
    group_name = field.get("_test_group", "unknown")
    group_index = field.get("_group_index", 0)
    group_total = field.get("_group_total", 0)
    field_name = field.get("id", "unknown").split(".")[-1]
    
    if group_index == 1:
        print(f"\n📋 Starting {group_name}: {group_total} fields")
    
    if group_index % 5 == 0 or group_index == group_total:
        progress = f"{group_index}/{group_total}"
        percent = f"{group_index/group_total*100:.0f}%"
        print(f"   {group_name}: {progress} ({percent}) - current: {field_name}")
