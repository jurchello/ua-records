from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from identity.preview import _flatten  # reuse flattener for diffing
from schema_types import ObjKey


@dataclass
class ChangeOp:
    id: str
    section: str  # 'new'|'modified'|'deleted'
    ref: ObjKey
    path: str  # dotted/json path, '' for object-level ops
    before: Any
    after: Any
    op_type: str  # 'create_object'|'delete_object'|'set'|'add'|'remove'|'replace'


def _hash_id(*parts: str) -> str:
    h = hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return h


def build_change_ops(
    baseline: Dict[Tuple[str, str], Dict[str, Any]], after: Dict[Tuple[str, str], Dict[str, Any]]
) -> List[ChangeOp]:
    ops: List[ChangeOp] = []
    base_keys = set(baseline.keys())
    after_keys = set(after.keys())

    # object-level creates
    for k in sorted(after_keys - base_keys):
        kind, oid = k
        ref = ObjKey(kind, oid)
        ops.append(
            ChangeOp(
                id=_hash_id("create", kind, oid),
                section="new",
                ref=ref,
                path="",
                before=None,
                after=after[k],
                op_type="create_object",
            )
        )
        # field-level sets
        flat = _flatten(after[k])
        for p, v in flat.items():
            ops.append(
                ChangeOp(
                    id=_hash_id("new", kind, oid, p),
                    section="new",
                    ref=ref,
                    path=p,
                    before=None,
                    after=v,
                    op_type="set",
                )
            )

    # object-level deletes
    for k in sorted(base_keys - after_keys):
        kind, oid = k
        ref = ObjKey(kind, oid)
        ops.append(
            ChangeOp(
                id=_hash_id("delete", kind, oid),
                section="deleted",
                ref=ref,
                path="",
                before=baseline[k],
                after=None,
                op_type="delete_object",
            )
        )

    # modified objects: compare flattened fields
    for k in sorted(base_keys & after_keys):
        kind, oid = k
        ref = ObjKey(kind, oid)
        a = _flatten(baseline[k])
        b = _flatten(after[k])
        keys = sorted(set(a.keys()) | set(b.keys()))
        for p in keys:
            va = a.get(p, None)
            vb = b.get(p, None)
            if va == vb:
                continue
            if va is None and vb is not None:
                opt = "add"
            elif vb is None and va is not None:
                opt = "remove"
            else:
                opt = "replace"
            ops.append(
                ChangeOp(
                    id=_hash_id("mod", kind, oid, p),
                    section="modified",
                    ref=ref,
                    path=p,
                    before=va,
                    after=vb,
                    op_type=opt,
                )
            )
    return ops
