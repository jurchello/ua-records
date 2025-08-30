from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, TypedDict

from gi.repository import GLib


class PosRec(TypedDict):
    anchor: str  # 'topleft' | 'topright' | 'bottomleft' | 'bottomright'
    x: int
    y: int


def _dir() -> str:
    base = os.path.join(GLib.get_user_config_dir(), "UARecords")
    os.makedirs(base, exist_ok=True)
    return base


def _path() -> str:
    return os.path.join(_dir(), "positions.json")


def load_pos(form_id: str) -> Optional[PosRec]:
    try:
        with open(_path(), "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
        rec = data.get(form_id)
        if isinstance(rec, dict) and "anchor" in rec and "x" in rec and "y" in rec:
            return {"anchor": str(rec["anchor"]), "x": int(rec["x"]), "y": int(rec["y"])}
    except Exception:
        pass
    return None


def save_pos(form_id: str, anchor: str, x_off: int, y_off: int) -> None:
    p = Path(_path())
    data: Dict[str, Any] = {}

    try:
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
    except FileNotFoundError:
        data = {}
    except json.JSONDecodeError:
        data = {}

    data[form_id] = {"anchor": anchor, "x": int(x_off), "y": int(y_off)}

    tmp = p.with_suffix(p.suffix + ".tmp")
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, p)
    except OSError:
        try:
            if tmp.exists():
                tmp.unlink()
        except OSError:
            pass
