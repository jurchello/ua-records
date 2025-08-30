COMPONENTS_REGISTRY: dict[str, dict] = {}


def register(component: dict) -> None:
    cid = component.get("component_id")
    if not cid:
        raise ValueError("component missing component_id")
    COMPONENTS_REGISTRY[cid] = component


# Import modules after defining registry to avoid circular imports
def _load_components():
    """Load all component modules."""
    from .landowner import LANDOWNER_COMPONENT  # pylint: disable=import-outside-toplevel
    from .witness import WITNESS_COMPONENT  # pylint: disable=import-outside-toplevel
    from .clergyman import CLERGYMAN_COMPONENT  # pylint: disable=import-outside-toplevel

    register(LANDOWNER_COMPONENT)
    register(WITNESS_COMPONENT)
    register(CLERGYMAN_COMPONENT)


_load_components()
