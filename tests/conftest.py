from __future__ import annotations

import sys
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, Iterable, Iterator, Literal, Optional
import types

import pytest

# --- ensure project on sys.path ---
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class NoopDbTxn:
    def __init__(self, *_: Any, **__: Any) -> None:
        pass

    def __enter__(self) -> "NoopDbTxn":
        return self

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> Literal[False]:
        return False


# ---------- Tiny in-memory DB used by repositories in tests ----------
Handle = str


class TinyDb:
    def __init__(self) -> None:
        self._i = 0
        self.people: Dict[Handle, Any] = {}
        self.events: Dict[Handle, Any] = {}
        self.families: Dict[Handle, Any] = {}
        self.tags: Dict[Handle, Any] = {}
        self.citations: Dict[Handle, Any] = {}
        self.places: Dict[Handle, Any] = {}
        self._backlinks: Dict[tuple[Handle, str], Iterable[tuple[str, object]]] = {}

    def _h(self) -> Handle:
        self._i += 1
        return f"H{self._i}"

    # Person
    def add_person(self, p: Any, _t: Any) -> Handle:
        h = self._h()
        self.people[h] = p
        return h

    def commit_person(self, _p: Any, _t: Any) -> None: ...
    def get_person_from_handle(self, h: Handle) -> Optional[Any]:
        return self.people.get(h)

    def iter_people(self) -> Iterator[Any]:
        return iter(self.people.values())

    # Event
    def add_event(self, e: Any, _t: Any) -> Handle:
        h = self._h()
        self.events[h] = e
        return h

    def commit_event(self, _e: Any, _t: Any) -> None: ...
    def get_event_from_handle(self, h: Handle) -> Optional[Any]:
        return self.events.get(h)

    def iter_events(self) -> Iterator[Any]:
        return iter(self.events.values())

    # Family
    def add_family(self, f: Any, _t: Any) -> Handle:
        h = self._h()
        self.families[h] = f
        return h

    def commit_family(self, _f: Any, _t: Any) -> None: ...
    def get_family_from_handle(self, h: Handle) -> Optional[Any]:
        return self.families.get(h)

    # Tag
    def add_tag(self, t: Any, _t: Any) -> Handle:
        h = self._h()
        self.tags[h] = t
        return h

    def commit_tag(self, _t: Any, _tr: Any) -> None: ...
    def get_tag_from_handle(self, h: Handle) -> Optional[Any]:
        return self.tags.get(h)

    def get_tag_handles(self) -> Iterable[Handle]:
        return list(self.tags.keys())

    def get_number_of_tags(self) -> int:
        return len(self.tags)

    # Citation
    def add_citation(self, c: Any, _t: Any) -> Handle:
        h = self._h()
        self.citations[h] = c
        return h

    def commit_citation(self, _c: Any, _t: Any) -> None: ...
    def get_citation_from_handle(self, h: Handle) -> Optional[Any]:
        return self.citations.get(h)

    # Place
    def add_place(self, p: Any, _t: Any) -> Handle:
        h = self._h()
        self.places[h] = p
        return h

    def commit_place(self, _p: Any, _t: Any) -> None: ...
    def get_place_from_handle(self, h: Handle) -> Optional[Any]:
        return self.places.get(h)

    # Backlinks
    def find_backlink_handles(self, h: Handle, cls: Optional[str] = None) -> Iterable[tuple[str, object]]:
        return self._backlinks.get((h, cls or ""), [])

    def set_backlinks(self, h: Handle, cls: str, links: Iterable[tuple[str, object]]) -> None:
        self._backlinks[(h, cls)] = list(links)


# ---------- Fixtures ----------
@pytest.fixture()
def db() -> Any:
    return TinyDb()


