from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_work_context_identity_map_initialization():
    """Test that WorkContext initializes with IdentityMap"""
    from services.work_context import WorkContext
    
    ctx = WorkContext()
    
    # Initially has an IdentityMap instance
    assert ctx.identity_map is not None
    assert hasattr(ctx.identity_map, 'register_serializer')
    assert hasattr(ctx.identity_map, 'attach')
    assert hasattr(ctx.identity_map, 'get')


def test_work_context_identity_map_reset():
    """Test that reset() creates fresh identity_map"""
    from services.work_context import WorkContext
    
    ctx = WorkContext()
    
    # Get reference to initial identity_map
    original_identity_map = ctx.identity_map
    assert original_identity_map is not None
    
    # Reset should create fresh instance
    ctx.reset()
    assert ctx.identity_map is not None
    assert ctx.identity_map is not original_identity_map


def test_work_context_identity_map_basic_functionality():
    """Test basic IdentityMap functionality through WorkContext"""
    from services.work_context import WorkContext
    from importlib import import_module
    
    ctx = WorkContext()
    identity_map = ctx.identity_map
    
    # Register serializer first (required for IdentityMap)
    def person_serializer(obj):
        return {"handle": obj.get_handle(), "type": "Person"}
    
    identity_map.register_serializer("Person", person_serializer)
    
    # Create mock objects using conftest stubs
    lib = import_module("gramps.gen.lib")
    person = lib.Person("test123", "I0001")
    
    # Test attach functionality
    handle = identity_map.attach("Person", person)
    assert handle == "test123"
    
    # Test get functionality
    retrieved = identity_map.get("Person", "test123")
    assert retrieved is person


def test_work_context_full_integration_with_identity():
    """Test WorkContext with all components: form_state, db, identity_map"""
    from services.work_context import WorkContext
    from forms.forms.marriage.form_state import FormState
    
    ctx = WorkContext()
    
    # Initialize all components
    ctx.form_state = FormState()
    ctx.db = "mock_db"  # Mock for this test
    identity_map = ctx.identity_map
    
    # All should be available
    assert ctx.form_state is not None
    assert ctx.db == "mock_db"
    assert ctx.identity_map is identity_map
    
    # Reset should clear form_state and db, create fresh identity_map
    ctx.reset()
    assert ctx.form_state is None
    assert ctx.db is None
    assert ctx.identity_map is not None
    assert ctx.identity_map is not identity_map  # Fresh instance


def test_identity_map_can_be_set_manually():
    """Test that identity_map can also be set manually"""
    from services.work_context import WorkContext
    from identity.identity_map import IdentityMap
    
    ctx = WorkContext()
    custom_identity_map = IdentityMap()
    
    # Set manually
    ctx.identity_map = custom_identity_map
    
    # Should be the custom one
    assert ctx.identity_map is custom_identity_map


def test_work_context_identity_map_with_serializers():
    """Test that IdentityMap can register serializers through WorkContext"""
    from services.work_context import WorkContext
    
    ctx = WorkContext()
    identity_map = ctx.identity_map
    
    # Register a simple serializer
    def person_serializer(obj):
        return {"handle": obj.get_handle(), "type": "Person"}
    
    identity_map.register_serializer("Person", person_serializer)
    
    # Create and attach a person
    from importlib import import_module
    lib = import_module("gramps.gen.lib")
    person = lib.Person("test456", "I0002")
    
    identity_map.attach("Person", person)
    
    # Test that serialization works
    preview = identity_map.build_preview()
    assert "new" in preview
    assert "modified" in preview
    assert "deleted" in preview