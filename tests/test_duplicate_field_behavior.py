"""Test behavior with duplicate field IDs and visibility conditions."""

from __future__ import annotations
import pytest
from forms.forms.marriage.form_state import FormState


def test_duplicate_military_rank_field_behavior():
    """Test what happens when both military_rank fields have the same ID."""
    form_state = FormState()

    # Simulate scenario: user fills both fields but only one should be visible
    prefix = "groom_box"
    key = "landowner.military_rank"

    # First set male military rank
    male_value = "Полковник"
    form_state.set(prefix, key, male_value, allow_log=False)

    # Check what we get
    retrieved1 = form_state.get(prefix, key)
    assert retrieved1 == male_value, f"Expected {male_value}, got {retrieved1}"

    # Then set female military rank (simulating overwrite)
    female_value = "Полковникова"
    form_state.set(prefix, key, female_value, allow_log=False)

    # Check what we get now
    retrieved2 = form_state.get(prefix, key)
    assert retrieved2 == female_value, f"Expected {female_value}, got {retrieved2}"

    print(f"Male value: {male_value}")
    print(f"Female value: {female_value}")
    print(f"Final stored value: {retrieved2}")
    print("✓ Last write wins - female value overwrote male value")


def test_military_rank_vs_regular_person_fields():
    """Compare military_rank behavior between landowner (duplicate) and regular person (single)."""
    form_state = FormState()

    # Test regular person military_rank (single field)
    form_state.set("bride_box", "subject_person.military_rank", "Майорша", allow_log=False)
    regular_value = form_state.get("bride_box", "subject_person.military_rank")

    # Test landowner military_rank (duplicate fields with same ID)
    form_state.set("bride_box", "landowner.military_rank", "Полковникова", allow_log=False)
    landowner_value = form_state.get("bride_box", "landowner.military_rank")

    print(f"Regular person military_rank: {regular_value}")
    print(f"Landowner military_rank: {landowner_value}")

    assert regular_value == "Майорша"
    assert landowner_value == "Полковникова"
    print("✓ Both types of military_rank work correctly")


def test_state_collector_behavior_simulation():
    """Simulate how StateCollector would handle duplicate IDs."""
    form_state = FormState()
    prefix = "groom_box"
    key = "landowner.military_rank"

    # Simulate StateCollector processing fields in order
    print("Simulating StateCollector.collect_row() behavior:")

    # First field processed (male military rank)
    print("1. Processing male military rank field...")
    form_state.set(prefix, key, "Капітан", allow_log=False)
    value_after_first = form_state.get(prefix, key)
    print(f"   Value after first field: {value_after_first}")

    # Second field processed (female military rank)
    print("2. Processing female military rank field...")
    form_state.set(prefix, key, "Капітанша", allow_log=False)
    value_after_second = form_state.get(prefix, key)
    print(f"   Value after second field: {value_after_second}")

    # The question: which value should we keep?
    print(f"\n🤔 Problem: Both fields have same ID but different values")
    print(f"   - Male field would set: 'Капітан'")
    print(f"   - Female field would set: 'Капітанша'")
    print(f"   - Final stored value: '{value_after_second}'")
    print(f"   - Result: Last processed field wins (order dependent!)")


def test_field_visibility_logic_needed():
    """Test that demonstrates why we need visibility checking in StateCollector."""
    print("=== WHY WE NEED VISIBILITY CHECKING ===")

    scenarios = [
        {
            "gender": "Чоловік",
            "male_field_visible": True,
            "female_field_visible": False,
            "male_field_value": "Підполковник",
            "female_field_value": "",  # User didn't fill hidden field
            "expected_result": "Підполковник",
        },
        {
            "gender": "Жінка",
            "male_field_visible": False,
            "female_field_visible": True,
            "male_field_value": "",  # User didn't fill hidden field
            "female_field_value": "Підполковникша",
            "expected_result": "Підполковникша",
        },
        {
            "gender": "Чоловік",
            "male_field_visible": True,
            "female_field_visible": False,
            "male_field_value": "Майор",
            "female_field_value": "Майорша",  # Somehow filled (bug or old data)
            "expected_result": "Майор",  # Should take from visible field
            "current_behavior": "Майорша",  # Takes from last processed field
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"\nScenario {i}: Gender = {scenario['gender']}")
        print(
            f"  Male field: {'visible' if scenario['male_field_visible'] else 'hidden'}, value='{scenario['male_field_value']}'"
        )
        print(
            f"  Female field: {'visible' if scenario['female_field_visible'] else 'hidden'}, value='{scenario['female_field_value']}'"
        )
        print(f"  Expected result: '{scenario['expected_result']}'")
        if "current_behavior" in scenario:
            print(f"  ⚠️  Current behavior: '{scenario['current_behavior']}' (WRONG!)")
        else:
            print(f"  ✓ Current behavior: probably correct")


if __name__ == "__main__":
    test_duplicate_military_rank_field_behavior()
    print("\n" + "=" * 50)
    test_military_rank_vs_regular_person_fields()
    print("\n" + "=" * 50)
    test_state_collector_behavior_simulation()
    print("\n" + "=" * 50)
    test_field_visibility_logic_needed()
