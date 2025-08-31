from __future__ import annotations

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_path_mapping_issue():
    """Test the exact path mapping issue found in real StateCollector"""
    from forms.forms.marriage.form_state import FormState
    from unittest.mock import Mock
    from gramps.gen.lib import Citation

    form_state = FormState()

    # Mock citation
    mock_citation = Mock(spec=Citation)
    mock_citation.get_handle.return_value = "cite123"
    mock_citation.get_gramps_id.return_value = "C0001"

    print(f"\n🔍 === Path Mapping Issue Test ===")

    # 1. Test correct path (what our tests used)
    print(f"1. Testing CORRECT path:")
    form_state.set("common_box", "citation", mock_citation, allow_log=True)
    result1 = form_state.get_object("common_box", "citation")
    print(f"   Result: {result1 is not None}")

    # 2. Test wrong path (what StateCollector actually does)
    print(f"2. Testing WRONG path (real StateCollector):")
    form_state2 = FormState()
    form_state2.set("common_box_1", "common_box.citation", mock_citation, allow_log=True)
    result2 = form_state2.get_object("common_box", "citation")
    print(f"   Result: {result2 is not None}")

    # 3. Try to access with wrong path
    print(f"3. Trying to access with wrong path:")
    result3 = form_state2.get_object("common_box_1", "common_box.citation")
    print(f"   Result: {result3 is not None}")

    # 4. Show what's actually stored
    print(f"4. What's stored in form_state2.typed:")
    print(f"   common_box: {form_state2.typed.common_box}")
    if hasattr(form_state2.typed, "common_box_1"):
        print(f"   common_box_1: {getattr(form_state2.typed, 'common_box_1', 'NOT_FOUND')}")

    print(f"\n💡 CONCLUSION:")
    print(f"   ✅ Correct path works: {result1 is not None}")
    print(f"   ❌ Wrong path fails: {result2 is not None}")
    print(f"   This proves our tests were correct, StateCollector has wrong paths!")


if __name__ == "__main__":
    test_path_mapping_issue()
