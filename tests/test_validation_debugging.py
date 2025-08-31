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
    """Mock minimal Gramps environment"""
    # Don't import actual gramps - mock it instead

    # Create mock objects
    mock_person = Mock()
    mock_person.get_handle.return_value = "person123"
    mock_person.get_gramps_id.return_value = "I0001"

    mock_place = Mock()
    mock_place.get_handle.return_value = "place123"
    mock_place.get_gramps_id.return_value = "P0001"

    mock_citation = Mock()
    mock_citation.get_handle.return_value = "cite123"
    mock_citation.get_gramps_id.return_value = "C0001"

    return {"person": mock_person, "place": mock_place, "citation": mock_citation}


def test_validation_structure_debugging(mock_gramps_env):
    """Debug validation issue - check what validator actually sees"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    # Create form state and context
    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state

    print("\n🔍 === Debugging Validation Structure ===")

    # Show initial dataclass structure
    print(f"\n📋 Initial dataclass structure:")
    print(f"form_state.typed = {form_state.typed}")
    print(f"form_state.typed.common_box = {form_state.typed.common_box}")
    print(f"form_state.typed.groom_box = {form_state.typed.groom_box}")
    print(f"form_state.typed.bride_box = {form_state.typed.bride_box}")

    # Test citation access
    print(f"\n🔗 Testing citation access:")
    citation_obj = mock_gramps_env["citation"]

    # Set citation in different ways to see what works
    print("Setting citation directly...")
    form_state.typed.common_box.citation = {"object": citation_obj, "handle": "cite123", "gramps_id": "C0001"}

    # Test validator access
    validator_citation = form_state.get_object("common_box", "citation")
    print(f"Validator sees citation object: {validator_citation}")
    print(f"Citation is None: {validator_citation is None}")
    print(f"Citation has handle: {getattr(validator_citation, 'get_handle', lambda: 'NO_HANDLE')()}")

    # Try via form_state.set method
    print(f"\nTesting via form_state.set method:")
    form_state.set("common_box", "citation", citation_obj, allow_log=True)
    validator_citation2 = form_state.get_object("common_box", "citation")
    print(f"After set() - validator sees: {validator_citation2}")

    # Test place access
    print(f"\n🏠 Testing place access:")
    place_obj = mock_gramps_env["place"]
    form_state.set("common_box", "marriage_place", place_obj, allow_log=True)
    validator_place = form_state.get_object("common_box", "marriage_place")
    print(f"Validator sees place object: {validator_place}")
    print(f"Place is None: {validator_place is None}")

    # Test person fields structure
    print(f"\n👤 Testing person structure:")
    person_obj = mock_gramps_env["person"]

    # Set person data
    form_state.set("groom_box", "subject_person.person", person_obj, allow_log=True)
    form_state.set("groom_box", "subject_person.original_name", "Іван", allow_log=True)
    form_state.set("groom_box", "subject_person.normalized_name", "Іван", allow_log=True)
    form_state.set("groom_box", "subject_person.original_surname", "Петренко", allow_log=True)
    form_state.set("groom_box", "subject_person.normalized_surname", "Петренко", allow_log=True)

    # Check what validator sees
    groom_person_dc = form_state.get("groom_box", "subject_person")
    print(f"Groom subject_person dataclass: {groom_person_dc}")
    print(f"Groom person object: {getattr(groom_person_dc, 'person', 'NOT_FOUND')}")
    print(f"Groom original_name: {getattr(groom_person_dc, 'original_name', 'NOT_FOUND')}")
    print(f"Groom normalized_name: {getattr(groom_person_dc, 'normalized_name', 'NOT_FOUND')}")

    # Test actual validation
    print(f"\n🔍 Running validator:")
    validator = MarriageValidator(ctx)
    issues = validator.validate()

    print(f"Validation issues found: {len(issues)}")
    for issue in issues:
        print(f"  ❌ {issue.field}: {issue.message}")

    # Manual checks of what validator methods see
    print(f"\n🛠️ Manual validator method checks:")

    # Check _required_objects
    citation_check = ctx.form_state.get_object("common_box", "citation")
    place_check = ctx.form_state.get_object("common_box", "marriage_place")
    print(f"citation check result: {citation_check}")
    print(f"place check result: {place_check}")
    print(f"citation bool: {bool(citation_check)}")
    print(f"place bool: {bool(place_check)}")

    # Check _allow_empty
    create_person1 = bool(ctx.form_state.get("groom_box", "create_person"))
    create_person2 = bool(ctx.form_state.get("groom_box.subject_person", "create_person"))
    print(f"create_person checks: {create_person1} or {create_person2} = {create_person1 or create_person2}")

    # Check _subject_person_dc
    subject_person = ctx.form_state.get("groom_box", "subject_person")
    print(f"subject_person dataclass: {subject_person}")
    print(f"subject_person type: {type(subject_person)}")
    if subject_person:
        print(f"  person field: {getattr(subject_person, 'person', 'MISSING')}")
        print(f"  original_name: {getattr(subject_person, 'original_name', 'MISSING')}")
        print(f"  normalized_name: {getattr(subject_person, 'normalized_name', 'MISSING')}")

    print(f"\n✅ === End Debugging ===")


def test_form_state_path_resolution():
    """Test how form_state resolves different path formats"""
    from forms.forms.marriage.form_state import FormState

    form_state = FormState()

    print(f"\n🛣️ Path resolution test:")

    # Test different path access methods
    paths_to_test = [
        ("common_box", "citation"),
        ("common_box", "marriage_place"),
        ("groom_box", "subject_person"),
        ("groom_box", "subject_person.person"),
        ("groom_box", "subject_person.original_name"),
        ("bride_box", "subject_person.person"),
    ]

    for prefix, key in paths_to_test:
        try:
            result = form_state._resolve_parent_and_attr(prefix, key)
            print(f"  {prefix}.{key} -> {result}")

            # Try to get the value
            value = form_state.get(prefix, key)
            print(f"    Current value: {value}")

        except Exception as e:
            print(f"  {prefix}.{key} -> ERROR: {e}")

    print("Done path testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
