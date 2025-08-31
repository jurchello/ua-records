from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_gramps_env():
    """Create stub Gramps objects using the stubs from conftest.py"""
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    return {
        "person": lib.Person("person123", "I0001"),
        "place": lib.Place("place123", "P0001"),
        "citation": lib.Citation("cite123", "C0001"),
    }


def create_mock_data_row(prefix: str, field_data: dict):
    """Create a mock DataRow with specified field data"""

    # Mock container widgets
    mock_widgets = {}
    for field_id, value in field_data.items():
        mock_widget = Mock()
        mock_widget.get_text = Mock(return_value=value)
        mock_widgets[field_id] = mock_widget

    # Mock DataRow
    mock_row = Mock()
    mock_row.prefix = prefix
    mock_row.widgets = mock_widgets
    mock_row.handles = {}
    mock_row.objects = {}
    mock_row._field_specs = {}

    return mock_row


def test_state_collector_data_flow():
    """Test that StateCollector properly collects data from UI to form_state"""
    from forms.forms.marriage.form_state import FormState
    from services.state_collector import StateCollector
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    print(f"\n🔄 === Testing StateCollector Data Flow ===")

    # Create form state
    form_state = FormState()

    # Mock UI rows with data like user would enter
    common_row = create_mock_data_row("common_box", {"tags_for_new_people": "test_tag"})

    groom_row = create_mock_data_row(
        "groom_box",
        {
            "subject_person_original_name": "Іван",
            "subject_person_normalized_name": "Іван",
            "subject_person_original_surname": "Петренко",
            "subject_person_normalized_surname": "Петренко",
        },
    )

    bride_row = create_mock_data_row(
        "bride_box",
        {
            "subject_person_original_name": "Марія",
            "subject_person_normalized_name": "Марія",
            "subject_person_original_surname": "Іванівна",
            "subject_person_normalized_surname": "Іванівна",
        },
    )

    # Collect data from rows
    print("🔍 Collecting data from UI rows...")
    StateCollector.collect_row(common_row, form_state, allow_log=True)
    StateCollector.collect_row(groom_row, form_state, allow_log=True)
    StateCollector.collect_row(bride_row, form_state, allow_log=True)

    # Check what was collected
    print(f"\n📋 Collected data:")
    print(f"Common tags: {form_state.get('common_box', 'tags_for_new_people')}")
    print(f"Groom original_name: {form_state.get('groom_box', 'subject_person_original_name')}")
    print(f"Groom normalized_name: {form_state.get('groom_box', 'subject_person_normalized_name')}")
    print(f"Bride original_name: {form_state.get('bride_box', 'subject_person_original_name')}")
    print(f"Bride normalized_name: {form_state.get('bride_box', 'subject_person_normalized_name')}")

    # Check nested access to subject_person
    groom_sp = form_state.get("groom_box", "subject_person")
    bride_sp = form_state.get("bride_box", "subject_person")
    print(f"Groom subject_person: {groom_sp}")
    print(f"Bride subject_person: {bride_sp}")

    if groom_sp:
        print(f"Groom subject_person.original_name: {getattr(groom_sp, 'original_name', 'NOT_FOUND')}")
    if bride_sp:
        print(f"Bride subject_person.original_name: {getattr(bride_sp, 'original_name', 'NOT_FOUND')}")

    print(f"✅ StateCollector data flow test complete")


def test_state_collector_with_objects(mock_gramps_env):
    """Test StateCollector with DnD objects (Person, Place, Citation)"""
    from forms.forms.marriage.form_state import FormState
    from services.state_collector import StateCollector
    from tests.conftest import ui_ids

    print(f"\n🎯 === Testing StateCollector with Objects ===")

    form_state = FormState()

    # Create mock row with objects using correct UI-id format
    common_row = Mock()
    common_row.prefix = "common_box"
    common_row.widgets = {}
    common_row.handles = ui_ids("common_box", {
        "common_box.citation": "cite123", 
        "common_box.marriage_place": "place123"
    })
    common_row.objects = ui_ids("common_box", {
        "common_box.citation": mock_gramps_env["citation"], 
        "common_box.marriage_place": mock_gramps_env["place"]
    })
    common_row._field_specs = {}

    groom_row = Mock()
    groom_row.prefix = "groom_box"
    groom_row.widgets = ui_ids("groom_box", {
        "groom_box.subject_person.original_name": Mock(get_text=lambda: "Іван"),
        "groom_box.subject_person.normalized_name": Mock(get_text=lambda: "Іван"),
    })
    groom_row.handles = ui_ids("groom_box", {
        "groom_box.subject_person.person": "person123"
    })
    groom_row.objects = ui_ids("groom_box", {
        "groom_box.subject_person.person": mock_gramps_env["person"]
    })
    groom_row._field_specs = {}

    # Collect data
    print("🔍 Collecting objects and text data...")
    StateCollector.collect_row(common_row, form_state, allow_log=True)
    StateCollector.collect_row(groom_row, form_state, allow_log=True)

    # Check objects
    citation_obj = form_state.get_object("common_box", "citation")
    place_obj = form_state.get_object("common_box", "marriage_place")
    person_obj = form_state.get_object("groom_box", "subject_person.person")

    print(f"\n📋 Objects collected:")
    print(f"Citation object: {citation_obj}")
    print(f"Place object: {place_obj}")
    print(f"Person object: {person_obj}")

    # Check text fields
    groom_name = form_state.get("groom_box", "subject_person.original_name")
    print(f"Groom name from text field: {groom_name}")

    # Test validation with collected data
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    ctx = WorkContext()
    ctx.form_state = form_state

    validator = MarriageValidator(ctx)
    issues = validator.validate()

    print(f"\n🔍 Validation after collection:")
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  ❌ {issue.field}: {issue.message}")

    # Citation and place should be found, but might have person identity issues
    assert form_state.get_object("common_box", "citation") is not None
    assert form_state.get_object("common_box", "marriage_place") is not None

    print(f"✅ Objects properly collected")


def test_field_id_mapping_issue():
    """Test potential issue with field ID mapping in StateCollector"""
    from services.state_collector import StateCollector

    print(f"\n🐛 === Testing Field ID Mapping Issues ===")

    # Test different field ID formats
    test_cases = [
        ("groom_box", "subject_person_original_name"),
        ("groom_box", "subject_person.original_name"),
        ("bride_box.subject_person", "original_name"),
    ]

    for prefix, field_id in test_cases:
        extracted_key = StateCollector._extract_raw_key(field_id, prefix)
        print(f"Prefix: '{prefix}', Field ID: '{field_id}' -> Extracted Key: '{extracted_key}'")

    # Check spacer detection
    spacer_tests = ["sp1", "_sp2", "__sp", "groom_box_sp1", "normal_field", "subject_person_name"]

    print(f"\n🕳️ Spacer detection tests:")
    for field_id in spacer_tests:
        is_spacer = StateCollector._is_spacer_field(field_id)
        print(f"'{field_id}' -> Spacer: {is_spacer}")

    print(f"✅ Field mapping tests complete")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
