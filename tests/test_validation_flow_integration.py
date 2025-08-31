from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_gtk_widgets():
    """Mock GTK widgets properly for StateCollector"""
    with patch("services.state_collector.Gtk") as mock_gtk:

        # Mock Entry widget
        class MockEntry:
            def __init__(self, text=""):
                self._text = text

            def get_text(self):
                return self._text

            def set_text(self, text):
                self._text = text

        # Mock ComboBoxText widget
        class MockComboBoxText:
            def __init__(self, active_text=""):
                self._active_text = active_text

            def get_active_text(self):
                return self._active_text

            def set_active_text(self, text):
                self._active_text = text

        # Mock CheckButton widget
        class MockCheckButton:
            def __init__(self, active=False):
                self._active = active

            def get_active(self):
                return self._active

            def set_active(self, active):
                self._active = active

        # Mock EventBox container
        class MockEventBox:
            def __init__(self, child):
                self._child = child

            def get_child(self):
                return self._child

        mock_gtk.Entry = MockEntry
        mock_gtk.ComboBoxText = MockComboBoxText
        mock_gtk.CheckButton = MockCheckButton
        mock_gtk.EventBox = MockEventBox

        return {
            "Entry": MockEntry,
            "ComboBoxText": MockComboBoxText,
            "CheckButton": MockCheckButton,
            "EventBox": MockEventBox,
        }


@pytest.fixture
def mock_gramps_objects():
    """Create stub Gramps objects using the stubs from conftest.py"""
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    return {
        "person":   lib.Person("person123", "I0001"),
        "place":    lib.Place("place456", "P0001"),
        "citation": lib.Citation("cite789", "C0001"),
    }


def create_realistic_data_row(prefix: str, widgets: dict, objects: dict = None, handles: dict = None):
    """Create a realistic DataRow with proper GTK widgets"""

    mock_row = Mock()
    mock_row.prefix = prefix
    mock_row.widgets = widgets or {}
    mock_row.objects = objects or {}
    mock_row.handles = handles or {}
    mock_row._field_specs = {}

    return mock_row


