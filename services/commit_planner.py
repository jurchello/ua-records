from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

@dataclass
class PlanItem:
    kind: str
    oid: str
    data: Dict[str, Any]

@dataclass
class CommitPlan:
    creates: List[PlanItem]
    updates: List[PlanItem]
    deletes: List[PlanItem]

def plan_commit(baseline: Dict[Tuple[str,str], Dict[str,Any]], target: Dict[Tuple[str,str], Dict[str,Any]]) -> CommitPlan:
    creates: List[PlanItem] = []
    updates: List[PlanItem] = []
    deletes: List[PlanItem] = []

    base_keys = set(baseline.keys())
    tgt_keys  = set(target.keys())

    for k in sorted(tgt_keys - base_keys):
        kind, oid = k
        creates.append(PlanItem(kind, oid, target[k]))

    for k in sorted(base_keys & tgt_keys):
        if baseline[k] != target[k]:
            kind, oid = k
            updates.append(PlanItem(kind, oid, target[k]))

    for k in sorted(base_keys - tgt_keys):
        kind, oid = k
        deletes.append(PlanItem(kind, oid, baseline[k]))

    return CommitPlan(creates=creates, updates=updates, deletes=deletes)