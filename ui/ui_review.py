from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Optional, Callable

from staging.ops import ChangeOp
from identity.preview import _flatten

ObjKeyT = Tuple[str, str]  # (kind, oid)

@dataclass
class FieldDiff:
    path: str
    before: Any
    after: Any
    status: str  # 'added'|'removed'|'modified'|'unchanged'
    op_id: Optional[str] = None
    op_type: Optional[str] = None
    section: Optional[str] = None

@dataclass
class ObjectReview:
    key: ObjKeyT
    label: str
    status: str  # 'created'|'deleted'|'modified'|'unchanged'
    before: Dict[str, Any]
    after: Dict[str, Any]
    diffs: List[FieldDiff]
    object_create_op: Optional[ChangeOp] = None
    object_delete_op: Optional[ChangeOp] = None

def _default_label_for(key: ObjKeyT) -> str:
    kind, oid = key
    mark = " (новий)" if oid.startswith("VH:") else ""
    return f"{kind} {oid}{mark}"

def _object_status(before: Dict[str, Any], after: Dict[str, Any], diffs: List[FieldDiff]) -> str:
    if before and not after:
        return "deleted"
    if after and not before:
        return "created"
    if any(d.status in ("modified", "added", "removed") for d in diffs):
        return "modified"
    return "unchanged"

def build_object_reviews(
    baseline: Dict[ObjKeyT, Dict[str, Any]],
    after: Dict[ObjKeyT, Dict[str, Any]],
    ops: List[ChangeOp],
    *,
    show_unchanged: bool = False,
    hide_paths: Optional[Callable[[str], bool] | set[str]] = None,
    label_resolver: Optional[Callable[[ObjKeyT], str]] = None,
) -> List[ObjectReview]:
    """
    Готує дані для UI: по кожному об'єкту — дві колонки (before/after) і список diff-рядків.
    - hide_paths: callable(path)->bool або множина шляхів, що слід приховати.
    - label_resolver: callable(key)->str для людських назв без доступу до БД у цьому шарі.
    """
    # Індекси опів
    op_by_key_and_path: Dict[Tuple[ObjKeyT, str], ChangeOp] = {}
    create_op_by_key: Dict[ObjKeyT, ChangeOp] = {}
    delete_op_by_key: Dict[ObjKeyT, ChangeOp] = {}

    for op in ops:
        key: ObjKeyT = (op.ref.kind, op.ref.oid)
        if op.path == "":
            if op.op_type == "create_object":
                create_op_by_key[key] = op
            elif op.op_type == "delete_object":
                delete_op_by_key[key] = op
        else:
            op_by_key_and_path[(key, op.path)] = op

    # Усі ключі, що беруть участь у порівнянні
    all_keys = sorted(set(baseline.keys()) | set(after.keys()))

    def _hidden(path: str) -> bool:
        if hide_paths is None:
            return False
        if isinstance(hide_paths, set):
            return path in hide_paths
        return bool(hide_paths(path))  # callable

    # Для стабільного й “приємного” порядку полів
    status_order = {"modified": 0, "added": 1, "removed": 2, "unchanged": 3}

    out: List[ObjectReview] = []
    for key in all_keys:
        before = baseline.get(key) or {}
        after_ = after.get(key) or {}

        flat_before = _flatten(before)
        flat_after = _flatten(after_)

        all_paths = sorted(set(flat_before.keys()) | set(flat_after.keys()))
        diffs: List[FieldDiff] = []

        for p in all_paths:
            if _hidden(p):
                continue

            b = flat_before.get(p, None)
            a = flat_after.get(p, None)

            if a == b:
                if not show_unchanged:
                    continue
                status = "unchanged"
            elif b is None and a is not None:
                status = "added"
            elif a is None and b is not None:
                status = "removed"
            else:
                status = "modified"

            op = op_by_key_and_path.get((key, p))
            diffs.append(
                FieldDiff(
                    path=p,
                    before=b,
                    after=a,
                    status=status,
                    op_id=(op.id if op else None),
                    op_type=(op.op_type if op else None),
                    section=(op.section if op else None),
                )
            )

        # гарне сортування за статусом, а далі за шляхом
        diffs.sort(key=lambda d: (status_order.get(d.status, 9), d.path))

        label = (label_resolver or _default_label_for)(key)
        obj_status = _object_status(before, after_, diffs)

        out.append(
            ObjectReview(
                key=key,
                label=label,
                status=obj_status,
                before=before,
                after=after_,
                diffs=diffs,
                object_create_op=create_op_by_key.get(key),
                object_delete_op=delete_op_by_key.get(key),
            )
        )

    # опціонально: нові → змінені → видалені → незмінені
    obj_status_order = {"created": 0, "modified": 1, "deleted": 2, "unchanged": 3}
    out.sort(key=lambda r: (obj_status_order.get(r.status, 9), r.label))
    return out