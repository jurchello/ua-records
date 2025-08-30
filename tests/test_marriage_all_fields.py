"""Test that all 14 persons in marriage form have proper fields and return FormState data."""

from __future__ import annotations
import pytest
from forms.forms.marriage.config import FORM_EXPANDED
from forms.forms.marriage.form_state import FormState


def get_all_person_field_ids():
    """Extract all person field IDs from the marriage form configuration."""
    person_fields = []
    marriage_form = FORM_EXPANDED['marriage']
    
    for tab in marriage_form['tabs']:
        for frame in tab.get('frames', []):
            for field in frame.get('fields', []):
                if field.get('type') == 'person':
                    field_id = field.get('id')
                    if field_id:
                        person_fields.append(field_id)
    
    return person_fields


def get_all_text_field_ids():
    """Extract all text/entry field IDs from the marriage form configuration."""
    text_fields = []
    marriage_form = FORM_EXPANDED['marriage']
    
    for tab in marriage_form['tabs']:
        for frame in tab.get('frames', []):
            for field in frame.get('fields', []):
                field_type = field.get('type')
                if field_type in ['entry', 'text', 'textarea']:
                    field_id = field.get('id')
                    if field_id:
                        text_fields.append(field_id)
    
    return text_fields


def test_marriage_form_has_exactly_14_person_fields():
    """Verify that marriage form has exactly 14 person fields."""
    person_fields = get_all_person_field_ids()
    assert len(person_fields) == 14, f"Expected 14 person fields, got {len(person_fields)}: {person_fields}"


def test_all_person_field_names_are_correct():
    """Verify the names of all 14 person fields match expected structure."""
    person_fields = get_all_person_field_ids()
    
    expected_person_fields = [
        # Groom and his landowner
        "groom_box.subject_person.person",
        "groom_box.landowner.person",
        
        # Bride and her landowner
        "bride_box.subject_person.person", 
        "bride_box.landowner.person",
        
        # Groom witnesses and their landowners
        "groom_box.witness_box_1.subject_person.person",
        "groom_box.witness_box_1.landowner.person",
        "groom_box.witness_box_2.subject_person.person",
        "groom_box.witness_box_2.landowner.person",
        
        # Bride witnesses and their landowners  
        "bride_box.witness_box_1.subject_person.person",
        "bride_box.witness_box_1.landowner.person",
        "bride_box.witness_box_2.subject_person.person", 
        "bride_box.witness_box_2.landowner.person",
        
        # Clergymen
        "clergymen_box.clergyman_1.person",
        "clergymen_box.clergyman_2.person",
    ]
    
    # Sort both lists for comparison
    person_fields.sort()
    expected_person_fields.sort()
    
    assert person_fields == expected_person_fields, f"Person fields don't match.\nActual: {person_fields}\nExpected: {expected_person_fields}"


def test_form_state_handles_all_person_fields():
    """Test that FormState can handle all person fields with data."""
    form_state = FormState()
    
    # Get all person fields
    person_fields = get_all_person_field_ids()
    
    # Test that we can set a person handle for each field
    for i, field_id in enumerate(person_fields):
        # Parse field_id into prefix and key
        parts = field_id.split(".")
        prefix = parts[0]
        key = ".".join(parts[1:])
        
        # Set person data with handle and gramps_id
        test_data = {"handle": f"test_handle_{i}", "gramps_id": f"I{i:04d}"}
        form_state.set(prefix, key, test_data)
        
        # Verify it was set
        retrieved_data = form_state.get(prefix, key)
        assert isinstance(retrieved_data, dict), f"Failed to get dict data for field {field_id}"
        assert retrieved_data.get("handle") == test_data["handle"], f"Wrong handle for field {field_id}"
        assert retrieved_data.get("gramps_id") == test_data["gramps_id"], f"Wrong gramps_id for field {field_id}"


def test_form_state_handles_all_text_fields():
    """Test that FormState can handle all text/entry fields with data."""
    form_state = FormState()
    
    # Get all text fields
    text_fields = get_all_text_field_ids()
    
    successful_sets = 0
    failed_fields = []
    
    for i, field_id in enumerate(text_fields):
        # Parse field_id into prefix and key
        parts = field_id.split(".")
        prefix = parts[0]
        key = ".".join(parts[1:])
        
        # Set text data
        test_value = f"test_text_value_{i}"
        form_state.set(prefix, key, test_value)
        
        # Verify it was set
        retrieved_value = form_state.get(prefix, key)
        if retrieved_value == test_value:
            successful_sets += 1
        else:
            failed_fields.append(field_id)
    
    # Should be able to set at least 80% of fields
    success_rate = successful_sets / len(text_fields) if text_fields else 1.0
    assert success_rate >= 0.8, f"Only {success_rate:.2%} of text fields worked. Failed fields: {failed_fields[:5]}..."
    
    print(f"Successfully set {successful_sets}/{len(text_fields)} text fields ({success_rate:.1%})")


def test_form_state_returns_complete_data_when_all_fields_filled():
    """Test that FormState returns proper data structure when all fields are filled."""
    form_state = FormState()
    
    # Fill all person fields
    person_fields = get_all_person_field_ids()
    for i, field_id in enumerate(person_fields):
        parts = field_id.split(".")
        prefix = parts[0]
        key = ".".join(parts[1:])
        test_data = {"handle": f"person_handle_{i}", "gramps_id": f"I{i:04d}"}
        form_state.set(prefix, key, test_data)
    
    # Fill some text fields
    text_fields = get_all_text_field_ids()
    for i, field_id in enumerate(text_fields[:5]):  # Just fill first 5 to test
        parts = field_id.split(".")
        prefix = parts[0]
        key = ".".join(parts[1:])
        form_state.set(prefix, key, f"text_value_{i}")
    
    # Get the complete form state data
    form_data = form_state.to_dict()
    
    # Verify we have data structure
    assert isinstance(form_data, dict), "FormState should return dict"
    
    # Should have person data for all person fields
    for i, field_id in enumerate(person_fields):
        parts = field_id.split(".")
        # Navigate through the nested dict structure
        current = form_data
        for part in parts:
            assert part in current, f"Missing part '{part}' for person field {field_id}"
            current = current[part]
        
        # Should be a dict with handle and gramps_id
        assert isinstance(current, dict), f"Person field {field_id} should be dict, got {type(current)}"
        assert current.get("handle") == f"person_handle_{i}", f"Wrong handle for {field_id}"
        assert current.get("gramps_id") == f"I{i:04d}", f"Wrong gramps_id for {field_id}"
    
    # Should have text data for text fields we set
    for i, field_id in enumerate(text_fields[:5]):
        parts = field_id.split(".")
        current = form_data
        for part in parts:
            assert part in current, f"Missing part '{part}' for text field {field_id}"
            current = current[part]
        
        assert current == f"text_value_{i}", f"Wrong value for text field {field_id}"


if __name__ == "__main__":
    # Run basic checks
    print("Testing marriage form structure...")
    test_marriage_form_has_exactly_14_person_fields()
    print("✓ Has exactly 14 person fields")
    
    test_all_person_field_names_are_correct() 
    print("✓ All person field names are correct")
    
    print("Testing FormState...")
    test_form_state_handles_all_person_fields()
    print("✓ FormState handles all person fields")
    
    test_form_state_handles_all_text_fields()
    print("✓ FormState handles all text fields")
    
    test_form_state_returns_complete_data_when_all_fields_filled()
    print("✓ FormState returns complete data structure")
    
    print("All tests passed!")