from __future__ import annotations

import sys
from pathlib import Path

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


def test_complete_form_validation(mock_gramps_env):
    """Test validation with complete form data like user would fill"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    # Create form state and context
    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state

    print(f"\n🎯 === Complete Form Validation Test ===")

    # Fill required common fields
    citation_obj = mock_gramps_env["citation"]
    place_obj = mock_gramps_env["place"]
    person_obj = mock_gramps_env["person"]

    form_state.set("common_box", "citation", citation_obj, allow_log=True)
    form_state.set("common_box", "marriage_place", place_obj, allow_log=True)

    # Fill groom data (like user would do in UI)
    form_state.set("groom_box", "subject_person.person", person_obj, allow_log=True)
    form_state.set("groom_box", "subject_person.original_name", "Іван", allow_log=True)
    form_state.set("groom_box", "subject_person.normalized_name", "Іван", allow_log=True)
    form_state.set("groom_box", "subject_person.original_surname", "Петренко", allow_log=True)
    form_state.set("groom_box", "subject_person.normalized_surname", "Петренко", allow_log=True)

    # Fill bride data (like user would do in UI)
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    bride_person = lib.Person("bride123", "I0002")

    form_state.set("bride_box", "subject_person.person", bride_person, allow_log=True)
    form_state.set("bride_box", "subject_person.original_name", "Марія", allow_log=True)
    form_state.set("bride_box", "subject_person.normalized_name", "Марія", allow_log=True)
    form_state.set("bride_box", "subject_person.original_surname", "Іванівна", allow_log=True)
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна", allow_log=True)

    # Check what's actually stored
    print(f"📋 Form state after filling:")
    print(f"Groom person: {form_state.get('groom_box', 'subject_person.person')}")
    print(f"Groom name: {form_state.get('groom_box', 'subject_person.original_name')}")
    print(f"Bride person: {form_state.get('bride_box', 'subject_person.person')}")
    print(f"Bride name: {form_state.get('bride_box', 'subject_person.original_name')}")

    # Run validation
    validator = MarriageValidator(ctx)
    issues = validator.validate()

    print(f"\n🔍 Validation Results:")
    print(f"Issues found: {len(issues)}")
    for issue in issues:
        print(f"  ❌ {issue.field}: {issue.message}")

    # Check each validation step manually
    print(f"\n🛠️ Step-by-step validation check:")

    # Required objects
    citation_found = bool(ctx.form_state.get_object("common_box", "citation"))
    place_found = bool(ctx.form_state.get_object("common_box", "marriage_place"))
    print(f"Citation found: {citation_found}")
    print(f"Place found: {place_found}")

    # Party validation for groom
    groom_sp = ctx.form_state.get("groom_box", "subject_person")
    groom_allow_empty = validator._allow_empty("groom_box")
    print(f"Groom subject_person: {groom_sp}")
    print(f"Groom allow_empty: {groom_allow_empty}")
    
    # Test that allow_empty defaults to False when not set
    assert groom_allow_empty is False, "allow_empty should default to False when not explicitly set"

    # Party validation for bride
    bride_sp = ctx.form_state.get("bride_box", "subject_person")
    bride_allow_empty = validator._allow_empty("bride_box")
    print(f"Bride subject_person: {bride_sp}")
    print(f"Bride allow_empty: {bride_allow_empty}")
    
    # Test that allow_empty defaults to False when not set
    assert bride_allow_empty is False, "allow_empty should default to False when not explicitly set"

    # Manual identity validation for bride
    if bride_sp:
        person_field = getattr(bride_sp, "person", None)
        names = [getattr(bride_sp, "original_name", None), getattr(bride_sp, "normalized_name", None)]
        surnames = [getattr(bride_sp, "original_surname", None), getattr(bride_sp, "normalized_surname", None)]

        print(f"Bride person_field: {person_field}")
        print(f"Bride names: {names}")
        print(f"Bride surnames: {surnames}")

        # Check if person object exists
        if isinstance(person_field, dict) and person_field.get("object") is not None:
            print(f"Bride has person object: YES")
        else:
            print(f"Bride has person object: NO")

        # Check if any names/surnames are non-empty
        any_names = any(n and str(n).strip() for n in names)
        any_surnames = any(s and str(s).strip() for s in surnames)
        print(f"Bride has names: {any_names}")
        print(f"Bride has surnames: {any_surnames}")

    # Assert validation should pass with complete data
    assert len(issues) == 0, f"Validation should pass with complete data, but got: {[i.message for i in issues]}"

    print(f"\n✅ Validation passed with complete form data")


def test_validation_error_cases(mock_gramps_env):
    """Test that validation properly catches missing required data"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state

    print(f"\n❌ === Testing Validation Error Cases ===")

    # Test 1: Missing citation
    place_obj = mock_gramps_env["place"]
    form_state.set("common_box", "marriage_place", place_obj, allow_log=True)

    validator = MarriageValidator(ctx)
    issues = validator.validate()

    citation_issue = any("Цитата" in i.message for i in issues)
    assert citation_issue, "Should detect missing citation"
    print("✓ Missing citation detected")

    # Test 2: Missing marriage place
    form_state = FormState()
    ctx.form_state = form_state
    citation_obj = mock_gramps_env["citation"]
    form_state.set("common_box", "citation", citation_obj, allow_log=True)

    validator = MarriageValidator(ctx)
    issues = validator.validate()

    place_issue = any("Місце" in i.message for i in issues)
    assert place_issue, "Should detect missing place"
    print("✓ Missing place detected")

    # Test 3: Missing person data
    form_state = FormState()
    ctx.form_state = form_state

    # Fill only common data
    form_state.set("common_box", "citation", citation_obj, allow_log=True)
    form_state.set("common_box", "marriage_place", place_obj, allow_log=True)

    validator = MarriageValidator(ctx)
    issues = validator.validate()

    person_issues = [i for i in issues if "персону" in i.message or "імʼя" in i.message]
    assert (
        len(person_issues) >= 2
    ), f"Should detect missing person data for both groom and bride, got: {[i.message for i in issues]}"
    print(f"✓ Missing person data detected: {len(person_issues)} issues")

    print(f"✅ All error cases properly detected")


