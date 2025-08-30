from __future__ import annotations

from typing import Any, Dict, Optional


def _safe_import(name: str) -> Optional[dict]:
    try:
        mod = __import__(f"providers.{name}", fromlist=["PROVIDER"])
        return getattr(mod, "PROVIDER", None)
    except Exception:
        return None


def _call_or_return(val: Any) -> Any:
    return val() if callable(val) else val


def _form_obj_from(cfg: Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(cfg, dict):
        if "tabs" in cfg or ("title" in cfg and "type" in cfg):
            return cfg
        if len(cfg) == 1:
            return next(iter(cfg.values()))
    raise RuntimeError("Unrecognized form config shape")


_m = _safe_import("marriage")
_providers = [p for p in (_m,) if p]

REQUIRED_KEYS = {"id", "title", "form"}
OPTIONAL_KEYS = {"list_label"}

FORM_REGISTRY: Dict[str, dict] = {}

for prov in _providers:
    pid = prov.get("id")
    if not pid:
        raise RuntimeError(f"Provider without 'id': {prov}")

    missing = REQUIRED_KEYS - set(prov.keys())
    if missing:
        raise RuntimeError(f"Provider '{pid}' is missing keys: {sorted(missing)}")

    raw_cfg = _call_or_return(prov["form"])
    form_obj = _form_obj_from(raw_cfg)

    if "id" not in form_obj:
        form_obj["id"] = pid

    if form_obj.get("id") != pid:
        pass

    if "tabs" not in form_obj or not isinstance(form_obj["tabs"], list):
        raise RuntimeError(f"Provider '{pid}': form must contain 'tabs': list")

    if "list_label" not in prov and "list_label" in form_obj:
        prov["list_label"] = form_obj["list_label"]

    FORM_REGISTRY[pid] = prov

if not FORM_REGISTRY:
    raise RuntimeError("No providers registered")
