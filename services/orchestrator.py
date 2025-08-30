from __future__ import annotations

import copy
from typing import Any, Callable, Dict

from identity.identity_map import CommitAdapter, IdentityMap
from services.commit_planner import CommitPlan
from services.patchers.event import build_event, patch_event
from services.patchers.family import build_family, patch_family
from services.patchers.person import build_person, patch_person

BUILDERS: Dict[str, Callable[[Dict[str, Any]], Any]] = {
    "Person": build_person,
    "Event": build_event,
    "Family": build_family,
}
PATCHERS: Dict[str, Callable[[Any, Dict[str, Any]], None]] = {
    "Person": patch_person,
    "Event": patch_event,
    "Family": patch_family,
}


def _create_all(plan: CommitPlan, idmap: IdentityMap, adapter: CommitAdapter) -> Dict[str, str]:
    vh_to_h: Dict[str, str] = {}
    for it in plan.creates:
        kind = it.kind
        obj = BUILDERS[kind](it.data)
        h = idmap.add_new(kind, obj, adapter)
        if it.oid.startswith("VH:"):
            vh_to_h[it.oid] = h
    return vh_to_h


def _patch_all(plan: CommitPlan, vh_to_h: Dict[str, str], idmap: IdentityMap, _adapter: CommitAdapter) -> None:
    for it in plan.updates:
        kind, oid = it.kind, it.oid
        h = vh_to_h.get(oid, oid)
        obj = idmap.get(kind, h)
        if obj is None:
            # You may attach() objects before running orchestrator, or implement lookup here.
            raise RuntimeError(f"Object not attached: {kind}:{h}")
        data = _remap_vh_refs(it.data, vh_to_h)
        PATCHERS[kind](obj, data)
        idmap.mark_dirty(kind, h)


def _delete_all(plan: CommitPlan, _idmap: IdentityMap, adapter: CommitAdapter) -> None:
    for it in plan.deletes:
        remove = getattr(adapter, "remove", None)
        if callable(remove):
            remove(it.kind, it.oid)


def _remap_vh_refs(data: Dict[str, Any], vh_to_h: Dict[str, str]) -> Dict[str, Any]:

    def fix(x):
        if isinstance(x, dict):
            return {k: fix(v) for k, v in x.items()}
        if isinstance(x, list):
            return [fix(v) for v in x]
        if isinstance(x, str) and x.startswith("VH:"):
            return vh_to_h.get(x, x)
        return x

    return fix(copy.deepcopy(data))


def execute_plan(plan: CommitPlan, idmap: IdentityMap, adapter: CommitAdapter) -> Dict[str, str]:
    vh_to_h = _create_all(plan, idmap, adapter)
    _patch_all(plan, vh_to_h, idmap, adapter)
    _delete_all(plan, idmap, adapter)
    idmap.commit_all(adapter)
    return vh_to_h
