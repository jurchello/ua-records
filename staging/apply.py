from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Tuple

from .json_path import set_at_path


def apply_ops(
    baseline: Dict[Tuple[str, str], Dict[str, Any]], ops, accepted_ids: List[str]
) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Apply a subset of ChangeOps (by id) to baseline, producing accepted_after.
    Objects are addressed by (kind, oid). Paths are dotted/[key] format.
    """
    out: Dict[Tuple[str, str], Dict[str, Any]] = {k: deepcopy(v) for k, v in baseline.items()}
    # group ops by object
    for op in ops:
        if op.id not in accepted_ids:
            continue
        k = (op.ref.kind, op.ref.oid)
        if op.op_type == "create_object":
            if k not in out:
                out[k] = {}
            continue
        if op.op_type == "delete_object":
            if k in out:
                del out[k]
            continue
        if k not in out:
            out[k] = {}
        if not op.path and isinstance(op.after, dict):
            out[k] = deepcopy(op.after)
        elif op.path:
            set_at_path(out[k], op.path, op.after)
    return out
