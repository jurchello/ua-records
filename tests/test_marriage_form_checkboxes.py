import sys
import types

import pytest

from services.form_state_base import FormStateBase


def _install_mock_environment():
    for k in list(sys.modules):
        if k in {"edit_form", "forms.forms.marriage.form_state"}:
            sys.modules.pop(k, None)

    edit_form_mod = types.ModuleType("edit_form")

    class MockEditForm:
        def __init__(self, form_id: str, **kwargs):
            self.form_id = form_id
            self._provider = MOCK_PROVIDERS.get(form_id, {})

        def make_form_state(self):
            return self._provider["form_state"]()

    setattr(edit_form_mod, "EditForm", MockEditForm)
    sys.modules["edit_form"] = edit_form_mod

    from forms.forms.marriage.form_state import FormState

    MOCK_PROVIDERS = {
        "marriage": {
            "form_state": FormState,
        }
    }


def test_marriage_form_has_allow_empty_checkboxes():
    """Test that all person entities have allow_empty checkboxes in the marriage form."""
    _install_mock_environment()
    from edit_form import EditForm

    form = EditForm("marriage")
    state = form.make_form_state()

    # Test that the form state has allow_empty fields for all person entities

    # Groom
    assert hasattr(state.typed.groom_box.subject_person, "allow_empty"), "Groom should have allow_empty checkbox"
    assert isinstance(state.typed.groom_box.subject_person.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.groom_box.subject_person.allow_empty is False, "allow_empty should default to False"

    # Groom landowner
    assert hasattr(
        state.typed.groom_box.landowner, "allow_empty"
    ), "Groom landowner should have allow_empty checkbox"
    assert isinstance(state.typed.groom_box.landowner.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.groom_box.landowner.allow_empty is False, "allow_empty should default to False"

    # Bride
    assert hasattr(state.typed.bride_box.subject_person, "allow_empty"), "Bride should have allow_empty checkbox"
    assert isinstance(state.typed.bride_box.subject_person.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.bride_box.subject_person.allow_empty is False, "allow_empty should default to False"

    # Bride landowner
    assert hasattr(
        state.typed.bride_box.landowner, "allow_empty"
    ), "Bride landowner should have allow_empty checkbox"
    assert isinstance(state.typed.bride_box.landowner.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.bride_box.landowner.allow_empty is False, "allow_empty should default to False"

    # Witnesses
    witnesses = [
        state.typed.groom_box.witness_box_1.subject_person,
        state.typed.groom_box.witness_box_1.landowner,
        state.typed.groom_box.witness_box_2.subject_person,
        state.typed.groom_box.witness_box_2.landowner,
        state.typed.bride_box.witness_box_1.subject_person,
        state.typed.bride_box.witness_box_1.landowner,
        state.typed.bride_box.witness_box_2.subject_person,
        state.typed.bride_box.witness_box_2.landowner,
    ]

    for i, witness in enumerate(witnesses):
        assert hasattr(witness, "allow_empty"), f"Witness {i+1} should have allow_empty checkbox"
        assert isinstance(witness.allow_empty, bool), f"Witness {i+1} allow_empty should be boolean"
        assert witness.allow_empty is False, f"Witness {i+1} allow_empty should default to False"

    # Clergymen
    assert hasattr(
        state.typed.clergymen_box.clergyman_1, "allow_empty"
    ), "Clergyman 1 should have allow_empty checkbox"
    assert isinstance(state.typed.clergymen_box.clergyman_1.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.clergymen_box.clergyman_1.allow_empty is False, "allow_empty should default to False"

    assert hasattr(
        state.typed.clergymen_box.clergyman_2, "allow_empty"
    ), "Clergyman 2 should have allow_empty checkbox"
    assert isinstance(state.typed.clergymen_box.clergyman_2.allow_empty, bool), "allow_empty should be boolean"
    assert state.typed.clergymen_box.clergyman_2.allow_empty is False, "allow_empty should default to False"


def test_checkbox_can_be_modified():
    """Test that allow_empty checkboxes can be set to True."""
    _install_mock_environment()
    from edit_form import EditForm

    form = EditForm("marriage")
    state = form.make_form_state()

    # Test setting checkbox to True
    state.typed.groom_box.subject_person.allow_empty = True
    assert state.typed.groom_box.subject_person.allow_empty is True, "allow_empty should be settable to True"

    # Test setting back to False
    state.typed.groom_box.subject_person.allow_empty = False
    assert state.typed.groom_box.subject_person.allow_empty is False, "allow_empty should be settable to False"


def test_checkbox_serialization():
    """Test that allow_empty checkboxes work with to_dict/update_from_dict."""
    _install_mock_environment()
    from edit_form import EditForm

    form = EditForm("marriage")
    state = form.make_form_state()

    # Set some checkboxes to True
    state.typed.groom_box.subject_person.allow_empty = True
    state.typed.bride_box.landowner.allow_empty = True
    state.typed.clergymen_box.clergyman_1.allow_empty = True

    # Test serialization
    data_dict = state.to_dict()
    assert data_dict["groom_box"]["subject_person"]["allow_empty"] is True, "allow_empty value should be preserved"
    assert data_dict["bride_box"]["landowner"]["allow_empty"] is True, "allow_empty value should be preserved"
    assert data_dict["clergymen_box"]["clergyman_1"]["allow_empty"] is True, "allow_empty value should be preserved"

    # Test deserialization
    new_state = form.make_form_state()
    new_state.update_from_dict(data_dict)

    assert new_state.typed.groom_box.subject_person.allow_empty is True, "allow_empty should be restored from dict"
    assert new_state.typed.bride_box.landowner.allow_empty is True, "allow_empty should be restored from dict"
    assert new_state.typed.clergymen_box.clergyman_1.allow_empty is True, "allow_empty should be restored from dict"


# Global variable to store MOCK_PROVIDERS
MOCK_PROVIDERS = {}
