"""Integration test for field visibility and data collection with duplicate IDs."""

from __future__ import annotations
import pytest


def create_test_form_config():
    """Create a simple fake form config to test duplicate ID behavior."""
    return {
        "id": "test_visibility_form",
        "title": "Test Visibility Form",
        "type": "Test",
        "tabs": [
            {
                "id": "test_tab",
                "title": "Test Tab",
                "frames": [
                    {
                        "title": "Gender and Military Rank Test",
                        "fields": [
                            # Gender selector
                            {
                                "id": "test_box.gender",
                                "label": "Gender",
                                "type": "entry",
                                "options": ["Чоловік", "Жінка"],
                                "default": "Чоловік",
                                "order": {"1": 1},
                            },
                            # Male military rank (visible when gender=Чоловік)
                            {
                                "id": "test_box.military_rank",
                                "label": "Military Rank (Male)",
                                "type": "entry",
                                "options": ["Капітан", "Майор", "Полковник"],
                                "show_when": {"var": "test_box.gender", "equals": "Чоловік"},
                                "order": {"1": 2},
                            },
                            # Female military rank (visible when gender=Жінка)
                            {
                                "id": "test_box.military_rank",  # Same ID!
                                "label": "Military Rank (Female)",
                                "type": "entry",
                                "options": ["Капітанша", "Майорша", "Полковникова"],
                                "show_when": {"var": "test_box.gender", "equals": "Жінка"},
                                "order": {"1": 3},
                            },
                            # Column visibility test
                            {
                                "id": "test_box.col_test",
                                "label": "Column Test",
                                "type": "entry",
                                "show_when_cols_in": [3, 4, 5],  # Only in wide layouts
                                "order": {"1": 4},
                            },
                            # Always visible field for comparison
                            {
                                "id": "test_box.always_visible",
                                "label": "Always Visible",
                                "type": "entry",
                                "order": {"1": 5},
                            },
                        ],
                    }
                ],
            }
        ],
    }


def create_test_state_class():
    """Create a simple state class for the test form."""
    from dataclasses import dataclass
    from services.form_state_base import FormStateBase

    @dataclass
    class TestBoxData:
        gender: str = ""
        military_rank: str = ""
        col_test: str = ""
        always_visible: str = ""

    @dataclass
    class TestFormData:
        test_box: TestBoxData

        def __post_init__(self):
            if not isinstance(self.test_box, TestBoxData):
                self.test_box = TestBoxData()

    class TestFormState(FormStateBase):
        def __init__(self):
            super().__init__()
            self.typed = TestFormData(test_box=TestBoxData())

    return TestFormState


class MockWidget:
    """Mock GTK widget for testing."""

    def __init__(self, value=""):
        self._value = value
        self._visible = True

    def get_text(self):
        return self._value

    def set_text(self, value):
        self._value = value

    def set_visible(self, visible):
        self._visible = visible

    def get_visible(self):
        return self._visible


class MockDataRow:
    """Mock DataRow for testing StateCollector."""

    def __init__(self, prefix="test_box"):
        self.prefix = prefix
        self.widgets = {}
        self.handles = {}
        self.objects = {}
        self.types = {}
        self._field_specs = {}

    def add_widget(self, field_id, value="", field_spec=None):
        """Add a mock widget with value."""
        widget = MockWidget(value)
        self.widgets[field_id] = widget
        if field_spec:
            self._field_specs[field_id] = field_spec
        return widget


def test_duplicate_id_integration():
    """Integration test: form config → widgets → StateCollector → FormState."""
    from services.state_collector import StateCollector

    # Create test components
    form_config = create_test_form_config()
    TestFormState = create_test_state_class()
    form_state = TestFormState()

    print("=== INTEGRATION TEST: DUPLICATE FIELD IDs ===\n")

    # Test scenario 1: Male gender selected
    print("📋 SCENARIO 1: Male gender selected")
    row1 = MockDataRow()

    # Add widgets (simulating form builder)
    row1.add_widget("gender", "Чоловік")
    male_widget = row1.add_widget("military_rank", "Полковник")  # Visible
    female_widget = row1.add_widget("military_rank", "")  # Hidden, but StateCollector doesn't know
    row1.add_widget("always_visible", "test_value")

    # Simulate what happens with current StateCollector
    print("  Widgets created:")
    print(f"    gender: 'Чоловік'")
    print(f"    military_rank (male): 'Полковник'")
    print(f"    military_rank (female): '' (hidden but processed)")
    print(f"    always_visible: 'test_value'")

    # StateCollector processes ALL widgets
    StateCollector.collect_row(row1, form_state, allow_log=False)

    final_military = form_state.get("test_box", "military_rank")
    final_gender = form_state.get("test_box", "gender")
    final_always = form_state.get("test_box", "always_visible")

    print(f"\n  📊 Results after StateCollector:")
    print(f"    gender: '{final_gender}'")
    print(f"    military_rank: '{final_military}'")
    print(f"    always_visible: '{final_always}'")

    # The problem: which military_rank value was kept?
    if final_military == "Полковник":
        print(f"    ✓ Correct: kept value from visible field")
    elif final_military == "":
        print(f"    ⚠️  Problem: kept value from hidden field (empty)")
    else:
        print(f"    ❓ Unexpected value: {final_military}")


def test_visibility_evaluation_needed():
    """Show what visibility evaluation logic we need."""
    form_config = create_test_form_config()

    print("\n=== VISIBILITY EVALUATION LOGIC NEEDED ===")

    # Find fields with visibility conditions
    all_fields = []
    for tab in form_config["tabs"]:
        for frame in tab["frames"]:
            for field in frame["fields"]:
                all_fields.append(field)

    print(f"\nForm has {len(all_fields)} fields:")

    for field in all_fields:
        field_id = field.get("id", "unknown")
        show_when = field.get("show_when")
        show_when_cols = field.get("show_when_cols_in")

        print(f"\n  {field_id}:")
        if show_when:
            var = show_when.get("var", "")
            condition = show_when.get("equals") or show_when.get("in")
            print(f"    show_when: {var} == {condition}")
        if show_when_cols:
            print(f"    show_when_cols_in: {show_when_cols}")
        if not show_when and not show_when_cols:
            print(f"    always visible")

    print(f"\n💡 StateCollector needs to evaluate these conditions!")
    print(f"   Current behavior: processes ALL widgets regardless of visibility")
    print(f"   Needed behavior: process only VISIBLE widgets")


def test_proposed_solution():
    """Test the proposed solution approach."""
    print("\n=== PROPOSED SOLUTION ===")
    print("1. Modify StateCollector.collect_row() to check field visibility")
    print("2. Before collecting widget value, evaluate:")
    print("   - show_when conditions against current state")
    print("   - show_when_cols_in against current column count")
    print("3. Only collect from visible fields")
    print("4. For duplicate IDs: last visible field wins")

    print("\nPseudo-code:")
    print(
        """
    for field_id, widget in row.widgets.items():
        field_spec = row._field_specs.get(field_id, {})
        
        # Check visibility
        if not is_field_visible(field_spec, current_state, column_count):
            continue  # Skip hidden fields
            
        value = _value_from_widget(widget)
        state.set(prefix, key, value)
    """
    )


if __name__ == "__main__":
    test_duplicate_id_integration()
    test_visibility_evaluation_needed()
    test_proposed_solution()