def test_complete_validation_integration_flow(mock_gtk_widgets, mock_gramps_objects):
    """Test complete validation flow: UI -> StateCollector -> FormState -> Validator"""
    from forms.forms.marriage.form_state import FormState
    from services.state_collector import StateCollector
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator
    from tests.conftest import ui_ids

    print(f"\n🔄 === Complete Validation Integration Test ===")

    # Step 1: Create form state
    form_state = FormState()

    # Step 2: Create realistic UI data rows with proper GTK widgets
    # Common row (DnD об'єкти)
    common_row = create_realistic_data_row(
        prefix="common_box",
        widgets=ui_ids("common_box", {
            "common_box.tags_for_new_people": mock_gtk_widgets["Entry"]("test,tag"),
        }),
        objects=ui_ids("common_box", {
            "common_box.citation":       mock_gramps_objects["citation"],
            "common_box.marriage_place": mock_gramps_objects["place"],
        }),
        handles=ui_ids("common_box", {
            "common_box.citation":       "cite789",
            "common_box.marriage_place": "place456",
        }),
    )

    # Groom row
    groom_row = create_realistic_data_row(
        prefix="groom_box",
        widgets=ui_ids("groom_box", {
            "groom_box.subject_person.original_name":       mock_gtk_widgets["Entry"]("Іван"),
            "groom_box.subject_person.normalized_name":     mock_gtk_widgets["Entry"]("Іван"),
            "groom_box.subject_person.original_surname":    mock_gtk_widgets["Entry"]("Петренко"),
            "groom_box.subject_person.normalized_surname":  mock_gtk_widgets["Entry"]("Петренко"),
            "groom_box.subject_person.gender":              mock_gtk_widgets["ComboBoxText"]("Чоловік"),
            "groom_box.subject_person.age":                 mock_gtk_widgets["Entry"]("25"),
        }),
        objects=ui_ids("groom_box", {
            "groom_box.subject_person.person": mock_gramps_objects["person"],
        }),
        handles=ui_ids("groom_box", {
            "groom_box.subject_person.person": "person123",
        }),
    )

    # Bride row
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    bride_person = lib.Person("bride456", "I0002")

    bride_row = create_realistic_data_row(
        prefix="bride_box",
        widgets=ui_ids("bride_box", {
            "bride_box.subject_person.original_name":       mock_gtk_widgets["Entry"]("Марія"),
            "bride_box.subject_person.normalized_name":     mock_gtk_widgets["Entry"]("Марія"),
            "bride_box.subject_person.original_surname":    mock_gtk_widgets["Entry"]("Іванівна"),
            "bride_box.subject_person.normalized_surname":  mock_gtk_widgets["Entry"]("Іванівна"),
            "bride_box.subject_person.gender":              mock_gtk_widgets["ComboBoxText"]("Жінка"),
            "bride_box.subject_person.age":                 mock_gtk_widgets["Entry"]("22"),
        }),
        objects=ui_ids("bride_box", {
            "bride_box.subject_person.person": bride_person,
        }),
        handles=ui_ids("bride_box", {
            "bride_box.subject_person.person": "bride456",
        }),
    )

    # Step 3: Use StateCollector to collect data from UI rows
    print("📥 Collecting data from UI rows...")
    StateCollector.collect_row(common_row, form_state, allow_log=True)
    StateCollector.collect_row(groom_row, form_state, allow_log=True)
    StateCollector.collect_row(bride_row, form_state, allow_log=True)

    # Step 4: Verify data was collected properly
    print(f"\n📋 Collected data verification:")

    # Check objects
    citation = form_state.get_object("common_box", "citation")
    place = form_state.get_object("common_box", "marriage_place")
    groom_person = form_state.get_object("groom_box", "subject_person.person")
    bride_person_obj = form_state.get_object("bride_box", "subject_person.person")

    print(f"Citation collected: {citation is not None}")
    print(f"Place collected: {place is not None}")
    print(f"Groom person collected: {groom_person is not None}")
    print(f"Bride person collected: {bride_person_obj is not None}")

    # Check text fields
    groom_name = form_state.get("groom_box", "subject_person.original_name")
    bride_name = form_state.get("bride_box", "subject_person.original_name")
    groom_surname = form_state.get("groom_box", "subject_person.original_surname")
    bride_surname = form_state.get("bride_box", "subject_person.original_surname")

    print(f"Groom name: '{groom_name}'")
    print(f"Bride name: '{bride_name}'")
    print(f"Groom surname: '{groom_surname}'")
    print(f"Bride surname: '{bride_surname}'")

    # Check nested dataclass access
    groom_subject = form_state.get("groom_box", "subject_person")
    bride_subject = form_state.get("bride_box", "subject_person")

    print(f"Groom subject_person dataclass: {groom_subject is not None}")
    print(f"Bride subject_person dataclass: {bride_subject is not None}")

    if groom_subject:
        print(f"  Groom subject.original_name: '{getattr(groom_subject, 'original_name', None)}'")
        print(f"  Groom subject.person: {getattr(groom_subject, 'person', None) is not None}")

    if bride_subject:
        print(f"  Bride subject.original_name: '{getattr(bride_subject, 'original_name', None)}'")
        print(f"  Bride subject.person: {getattr(bride_subject, 'person', None) is not None}")

    # Step 5: Run validation
    print(f"\n🔍 Running validation...")
    ctx = WorkContext()
    ctx.form_state = form_state

    validator = MarriageValidator(ctx)
    issues = validator.validate()

    print(f"Validation issues found: {len(issues)}")
    for issue in issues:
        print(f"  ❌ {issue.field}: {issue.message}")

    # Step 6: Assertions
    # With complete data, validation should pass
    assert citation is not None, "Citation should be collected"
    assert place is not None, "Place should be collected"
    # Check dataclass contains the data even if direct field access returns None
    assert groom_subject is not None, "Groom subject_person should exist"
    assert bride_subject is not None, "Bride subject_person should exist"

    # Most importantly - validation should pass with complete data
    if len(issues) > 0:
        print(f"\n❌ VALIDATION FAILED - this indicates a problem in the data flow:")
        for issue in issues:
            print(f"  - {issue.field}: {issue.message}")

        # Debug what validator actually sees
        print(f"\n🔍 Debug validator data access:")
        groom_sp_debug = ctx.form_state.get("groom_box", "subject_person")
        bride_sp_debug = ctx.form_state.get("bride_box", "subject_person")
        citation_debug = ctx.form_state.get_object("common_box", "citation")
        place_debug = ctx.form_state.get_object("common_box", "marriage_place")

        print(f"  Validator sees citation: {citation_debug is not None}")
        print(f"  Validator sees place: {place_debug is not None}")
        print(f"  Validator sees groom subject_person: {groom_sp_debug is not None}")
        print(f"  Validator sees bride subject_person: {bride_sp_debug is not None}")

        if groom_sp_debug:
            print(f"  Groom has person object: {getattr(groom_sp_debug, 'person', None) is not None}")
            print(f"  Groom has names: {getattr(groom_sp_debug, 'original_name', None)}")

        if bride_sp_debug:
            print(f"  Bride has person object: {getattr(bride_sp_debug, 'person', None) is not None}")
            print(f"  Bride has names: {getattr(bride_sp_debug, 'original_name', None)}")

    # This should pass with complete data
    assert len(issues) == 0, f"Validation should pass with complete data, but got: {[i.message for i in issues]}"

    print(f"\n✅ Complete validation integration test PASSED")


