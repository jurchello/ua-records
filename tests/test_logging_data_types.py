from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generator

import pytest

from uconstants.logging import DEFAULT_CHANNELS
from ulogging import get_logger, setup_logging


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def rm(p: Path) -> None:
    try:
        p.write_text("", encoding="utf-8")
    except FileNotFoundError:
        pass


@dataclass
class SmallDC:
    a: int
    b: str


class WithRepr:
    def __init__(self, x: int) -> None:
        self.x = x

    def __repr__(self) -> str:
        return f"WithRepr(x={self.x})"


def gen_numbers() -> Generator[int, None, None]:
    for i in range(3):
        yield i


@pytest.mark.parametrize(
    "payload,expect_substrings",
    [
        (SmallDC(a=1, b="x"), ["{'a': 1, 'b': 'x'}"]),
        ({1, 3, 2}, ["'1'", "'2'", "'3'"]),
        (["a", 1, WithRepr(5)], ["'a'", "1", "WithRepr(x=5)"]),
        ((1, 2, 3), ["[1, 2, 3]"]),
        (gen_numbers(), ["[0, 1, 2]"]),
        ({"k": WithRepr(7)}, ["'k': WithRepr(x=7)"]),
        (b"bytes", ["b'bytes'"]),
        (bytearray(b"ba"), ["bytearray(b'ba')"]),
        ({"nested": {"dc": SmallDC(2, "y"), "set": {2, 1}}}, ["'nested'"]),
        ({"json_like": [1, 2, {"x": None, "y": True}]}, ["'json_like'", "'x': None", "'y': True"]),
    ],
)
def test_various_payloads_are_logged_pretty(tmp_path: Path, payload: Any, expect_substrings: list[str]) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    success_file = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(success_file)
    logger.channel("success").info(payload)
    txt = read_text(success_file)
    assert txt
    for s in expect_substrings:
        assert s.strip("'") in txt


def test_with_types_appends_type_info(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    success_file = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(success_file)
    obj = SmallDC(10, "z")
    logger.channel("success").info(obj, with_types=True)
    out = read_text(success_file)
    assert "(type=" in out
    assert re.search(r"\(type=.*SmallDC\)", out) is not None


def test_custom_object_with_repr_in_collections(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    p = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(p)
    payload = {"objs": [WithRepr(1), WithRepr(2)], "set": {WithRepr(3), WithRepr(4)}}
    logger.channel("success").info(payload)
    txt = read_text(p)
    assert "WithRepr(x=1)" in txt and "WithRepr(x=2)" in txt
    assert "WithRepr(x=3)" in txt and "WithRepr(x=4)" in txt


def test_formstate_like_structure(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    p = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(p)
    form_state = {
        "fields": {
            "person_handle": "I123",
            "place_handle": "P789",
            "confidence": "high",
            "notes": ["one", "two"],
            "attrs": [{"k": "caste", "v": "Священник"}],
        },
        "meta": {"version": 1, "valid": True},
    }
    logger.channel("success").info(form_state, with_types=False)
    txt = read_text(p)
    assert "'person_handle': 'I123'" in txt
    assert "'place_handle': 'P789'" in txt
    assert "'notes': ['one', 'two']" in txt
    assert "'version': 1" in txt
    assert "'valid': True" in txt


def test_bytes_and_bytearray_not_unrolled(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    p = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(p)
    logger.channel("success").info({"b": b"abc", "ba": bytearray(b"ab")})
    out = read_text(p)
    assert "b'abc'" in out
    assert "bytearray(b'ab')" in out


def test_generator_exhaustion_logged_as_list(tmp_path: Path) -> None:
    setup_logging(logs_dir=tmp_path, enable_console=False, channels=DEFAULT_CHANNELS)
    logger = get_logger(pretty=True)
    p = tmp_path / DEFAULT_CHANNELS["success"]["filename"]
    rm(p)

    def gen():
        for i in range(4):
            yield i

    g = gen()
    logger.channel("success").info(g)
    out = read_text(p)
    assert "[0, 1, 2, 3]" in out
