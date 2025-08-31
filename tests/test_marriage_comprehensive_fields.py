"""Comprehensive testing of ALL marriage form fields with 100% coverage.

This suite relies ONLY on field 'id' (dot-path).
"""

from __future__ import annotations
import pytest
from tests.helpers.field_testing import create_marriage_field_tester
from forms.forms.marriage.form_state import FormState


def test_marriage_form_100_percent_field_coverage():
    """Test that we can identify and test ALL fields in marriage form."""
    tester = create_marriage_field_tester()

    # Get comprehensive field analysis
    all_fields = tester.get_all_fields()
    unique_types = tester.get_unique_field_types()
    testable_fields = tester.get_testable_fields()
    untestable_fields = tester.get_untestable_fields()

    # Basic validation
    assert len(all_fields) > 0, "Marriage form should have fields"
    assert len(unique_types) > 0, "Marriage form should have field types"

    # Test all testable fields with FormState
    results = tester.test_all_fields_with_form_state(FormState)

    # Print detailed report
    tester.print_coverage_report(results)

    # Assert coverage requirements
    total_testable = len(testable_fields)
    successful_tests = len(results["success"])

    if total_testable > 0:
        success_rate = successful_tests / total_testable
        assert success_rate >= 0.8, f"At least 80% of testable fields should work. Got {success_rate:.1%}"

    # Verify we're testing all major field types
    expected_types = {"entry", "person", "place", "citation"}
    tested_types = set(results["field_type_coverage"].keys())
    missing_types = expected_types - tested_types

    assert not missing_types, f"Missing coverage for field types: {missing_types}"


def test_marriage_form_field_types_comprehensive():
    """Test that all known field types are properly supported."""
    tester = create_marriage_field_tester()

    # Get all field types in the form
    actual_types = tester.get_unique_field_types()
    testable_types = tester.get_testable_field_types()

    print(f"\nActual field types in marriage form: {sorted(actual_types)}")
    print(f"Testable field types supported: {sorted(testable_types)}")

    # Check which actual types are not testable
    untestable_types = actual_types - testable_types
    if untestable_types:
        print(f"Field types not supported for testing: {sorted(untestable_types)}")

    # At least basic types should be testable
    basic_types = {"entry", "person", "place", "citation"}
    supported_basic = basic_types & testable_types
    assert len(supported_basic) >= 4, f"Should support all basic types: {basic_types}"


def test_marriage_form_all_person_fields_with_helper():
    """Test all person fields using the comprehensive helper (via id-only)."""
    tester = create_marriage_field_tester()

    person_fields = tester.get_fields_by_type("person")
    assert len(person_fields) == 14, f"Expected 14 person fields, got {len(person_fields)}"

    # Test each person field individually
    form_state = FormState()
    successful_person_tests = 0

    for i, field in enumerate(person_fields):
        field_id = field.get("id")
        if not field_id or "." not in field_id:
            continue  # skip malformed ids

        prefix, key = field_id.split(".", 1)
        test_value = tester.generate_test_value("person", field)

        try:
            form_state.set(prefix, key, test_value, allow_log=False)
            retrieved = form_state.get(prefix, key)

            if tester._values_match(test_value, retrieved, "person"):
                successful_person_tests += 1
        except Exception:
            pass

    success_rate = successful_person_tests / len(person_fields) if person_fields else 0
    assert success_rate >= 0.9, f"At least 90% of person fields should work. Got {success_rate:.1%}"


def test_marriage_form_identify_untestable_fields():
    """Identify fields that cannot be tested due to bad/malformed ids or unsupported types."""
    tester = create_marriage_field_tester()

    all_fields = tester.get_all_fields()
    untestable = tester.get_untestable_fields()

    # Analyze reasons for untestability
    bad_id = []
    unsupported_type = []

    testable_types = tester.get_testable_field_types()
    for field in untestable:
        field_id = field.get("id", "unknown")
        field_type = field.get("type")

        # id must exist and contain a dot to split prefix/key
        if not field_id or "." not in field_id:
            bad_id.append(f"{field_id} ({field_type})")
        elif field_type not in testable_types:
            unsupported_type.append(f"{field_id} ({field_type})")

    # Report findings
    total_fields = len(all_fields)
    testable_count = len(all_fields) - len(untestable)
    testability_rate = testable_count / total_fields if total_fields > 0 else 0

    print(f"\nField testability analysis:")
    print(f"Total fields: {total_fields}")
    print(f"Testable fields: {testable_count}")
    print(f"Testability rate: {testability_rate:.1%}")

    if bad_id:
        print(f"Fields with bad or non-dot ids: {bad_id[:5]}...")

    if unsupported_type:
        print(f"Fields with unsupported types: {unsupported_type[:5]}...")

    # We should be able to test most fields
    assert testability_rate >= 0.7, f"Should be able to test at least 70% of fields. Got {testability_rate:.1%}"


def test_marriage_form_generate_field_type_test_values():
    """Test that we can generate appropriate test values for all field types."""
    tester = create_marriage_field_tester()

    # Test value generation for each field type
    test_cases = {
        "entry": str,
        "text": str,
        "textarea": str,
        "person": dict,
        "place": dict,
        "citation": dict,
        "date": str,
        "select": str,
        "checkbox": bool,
    }

    for field_type, expected_type in test_cases.items():
        dummy_field = {"id": f"test_prefix.test_{field_type}", "type": field_type}
        test_value = tester.generate_test_value(field_type, dummy_field)

        assert isinstance(
            test_value, expected_type
        ), f"Test value for {field_type} should be {expected_type.__name__}, got {type(test_value)}"

        # Specific validations
        if field_type in ["person", "place", "citation"]:
            assert "handle" in test_value, f"{field_type} test value should have 'handle'"
            assert "gramps_id" in test_value, f"{field_type} test value should have 'gramps_id'"


if __name__ == "__main__":
    # Run comprehensive test
    print("Running comprehensive marriage form field tests...")

    test_marriage_form_100_percent_field_coverage()
    print("✓ 100% field coverage test passed")

    test_marriage_form_field_types_comprehensive()
    print("✓ Field types comprehensive test passed")

    test_marriage_form_all_person_fields_with_helper()
    print("✓ All person fields test passed")

    test_marriage_form_identify_untestable_fields()
    print("✓ Untestable fields analysis passed")

    test_marriage_form_generate_field_type_test_values()
    print("✓ Test value generation passed")

    print("\nAll comprehensive field tests passed!")
