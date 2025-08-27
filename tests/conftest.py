from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, Optional, Literal
from types import TracebackType

import pytest
from gramps.gen.lib import Person, Event, Family, Tag, Citation, Place

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
        self.people: Dict[Handle, Person] = {}
        self.events: Dict[Handle, Event] = {}
        self.families: Dict[Handle, Family] = {}
        self.tags: Dict[Handle, Tag] = {}
        self.citations: Dict[Handle, Citation] = {}
        self.places: Dict[Handle, Place] = {}
        self._backlinks: Dict[tuple[Handle, str], Iterable[tuple[str, object]]] = {}

    def _h(self) -> Handle: self._i += 1; return f"H{self._i}"

    # Person
    def add_person(self, p: Person, _t: Any) -> Handle: h=self._h(); self.people[h]=p; return h
    def commit_person(self, _p: Person, _t: Any) -> None: ...
    def get_person_from_handle(self, h: Handle) -> Optional[Person]: return self.people.get(h)
    def iter_people(self) -> Iterator[Person]: return iter(self.people.values())

    # Event
    def add_event(self, e: Event, _t: Any) -> Handle: h=self._h(); self.events[h]=e; return h
    def commit_event(self, _e: Event, _t: Any) -> None: ...
    def get_event_from_handle(self, h: Handle) -> Optional[Event]: return self.events.get(h)
    def iter_events(self) -> Iterator[Event]: return iter(self.events.values())

    # Family
    def add_family(self, f: Family, _t: Any) -> Handle: h=self._h(); self.families[h]=f; return h
    def commit_family(self, _f: Family, _t: Any) -> None: ...
    def get_family_from_handle(self, h: Handle) -> Optional[Family]: return self.families.get(h)

    # Tag
    def add_tag(self, t: Tag, _t: Any) -> Handle: h=self._h(); self.tags[h]=t; return h
    def commit_tag(self, _t: Tag, _tr: Any) -> None: ...
    def get_tag_from_handle(self, h: Handle) -> Optional[Tag]: return self.tags.get(h)
    def get_tag_handles(self) -> Iterable[Handle]: return list(self.tags.keys())
    def get_number_of_tags(self) -> int: return len(self.tags)

    # Citation
    def add_citation(self, c: Citation, _t: Any) -> Handle: h=self._h(); self.citations[h]=c; return h
    def commit_citation(self, _c: Citation, _t: Any) -> None: ...
    def get_citation_from_handle(self, h: Handle) -> Optional[Citation]: return self.citations.get(h)

    # Place
    def add_place(self, p: Place, _t: Any) -> Handle: h=self._h(); self.places[h]=p; return h
    def commit_place(self, _p: Place, _t: Any) -> None: ...
    def get_place_from_handle(self, h: Handle) -> Optional[Place]: return self.places.get(h)

    # Backlinks
    def find_backlink_handles(self, h: Handle, cls: Optional[str]=None) -> Iterable[tuple[str, object]]:
        return self._backlinks.get((h, cls or ""), [])
    def set_backlinks(self, h: Handle, cls: str, links: Iterable[tuple[str, object]]) -> None:
        self._backlinks[(h, cls)] = list(links)


# ---------- Fixtures ----------
@pytest.fixture()
def db() -> Any:
    return TinyDb()

@pytest.fixture(autouse=True)
def patch_dbtxn(monkeypatch: pytest.MonkeyPatch) -> None:
    import repositories.person_repository as m1
    import repositories.event_repository as m2
    import repositories.family_repository as m3
    import repositories.tag_repository as m4
    import repositories.citation_repository as m5
    import repositories.place_repository as m6
    for mod in (m1, m2, m3, m4, m5, m6):
        monkeypatch.setattr(mod, "DbTxn", NoopDbTxn, raising=True)

__all__ = ["TinyDb"]