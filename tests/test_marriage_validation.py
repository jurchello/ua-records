from __future__ import annotations

import pytest
from forms.forms.marriage.validator import MarriageValidator
from services.work_context import WorkContext
from forms.forms.marriage.form_state import FormState


def test_marriage_validator_imports():
    """Перевірити що валідатор імпортується без помилок"""
    assert MarriageValidator is not None


def test_marriage_validator_basic():
    """Базовий тест валідації шлюбу"""
    ctx = WorkContext()
    ctx.form_state = FormState()

    validator = MarriageValidator(ctx)
    assert validator is not None

    # Валідація пустої форми має повертати помилки
    issues = validator.validate()
    assert isinstance(issues, list)


def test_validator_via_provider():
    """Тест валідатора через провайдер"""
    import sys
    
    # Clean up any mocked providers module from other tests
    if "providers" in sys.modules:
        providers_mod = sys.modules["providers"]
        # Check if it's a mocked module (has minimal attributes)
        if hasattr(providers_mod, "FORM_REGISTRY"):
            registry = getattr(providers_mod, "FORM_REGISTRY")
            # If registry has only test keys like "x", it's mocked - remove it
            if isinstance(registry, dict) and list(registry.keys()) == ["x"]:
                sys.modules.pop("providers", None)
    
    from providers import FORM_REGISTRY
    
    # Ensure we have at least one real provider
    assert len(FORM_REGISTRY) > 0, f"No providers in registry: {FORM_REGISTRY}"
    
    # Find marriage validator (should be MarriageValidator class)
    marriage_provider = None
    for prov in FORM_REGISTRY.values():
        if prov.get("validator") is MarriageValidator:
            marriage_provider = prov
            break
    
    assert marriage_provider is not None, f"No marriage provider found in: {list(FORM_REGISTRY.keys())}"
    
    validator = marriage_provider.get("validator")
    assert validator is not None
    assert validator.__name__ == "MarriageValidator"
    
    # Можемо створити екземпляр
    ctx = WorkContext()
    ctx.form_state = FormState()
    validator_instance = validator(ctx)
    assert isinstance(validator_instance, MarriageValidator)
    assert hasattr(validator_instance, 'validate')
