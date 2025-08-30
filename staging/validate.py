from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _collect_vh_ids(obj: Any, acc: List[str]) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            _collect_vh_ids(v, acc)
    elif isinstance(obj, list):
        for it in obj:
            _collect_vh_ids(it, acc)
    elif isinstance(obj, str):
        if obj.startswith("VH:"):
            acc.append(obj)


def validate_hv_graph(graph: Dict[Tuple[str, str], Dict[str, Any]]) -> List[str]:
    """Ensure that all VH references point to objects present in the graph to be created."""
    errors: List[str] = []
    vh_targets = {oid for _, oid in graph.keys() if oid.startswith("VH:")}
    for (kind, oid), payload in graph.items():
        refs: List[str] = []
        _collect_vh_ids(payload, refs)
        for r in refs:
            if r not in vh_targets and (kind, r) not in graph:
                errors.append(f"{kind}:{oid} references missing {r}")
    return errors
