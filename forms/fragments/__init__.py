from __future__ import annotations
from typing import Dict, List

# fragment_id -> list[ field-dict ]
FRAGMENTS_REGISTRY: Dict[str, List[dict]] = {}


def register_fragment(fragment_id: str, fields: List[dict]) -> None:
    if not fragment_id or not isinstance(fields, list):
        raise ValueError("Bad fragment registration")
    FRAGMENTS_REGISTRY[fragment_id] = fields


# Import modules after defining registry to avoid circular imports
def _load_fragments():
    """Load all fragment modules."""
    from .man_fragment import MAN_SUBJECT_FRAGMENT  # pylint: disable=import-outside-toplevel
    from .woman_fragment import WOMAN_SUBJECT_FRAGMENT  # pylint: disable=import-outside-toplevel

    register_fragment("man_subject", MAN_SUBJECT_FRAGMENT)
    register_fragment("woman_subject", WOMAN_SUBJECT_FRAGMENT)


_load_fragments()
