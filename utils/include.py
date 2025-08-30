from __future__ import annotations
from copy import deepcopy
from typing import Any, Dict, List, Optional


def _subst_placeholders(value: Any, mount: str) -> Any:
    if isinstance(value, dict):
        return {k: _subst_placeholders(v, mount) for k, v in value.items()}
    if isinstance(value, list):
        return [_subst_placeholders(v, mount) for v in value]
    if isinstance(value, str):
        return value.replace("{mount}", mount)
    return value


def _expand_fields(
    fields: List[dict],
    *,
    fragments: Dict[str, List[dict]] | None,
) -> List[dict]:
    out: List[dict] = []
    for item in fields:
        if "$fragment" in item:
            if not fragments:
                raise KeyError("Fragments registry is not provided")
            spec = item["$fragment"] or {}
            frag_id = spec.get("fragment")
            mount = spec.get("mount")
            if not frag_id or not mount:
                raise ValueError("Bad $fragment spec: need 'fragment' and 'mount'")
            if frag_id not in fragments:
                raise KeyError(f"Unknown fragment: {frag_id}")
            frag_fields = deepcopy(fragments[frag_id])
            for f in frag_fields:
                fid = f.get("id")
                if not fid:
                    continue
                f["id"] = f"{mount}.{fid}"
            frag_fields = _subst_placeholders(frag_fields, mount)
            out.extend(frag_fields)
            continue
        out.append(item)
    return out


def _expand_frames(
    frames: List[dict],
    *,
    components: Dict[str, dict],
    fragments: Dict[str, List[dict]] | None,
) -> List[dict]:
    expanded_frames: List[dict] = []

    for item in frames:
        if "$include" in item:
            spec = item["$include"] or {}
            comp_id: Optional[str] = spec.get("component")
            mount: Optional[str] = spec.get("mount")
            title_override: Optional[str] = spec.get("title")
            if not comp_id or not mount:
                raise ValueError("Bad $include spec: need 'component' and 'mount'")
            if comp_id not in components:
                raise KeyError(f"Unknown component: {comp_id}")
            comp = deepcopy(components[comp_id])
            comp = _subst_placeholders(comp, mount)
            comp_frames: List[dict] = comp.get("frames", [])
            if not isinstance(comp_frames, list):
                raise ValueError(f"Component '{comp_id}' has no 'frames' list")
            comp_frames = _expand_frames(comp_frames, components=components, fragments=fragments)
            if title_override and comp_frames:
                comp_frames[0]["title"] = title_override
            expanded_frames.extend(comp_frames)
            continue
        if "fields" in item and isinstance(item["fields"], list):
            fr_copy = dict(item)
            fr_copy["fields"] = _expand_fields(fr_copy["fields"], fragments=fragments)
            expanded_frames.append(fr_copy)
        else:
            expanded_frames.append(item)
    return expanded_frames


def expand_form(
    form: Dict[str, Any],
    components_registry: Dict[str, dict],
    fragments_registry: Dict[str, List[dict]] | None = None,
) -> Dict[str, Any]:
    result = deepcopy(form)
    for _form_key, form_def in result.items():
        tabs = form_def.get("tabs", [])
        for tab in tabs:
            frames = tab.get("frames", [])
            tab["frames"] = _expand_frames(frames, components=components_registry, fragments=fragments_registry)
    return result
