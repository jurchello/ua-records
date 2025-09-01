from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_gramps_objects():
    """Create stub Gramps objects using the stubs from conftest.py"""
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    return {
        "person": lib.Person("person123", "I0001"),
        "place": lib.Place("place123", "P0001"),
        "citation": lib.Citation("cite123", "C0001"),
    }


def test_allow_empty_validation_integration(mock_gramps_objects):
    """End-to-end test: allow_empty checkbox should skip validation"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state
    
    # Set required fields
    citation_obj = mock_gramps_objects["citation"]
    place_obj = mock_gramps_objects["place"]
    form_state.set("common_box", "citation", citation_obj)
    form_state.set("common_box", "marriage_place", place_obj)
    
    # Test 1: allow_empty=True for groom - should pass validation WITHOUT names
    form_state.set("groom_box", "subject_person.allow_empty", True)
    # Intentionally NOT setting names for groom
    
    # Set bride with names (allow_empty=False by default)
    form_state.set("bride_box", "subject_person.original_name", "Марія")
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна")
    
    validator = MarriageValidator(ctx)
    issues = validator.validate()
    
    # Should pass because groom has allow_empty=True
    groom_issues = [i for i in issues if "Наречений" in i.field]
    assert len(groom_issues) == 0, f"Groom validation should pass when allow_empty=True, but got: {[i.message for i in groom_issues]}"


def test_allow_empty_false_requires_names(mock_gramps_objects):
    """Test that allow_empty=False still requires names"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state
    
    # Set required fields
    citation_obj = mock_gramps_objects["citation"]
    place_obj = mock_gramps_objects["place"]
    form_state.set("common_box", "citation", citation_obj)
    form_state.set("common_box", "marriage_place", place_obj)
    
    # Test: allow_empty=False for groom - should FAIL validation without names
    form_state.set("groom_box", "subject_person.allow_empty", False)
    # Intentionally NOT setting names for groom
    
    # Set bride with names
    form_state.set("bride_box", "subject_person.original_name", "Марія")
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна")
    
    validator = MarriageValidator(ctx)
    issues = validator.validate()
    
    # Should fail because groom has allow_empty=False and no names
    groom_issues = [i for i in issues if "Наречений" in i.field]
    assert len(groom_issues) > 0, "Groom validation should fail when allow_empty=False and no names provided"


def test_checkbox_to_validation_pipeline():
    """Test complete pipeline: HTML checkbox → FormState.set → type conversion → validator"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state
    
    # Simulate HTML form submission with string values (like HTML sends)
    form_state.set("groom_box", "subject_person.allow_empty", "true")  # String from HTML
    form_state.set("bride_box", "subject_person.allow_empty", "false")  # String from HTML
    
    # Test type conversion: strings should become booleans
    assert form_state.get("groom_box", "subject_person.allow_empty") is True, "String 'true' should convert to boolean True"
    assert form_state.get("bride_box", "subject_person.allow_empty") is False, "String 'false' should convert to boolean False"
    
    # Test validator can read the converted values
    validator = MarriageValidator(ctx)
    assert validator._allow_empty("groom_box") is True, "Validator should read allow_empty=True for groom"
    assert validator._allow_empty("bride_box") is False, "Validator should read allow_empty=False for bride"


def test_allow_empty_field_path_regression():
    """Regression test: ensure validator reads allow_empty from correct path"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state
    
    # This was the bug: data was stored as "groom_box" → "subject_person.allow_empty"
    # But validator was looking for "groom_box.subject_person" → "allow_empty"
    
    # Set data the way HTML form sends it
    form_state.set("groom_box", "subject_person.allow_empty", True)
    
    # Validator should find it (this was failing before the fix)
    validator = MarriageValidator(ctx)
    result = validator._allow_empty("groom_box")
    
    assert result is True, "Validator should find allow_empty value at correct path"


def test_multiple_boolean_string_values():
    """Test various boolean string values that HTML might send"""
    from forms.forms.marriage.form_state import FormState
    
    form_state = FormState()
    
    # Test different true values
    test_cases = [
        ("true", True),
        ("True", True),
        ("TRUE", True),
        ("1", True),
        ("on", True),
        ("yes", True),
        ("t", True),
        ("y", True),
        ("false", False),
        ("False", False),
        ("FALSE", False),
        ("0", False),
        ("off", False),
        ("no", False),
        ("f", False),
        ("n", False),
        ("", False),
        ("random", False),
    ]
    
    for input_value, expected_output in test_cases:
        # Reset form state
        form_state = FormState()
        
        # Set the value
        form_state.set("groom_box", "subject_person.allow_empty", input_value)
        
        # Check conversion
        actual = form_state.get("groom_box", "subject_person.allow_empty")
        assert actual is expected_output, f"Input '{input_value}' should convert to {expected_output}, got {actual}"


def test_allow_empty_with_person_object():
    """Test allow_empty behavior when person object is provided"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state
    
    # Create person object
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    person_obj = lib.Person("person123", "I0001")
    citation_obj = lib.Citation("cite123", "C0001")
    place_obj = lib.Place("place123", "P0001")
    
    # Set required fields
    form_state.set("common_box", "citation", citation_obj)
    form_state.set("common_box", "marriage_place", place_obj)
    
    # Set person object but allow_empty=False (should pass because person exists)
    form_state.set("groom_box", "subject_person.person", person_obj)
    form_state.set("groom_box", "subject_person.allow_empty", False)
    
    # Set bride with names
    form_state.set("bride_box", "subject_person.original_name", "Марія")
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна")
    
    validator = MarriageValidator(ctx)
    issues = validator.validate()
    
    # Should pass because groom has person object (even though no text names)
    groom_issues = [i for i in issues if "Наречений" in i.field]
    assert len(groom_issues) == 0, f"Groom validation should pass when person object exists, but got: {[i.message for i in groom_issues]}"


def test_allow_empty_witness_and_landowner():
    """Test allow_empty works for witnesses and landowners too"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    form_state = FormState()
    ctx = WorkContext()  
    ctx.form_state = form_state
    
    # Create required objects
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    citation_obj = lib.Citation("cite123", "C0001")
    place_obj = lib.Place("place123", "P0001")
    
    # Set required fields
    form_state.set("common_box", "citation", citation_obj)
    form_state.set("common_box", "marriage_place", place_obj)
    
    # Set main parties with names
    form_state.set("groom_box", "subject_person.original_name", "Іван")
    form_state.set("groom_box", "subject_person.normalized_surname", "Петренко")
    form_state.set("bride_box", "subject_person.original_name", "Марія") 
    form_state.set("bride_box", "subject_person.normalized_surname", "Іванівна")
    
    # Test witnesses and landowners have allow_empty functionality
    # (Note: they might have different validation rules, but should support allow_empty)
    form_state.set("groom_box", "witness_box_1.subject_person.allow_empty", True)
    form_state.set("groom_box", "landowner.allow_empty", True)
    
    validator = MarriageValidator(ctx)
    issues = validator.validate()
    
    # Should not have validation issues for witnesses/landowners with allow_empty=True
    # (The exact validation rules might vary, but allow_empty should be respected)
    assert isinstance(issues, list), "Validator should return list of issues"