@pytest.fixture(autouse=True)
def stub_gramps_lib():
    """Підміняємо gramps.gen.lib простими класами з потрібними методами."""
    lib = types.SimpleNamespace()

    class StubMeta(type):
        """Metaclass that returns 1 for any missing class attribute"""
        def __getattr__(cls, name):
            return 1

    class Person(metaclass=StubMeta):
        MALE = 1
        FEMALE = 2
        UNKNOWN = 0
        def __init__(self, h="person123", gid="I0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Place(metaclass=StubMeta):
        def __init__(self, h="place456", gid="P0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Citation(metaclass=StubMeta):
        CONF_VERY_HIGH = 4
        def __init__(self, h="cite789", gid="C0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Event(metaclass=StubMeta):
        def __init__(self, h="event123", gid="E0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Family(metaclass=StubMeta):
        def __init__(self, h="family123", gid="F0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Tag(metaclass=StubMeta):
        def __init__(self, h="tag123", gid="T0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class EventType(metaclass=StubMeta):
        MARRIAGE = 1
        def __init__(self, type_id=MARRIAGE):
            self.type_id = type_id

    class EventRoleType(metaclass=StubMeta):
        PRIMARY = 1
        def __init__(self, type_id=PRIMARY):
            self.type_id = type_id

    class FamilyRelType(metaclass=StubMeta):
        MARRIED = 1
        def __init__(self, type_id=MARRIED):
            self.type_id = type_id

    class AttributeType(metaclass=StubMeta):
        OCCUPATION = 1
        def __init__(self, type_id=OCCUPATION):
            self.type_id = type_id

    class Attribute(metaclass=StubMeta):
        def __init__(self, type_id=1):
            self.type_id = type_id
            self.value = ""
        def get_type(self): return self.type_id
        def set_type(self, type_id): self.type_id = type_id
        def get_value(self): return self.value
        def set_value(self, value): self.value = value

    # Additional types needed for field help and other tests
    class NoteType(metaclass=StubMeta):
        GENERAL = 1
        def __init__(self, type_id=GENERAL):
            self.type_id = type_id

    class NameType(metaclass=StubMeta):
        BIRTH = 1
        def __init__(self, type_id=BIRTH):
            self.type_id = type_id

    class PlaceType(metaclass=StubMeta):
        CITY = 1
        def __init__(self, type_id=CITY):
            self.type_id = type_id

    class SourceAttributeType(metaclass=StubMeta):
        PAGE = 1
        def __init__(self, type_id=PAGE):
            self.type_id = type_id

    class ChildRefType(metaclass=StubMeta):
        BIRTH = 1
        def __init__(self, type_id=BIRTH):
            self.type_id = type_id

    class Note(metaclass=StubMeta):
        def __init__(self, h="note123", gid="N0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Name(metaclass=StubMeta):
        def __init__(self, h="name123", gid="M0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    # Additional types for deeper Gramps imports
    class NameOriginType(metaclass=StubMeta):
        BIRTH = 1
        def __init__(self, type_id=BIRTH):
            self.type_id = type_id

    class Surname(metaclass=StubMeta):
        def __init__(self, h="surname123", gid="S0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    # GUI-related classes for field help tests
    class StyledText(metaclass=StubMeta):
        def __init__(self, text=""):
            self.text = text
        def get_text(self): return self.text

    class StyledTextTag(metaclass=StubMeta):
        def __init__(self, name="tag"):
            self.name = name

    class StyledTextTagType(metaclass=StubMeta):
        BOLD = 1
        ITALIC = 2
        def __init__(self, type_id=BOLD):
            self.type_id = type_id

    # More GUI classes that might be needed
    class MediaObject(metaclass=StubMeta):
        def __init__(self, h="media123", gid="M0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Repository(metaclass=StubMeta):
        def __init__(self, h="repo123", gid="R0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Source(metaclass=StubMeta):
        def __init__(self, h="source123", gid="S0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Address(metaclass=StubMeta):
        def __init__(self, h="addr123", gid="A0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    class Url(metaclass=StubMeta):
        def __init__(self, h="url123", gid="U0001"):
            self._h, self._gid = h, gid
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    # Create a universal stub creator that adds missing classes dynamically
    class UniversalStub(metaclass=StubMeta):
        def __init__(self, *args, **kwargs):
            self._h = "stub123"
            self._gid = "STUB001"
        def get_handle(self): return self._h
        def get_gramps_id(self): return self._gid

    lib.Person, lib.Place, lib.Citation = Person, Place, Citation
    lib.Event, lib.Family, lib.Tag = Event, Family, Tag
    lib.EventType = EventType
    lib.EventRoleType = EventRoleType
    lib.FamilyRelType = FamilyRelType
    lib.Attribute = Attribute
    lib.AttributeType = AttributeType
    lib.NoteType = NoteType
    lib.NameType = NameType
    lib.PlaceType = PlaceType
    lib.SourceAttributeType = SourceAttributeType
    lib.ChildRefType = ChildRefType
    lib.Note = Note
    lib.Name = Name
    lib.NameOriginType = NameOriginType
    lib.Surname = Surname
    lib.StyledText = StyledText
    lib.StyledTextTag = StyledTextTag
    lib.StyledTextTagType = StyledTextTagType
    lib.MediaObject = MediaObject
    lib.Repository = Repository
    lib.Source = Source
    lib.Address = Address
    lib.Url = Url
    
    # Create a module wrapper that provides fallback for missing classes
    class StubModule:
        def __init__(self, lib_namespace):
            self._lib = lib_namespace
            
        def __getattr__(self, name):
            if hasattr(self._lib, name):
                return getattr(self._lib, name)
            # Return UniversalStub for any missing class
            return UniversalStub
    
    stub_module = StubModule(lib)
    
    sys.modules.setdefault("gramps", types.ModuleType("gramps"))
    sys.modules.setdefault("gramps.gen", types.ModuleType("gramps.gen"))
    sys.modules["gramps.gen.lib"] = stub_module
    yield


def ui_ids(prefix: str, mapping: dict[str, object]) -> dict[str, object]:
    """Перетворює 'groom_box.subject_person.person' → 'groom_box_groom_box.subject_person.person'."""
    return {f"{prefix}_{k}": v for k, v in mapping.items()}


__all__ = ["TinyDb", "ui_ids"]