def test_allow_empty_integration_in_existing_flow(mock_gramps_env):
    """Test allow_empty functionality within existing validation flow"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state

    print(f"\n🔄 === Allow Empty Integration Test ===")

    # Fill required common fields
    citation_obj = mock_gramps_env["citation"]
    place_obj = mock_gramps_env["place"]
    form_state.set("common_box", "citation", citation_obj, allow_log=True)
    form_state.set("common_box", "marriage_place", place_obj, allow_log=True)

    # Test scenario: groom with allow_empty=True, bride with allow_empty=False
    form_state.set("groom_box", "subject_person.allow_empty", True, allow_log=True)
    # No names for groom - should pass
    
    form_state.set("bride_box", "subject_person.allow_empty", False, allow_log=True)  
    form_state.set("bride_box", "subject_person.original_name", "Марія", allow_log=True)
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна", allow_log=True)

    # Verify allow_empty values are set correctly
    groom_allow_empty = ctx.form_state.get("groom_box", "subject_person.allow_empty")
    bride_allow_empty = ctx.form_state.get("bride_box", "subject_person.allow_empty")
    print(f"Groom allow_empty stored as: {groom_allow_empty} (type: {type(groom_allow_empty)})")
    print(f"Bride allow_empty stored as: {bride_allow_empty} (type: {type(bride_allow_empty)})")

    # Verify validator can read allow_empty correctly
    validator = MarriageValidator(ctx)
    groom_validator_result = validator._allow_empty("groom_box")
    bride_validator_result = validator._allow_empty("bride_box")
    print(f"Validator reads groom allow_empty as: {groom_validator_result}")
    print(f"Validator reads bride allow_empty as: {bride_validator_result}")
    
    assert groom_validator_result is True, "Validator should read groom allow_empty as True"
    assert bride_validator_result is False, "Validator should read bride allow_empty as False"

    # Run validation
    issues = validator.validate()
    print(f"Validation issues: {len(issues)}")
    for issue in issues:
        print(f"  - {issue.field}: {issue.message}")

    # Should pass because:
    # - Common fields are filled
    # - Groom has allow_empty=True (no validation required)
    # - Bride has names filled (validation passes)
    groom_issues = [i for i in issues if "Наречений" in i.field]
    assert len(groom_issues) == 0, f"Groom validation should pass with allow_empty=True, but got: {[i.message for i in groom_issues]}"

    print(f"✅ Allow empty integration test passed")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
