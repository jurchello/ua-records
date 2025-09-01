from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from gramps.gen.lib import Citation, Person, Place


class FormStateBase:
    def __init__(self) -> None:
        self.typed = None

    def _normalize_key(self, prefix: str, key: str) -> str:
        if key.startswith(prefix + "_"):
            return key[len(prefix) + 1 :]
        return key

    def _resolve_parent_and_attr(self, prefix: str, key: str) -> tuple[object, str] | None:

        if self.typed is None:
            return None
        root = getattr(self.typed, prefix, None)
        if root is None:
            return None

        if not key:
            return None

        parts = key.split(".")
        parent = root
        for seg in parts[:-1]:
            if not hasattr(parent, seg):
                return None
            parent = getattr(parent, seg)
        return parent, parts[-1]

    def _resolve_value(self, prefix: str, key: str) -> Any:
        if self.typed is None:
            raise KeyError("typed dataclass not set")
        root = getattr(self.typed, prefix, None)
        if root is None:
            raise KeyError(f"Unknown prefix: {prefix}")
        if not key:
            return root
        cur = root
        for seg in key.split("."):
            if not hasattr(cur, seg):
                raise KeyError(f"missing path segment '{seg}' for {prefix}.{key}")
            cur = getattr(cur, seg)
        return cur

    def get(self, prefix: str, key: str) -> Any:
        return self.get_nested(prefix, key)

    def set(
        self,
        prefix: str,
        key: str,
        value: str | int | dict[str, str | Person | Place | Citation] | Person | Place | Citation,
        allow_log: bool = True,
    ) -> None:
        norm_key = self._normalize_key(prefix, key)
        pair = self._resolve_parent_and_attr(prefix, norm_key)
        if pair is None:
            self._log(allow_log, f"⚠️ Unknown path: {prefix}.{norm_key}")
            return

        parent, leaf = pair
        if not hasattr(parent, leaf):
            self._log(allow_log, f"⚠️ Field not found: {prefix}.{norm_key}")
            return

        wrapped = self._wrap_object_value(value)
        wrapped = self._enrich_wrapped_value(wrapped, allow_log, prefix, norm_key)
        wrapped = self._convert_type_if_needed(wrapped, prefix, norm_key)

        current = getattr(parent, leaf)
        if isinstance(current, dict) and isinstance(wrapped, dict):
            merged = self._merge_preserving_unknown_keys(current, wrapped)
            setattr(parent, leaf, merged)
        else:
            setattr(parent, leaf, wrapped)

    def get_nested(self, prefix: str, key: str) -> Any:
        try:
            return self._resolve_value(prefix, key)
        except KeyError:
            return None

    def get_object(self, prefix: str, key: str) -> Any:
        try:
            from gramps.gen.lib import Citation, Person, Place  # pylint: disable=import-outside-toplevel
            valid_types = (Person, Place, Citation)
        except ImportError:
            # For tests or when gramps is not available
            valid_types = (object,)

        try:
            value = self._resolve_value(prefix, key)
        except KeyError:
            return None

        if isinstance(value, dict) and "object" in value:
            obj = value.get("object")
            if isinstance(obj, valid_types):
                return obj
            return None

        if isinstance(value, valid_types):
            return value
        return None

    def get_wrapped(self, prefix: str, key: str) -> dict[str, str | Person | Place | Citation] | None:
        try:
            val = self._resolve_value(prefix, key)
        except KeyError:
            return None
        return val if isinstance(val, dict) else None

    def get_handle(self, prefix: str, key: str) -> str | None:
        w = self.get_wrapped(prefix, key)
        return w.get("handle") if isinstance(w, dict) else None

    def to_dict(self) -> dict[str, object]:
        if self.typed is None:
            return {}
        return asdict(self.typed)

    def update_from_dict(self, data: dict[str, Any]) -> None:

        if self.typed is None or not isinstance(data, dict):
            return

        def _apply(obj: Any, payload: Any) -> Any:
            if is_dataclass(obj) and isinstance(payload, dict):
                for k, v in payload.items():
                    if hasattr(obj, k):
                        cur = getattr(obj, k)
                        setattr(obj, k, _apply(cur, v))
                return obj
            if isinstance(obj, dict) and isinstance(payload, dict):
                out = dict(obj)
                out.update(payload)
                return out
            return payload

        for top_key, payload in data.items():
            if hasattr(self.typed, top_key):
                cur = getattr(self.typed, top_key)
                setattr(self.typed, top_key, _apply(cur, payload))

    def _wrap_object_value(
        self, value: str | int | Person | Place | Citation | dict[str, Any]
    ) -> str | int | dict[str, Any]:
        if isinstance(value, dict) and "object" in value:
            return value

        if hasattr(value, "get_handle"):
            wrapped: dict[str, Any] = {"object": value}
            try:
                h = value.get_handle()
                if h:
                    wrapped["handle"] = h
            except Exception:
                pass
            try:
                gid = value.get_gramps_id()
                if gid:
                    wrapped["gramps_id"] = gid
            except Exception:
                pass
            return wrapped
        return value

    def _enrich_wrapped_value(
        self,
        value: str | int | dict[str, Any],
        _allow_log: bool,
        _prefix: str,
        _key: str,
    ) -> str | int | dict[str, Any]:
        if isinstance(value, dict) and "object" in value:
            obj = value["object"]
            if "handle" not in value and hasattr(obj, "get_handle"):
                try:
                    h = obj.get_handle()
                    if h:
                        value["handle"] = h
                except Exception:
                    pass
            if "gramps_id" not in value and hasattr(obj, "get_gramps_id"):
                try:
                    gid = obj.get_gramps_id()
                    if gid:
                        value["gramps_id"] = gid
                except Exception:
                    pass
        return value

    def _merge_preserving_unknown_keys(
        self,
        current: dict[str, Any],
        new: dict[str, Any],
    ) -> dict[str, Any]:
        merged = dict(current)
        merged.update(new)
        return merged

    def _get_type_conversions(self) -> dict[str, type]:
        """Override in subclass to specify which fields need type conversion"""
        return {}

    def _convert_type_if_needed(self, value: str | int | dict[str, Any], prefix: str, key: str) -> str | int | dict[str, Any] | None:
        """Convert string values to appropriate types based on field configuration"""
        if not isinstance(value, str):
            return value
        
        # Get type conversions from subclass
        conversions = self._get_type_conversions()
        field_path = f"{prefix}.{key}"
        
        if field_path in conversions:
            target_type = conversions[field_path]
            if target_type == int:
                if value.strip() == '':
                    return None
                try:
                    return int(value)
                except ValueError:
                    # Return original string if conversion fails - validator will catch this
                    return value
            elif target_type == bool:
                # Robust boolean conversion
                true_values = {'true', '1', 'on', 'yes', 't', 'y'}
                clean_value = value.lower().strip()
                return clean_value in true_values
        
        return value

    def _log(self, allow: bool, msg: str) -> None:
        if allow:
            print(msg)
