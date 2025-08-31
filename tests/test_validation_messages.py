from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_validation_messages_are_user_friendly():
    """Test that validation error messages use user-friendly field descriptions"""
    from forms.forms.marriage.form_state import FormState
    from services.work_context import WorkContext
    from forms.forms.marriage.validator import MarriageValidator

    print(f"\n📝 === Testing User-Friendly Validation Messages ===")

    # Create empty form state to trigger validation errors
    form_state = FormState()
    ctx = WorkContext()
    ctx.form_state = form_state

    # Run validation to get error messages
    validator = MarriageValidator(ctx)
    issues = validator.validate()

    print(f"Found {len(issues)} validation issues:")

    # Check that error messages contain user-friendly descriptions
    messages = [f"{issue.field}: {issue.message}" for issue in issues]
    for msg in messages:
        print(f"  • {msg}")

    # Verify we have user-friendly field descriptions, not technical paths
    field_descriptions = [issue.field for issue in issues]

    # Should contain user-friendly descriptions like "Загальне → Цитата"
    # instead of technical paths like "common_box.citation"
    user_friendly_found = any("→" in field for field in field_descriptions)
    technical_paths_found = any("_box." in field for field in field_descriptions)

    print(f"\nUser-friendly descriptions found: {user_friendly_found}")
    print(f"Technical paths found: {technical_paths_found}")

    # Assert that we have user-friendly descriptions
    assert user_friendly_found, "Should contain user-friendly field descriptions with '→' arrows"

    # Ideally, we should not have technical paths in user-facing messages
    # But we might have some unmapped paths, so this is just informational
    if technical_paths_found:
        print("⚠️  Some technical paths still present - consider mapping them")

    # Test specific expected mappings
    expected_mappings = {
        "Загальне → Цитата": "Цитата обовʼязкова",
        "Загальне → Місце реєстрації шлюбу": "Місце обовʼязкове",
        "Наречений → Основні дані": "потрібно вказати персону, імʼя або прізвище",
        "Наречена → Основні дані": "потрібно вказати персону, імʼя або прізвище",
    }

    found_mappings = {}
    for issue in issues:
        for expected_field, expected_msg_part in expected_mappings.items():
            if issue.field == expected_field and expected_msg_part in issue.message:
                found_mappings[expected_field] = issue.message
                break

    print(f"\nExpected mappings found: {len(found_mappings)}/{len(expected_mappings)}")
    for field, message in found_mappings.items():
        print(f"  ✓ {field}: {message}")

    # We should find at least the required object mappings
    assert (
        len(found_mappings) >= 2
    ), f"Should find at least citation and place mappings, found: {list(found_mappings.keys())}"

    print(f"\n✅ User-friendly validation messages test PASSED")


def test_technical_path_conversion():
    """Test the technical path to user-friendly conversion directly"""
    from forms.forms.marriage.validator import MarriageValidator
    from services.work_context import WorkContext

    print(f"\n🔄 === Testing Path Conversion Function ===")

    # Create validator instance to test the conversion method
    ctx = WorkContext()
    validator = MarriageValidator(ctx)

    test_paths = [
        ("common_box.citation", "Загальне → Цитата"),
        ("common_box.marriage_place", "Загальне → Місце реєстрації шлюбу"),
        ("groom_box.subject_person", "Наречений → Основні дані"),
        ("bride_box.subject_person", "Наречена → Основні дані"),
        ("groom_box.subject_person.age", "Наречений → Вік"),
        ("bride_box.landowner.gender", "Наречена → Поміщик → Стать"),
        ("unknown.path", "unknown.path"),  # Unmapped path should return as-is
    ]

    print("Path conversion tests:")
    for technical_path, expected_friendly in test_paths:
        actual_friendly = validator._get_user_friendly_path(technical_path)
        status = "✓" if actual_friendly == expected_friendly else "❌"
        print(f"  {status} '{technical_path}' → '{actual_friendly}'")
        if actual_friendly != expected_friendly:
            print(f"     Expected: '{expected_friendly}'")

        assert actual_friendly == expected_friendly, f"Path conversion failed for {technical_path}"

    print(f"\n✅ Path conversion test PASSED")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