def test_validation_missing_data_cases(mock_gtk_widgets, mock_gramps_objects):
    """Test that validation properly detects missing data"""
    from forms.forms.marriage.form_state import FormState
    from services.state_collector import StateCollector
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator
    from tests.conftest import ui_ids

    print(f"\n❌ === Testing Missing Data Detection ===")

    # Test case: Missing citation
    form_state = FormState()

    # Only place, no citation
    common_row = create_realistic_data_row(
        prefix="common_box",
        widgets={},
        objects=ui_ids("common_box", {"common_box.marriage_place": mock_gramps_objects["place"]}),
        handles=ui_ids("common_box", {"common_box.marriage_place": "place456"}),
    )

    StateCollector.collect_row(common_row, form_state, allow_log=True)

    ctx = WorkContext()
    ctx.form_state = form_state
    validator = MarriageValidator(ctx)
    issues = validator.validate()

    citation_missing = any("Цитата" in i.message for i in issues)
    assert citation_missing, "Should detect missing citation"
    print("✓ Missing citation properly detected")

    # Test case: Missing person data
    form_state = FormState()

    # Full common data but no person data
    common_row = create_realistic_data_row(
        prefix="common_box",
        widgets={},
        objects=ui_ids("common_box", {
            "common_box.citation": mock_gramps_objects["citation"], 
            "common_box.marriage_place": mock_gramps_objects["place"]
        }),
        handles=ui_ids("common_box", {
            "common_box.citation": "cite789", 
            "common_box.marriage_place": "place456"
        }),
    )

    # Empty groom/bride rows
    groom_row = create_realistic_data_row(prefix="groom_box", widgets={})
    bride_row = create_realistic_data_row(prefix="bride_box", widgets={})

    StateCollector.collect_row(common_row, form_state, allow_log=True)
    StateCollector.collect_row(groom_row, form_state, allow_log=True)
    StateCollector.collect_row(bride_row, form_state, allow_log=True)

    ctx = WorkContext()
    ctx.form_state = form_state
    validator = MarriageValidator(ctx)
    issues = validator.validate()

    person_issues = [i for i in issues if "персону" in i.message or "імʼя" in i.message]
    assert (
        len(person_issues) >= 2
    ), f"Should detect missing person data for both groom and bride, got {len(person_issues)} issues"
    print(f"✓ Missing person data properly detected: {len(person_issues)} issues")

    print(f"✅ Missing data detection tests PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
