from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, Set, Tuple

from .builder import deep_diff


@dataclass(frozen=True)
class Key:
    kind: str
    handle: str


class Serializer(Protocol):
    def __call__(self, obj: Any) -> Dict[str, Any]: ...


class CommitAdapter(Protocol):
    def add(self, kind: str, obj: Any) -> str: ...
    def commit(self, kind: str, obj: Any) -> None: ...


@dataclass
class Action:
    fn: Callable[..., None]
    args: List[Key]
    kwargs: Dict[str, Any]


class IdentityMap:
    """Unit-of-Work for Gramps objects (H only; VH appear as soon as created).

    - Tracks new/dirty/deleted objects.
    - Serializes objects to compute diffs and previews.
    - Commits changes via the supplied adapter.
    """

    def __init__(self) -> None:
        self._store: Dict[Key, Any] = {}
        self._new: Set[Key] = set()
        self._dirty: Set[Key] = set()
        self._deleted: Set[Key] = set()
        self._actions: List[Action] = []
        self._serializers: Dict[str, Serializer] = {}
        self._baseline: Dict[Key, Dict[str, Any]] = {}

    def register_serializer(self, kind: str, fn: Serializer) -> None:
        self._serializers[kind] = fn

    def _serialize(self, kind: str, obj: Any) -> Dict[str, Any]:
        fn = self._serializers.get(kind)
        if not fn:
            raise ValueError(f"no serializer for kind={kind}")
        return fn(obj)

    def _snapshot(self, kind: str, handle: str, obj: Any, *, empty: bool = False) -> None:
        k = Key(kind, handle)
        self._baseline[k] = {} if empty else self._serialize(kind, obj)

    def get(self, kind: str, handle: str) -> Optional[Any]:
        return self._store.get(Key(kind, handle))

    def attach(self, kind: str, obj: Any) -> str:
        handle_method = getattr(obj, "get_handle", None)
        handle = handle_method() if callable(handle_method) else getattr(obj, "handle", None)
        if not isinstance(handle, str) or not handle:
            raise ValueError("object must have handle")
        k = Key(kind, handle)
        self._store[k] = obj
        if k not in self._baseline:
            self._snapshot(kind, handle, obj)
        return handle

    def add_new(self, kind: str, obj: Any, adapter: CommitAdapter) -> str:
        handle = adapter.add(kind, obj)
        if not isinstance(handle, str) or not handle:
            raise RuntimeError(f"{kind} added but no handle")
        k = Key(kind, handle)
        self._store[k] = obj
        self._new.add(k)
        self._snapshot(kind, handle, obj, empty=True)
        return handle

    def mark_dirty(self, kind: str, handle: str) -> None:
        k = Key(kind, handle)
        if k in self._store:
            self._dirty.add(k)

    def mark_deleted(self, kind: str, handle: str) -> None:
        k = Key(kind, handle)
        if k in self._store:
            self._deleted.add(k)
            self._new.discard(k)
            self._dirty.discard(k)

    def defer(self, fn: Callable[..., None], *keys: Tuple[str, str], **kwargs: Any) -> None:
        self._actions.append(Action(fn=fn, args=[Key(k, h) for k, h in keys], kwargs=kwargs))

    def build_preview(self) -> Dict[str, List[Dict[str, Any]]]:
        new_items: List[Dict[str, Any]] = []
        modified_items: List[Dict[str, Any]] = []
        deleted_items: List[Dict[str, Any]] = []
        for k in self._new:
            obj = self._store.get(k)
            if obj is None:
                continue
            after = self._serialize(k.kind, obj)
            delta = deep_diff({}, after)
            new_items.append({"kind": k.kind, "handle": k.handle, "before": {}, "after": after, "delta": delta})
        for k in self._dirty:
            if k in self._deleted:
                continue
            obj = self._store.get(k)
            if obj is None:
                continue
            before = self._baseline.get(k, {})
            after = self._serialize(k.kind, obj)
            delta = deep_diff(before, after)
            if delta:
                modified_items.append(
                    {
                        "kind": k.kind,
                        "handle": k.handle,
                        "before": before,
                        "after": after,
                        "delta": delta,
                    }
                )
        for k in self._deleted:
            obj = self._store.get(k)
            before = self._baseline.get(k, self._serialize(k.kind, obj) if obj is not None else {})
            deleted_items.append({"kind": k.kind, "handle": k.handle, "before": before})
        return {"new": new_items, "modified": modified_items, "deleted": deleted_items}

    def commit_all(self, adapter: CommitAdapter) -> None:
        for act in self._actions:
            objs = [self._store[a] for a in act.args]
            act.fn(*objs, **act.kwargs)
        self._actions.clear()
        to_commit: Set[Key] = set(self._new) | set(self._dirty)
        for k in to_commit:
            if k in self._deleted:
                continue
            obj = self._store.get(k)
            if obj is not None:
                adapter.commit(k.kind, obj)
                self._snapshot(k.kind, k.handle, obj)
        # handle deletes, if adapter supports remove
        for k in list(self._deleted):
            remove = getattr(adapter, "remove", None)
            if callable(remove):
                remove(k.kind, k.handle)
        self._new.clear()
        self._dirty.clear()
        self._deleted.clear()
