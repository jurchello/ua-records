from __future__ import annotations

import json
from typing import Any, Iterable, TypeVar, Generic, Dict, cast

from constants.cache import (
    CODEC_JSON,
    CODEC_LISTS,
    CODEC_FORMSTATE,
)

JSONScalar = str | int | float | bool | None
JSONValue = JSONScalar | list["JSONValue"] | dict[str, "JSONValue"]
FormStateLike = dict[str, JSONValue]

T_in = TypeVar("T_in", contravariant=True)
T_out = TypeVar("T_out", covariant=True)


class BaseCodec(Generic[T_in, T_out]):
    name: str
    def encode(self, obj: T_in) -> bytes:
        raise NotImplementedError
    def decode(self, data: bytes) -> T_out:
        raise NotImplementedError


class ListsCodec(BaseCodec[Iterable[str], list[str]]):
    name = CODEC_LISTS
    def encode(self, obj: Iterable[str]) -> bytes:
        it: Iterable[object] = cast(Iterable[object], obj)
        items: list[str] = [str(x) for x in it]
        return json.dumps(items, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    def decode(self, data: bytes) -> list[str]:
        v = json.loads(data.decode("utf-8"))
        if isinstance(v, list):
            v_list: list[object] = cast(list[object], v)
            return [str(x) for x in v_list]
        return []


class JSONCodec(BaseCodec[JSONValue, JSONValue]):
    name = CODEC_JSON
    def encode(self, obj: JSONValue) -> bytes:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    def decode(self, data: bytes) -> JSONValue:
        return cast(JSONValue, json.loads(data.decode("utf-8")))


class FormStateCodec(BaseCodec[FormStateLike, FormStateLike]):
    name = CODEC_FORMSTATE
    def encode(self, obj: FormStateLike) -> bytes:
        return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    def decode(self, data: bytes) -> FormStateLike:
        v = json.loads(data.decode("utf-8"))
        if isinstance(v, dict):
            return cast(FormStateLike, v)
        return {}


_registry: Dict[str, BaseCodec[Any, Any]] = {
    CODEC_LISTS: ListsCodec(),
    CODEC_JSON: JSONCodec(),
    CODEC_FORMSTATE: FormStateCodec(),
}


def get_codec(name: str) -> BaseCodec[Any, Any]:
    c = _registry.get(name)
    if c is None:
        raise ValueError(f"Unknown codec: {name!r}")
    return c


def register_codec(codec: BaseCodec[Any, Any]) -> None:
    _registry[codec.name] = codec