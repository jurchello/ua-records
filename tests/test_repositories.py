from __future__ import annotations

from typing import Protocol, Iterable, cast
from gramps.gen.db.base import DbReadBase

from gramps.gen.lib import (
    Person, Family, Event, Tag, Citation, Place, AttributeType,
)

from repositories.person_repository import PersonRepository
from repositories.family_repository import FamilyRepository
from repositories.event_repository import EventRepository
from repositories.tag_repository import TagRepository
from repositories.citation_repository import CitationRepository
from repositories.place_repository import PlaceRepository
from repositories.backlink_repository import BacklinkRepository
from repositories.attribute_repository import AttributeRepository


class _HasAttrGetters(Protocol):
    def get_type(self) -> str: ...
    def get_value(self) -> object: ...

class _BacklinksDb(Protocol):
    def set_backlinks(
        self, h: str, objtype: str, links: Iterable[tuple[str, object]]
    ) -> None: ...


# ---------- PersonRepository ----------

def test_person_add_get_commit_iter(db: DbReadBase) -> None:
    repo = PersonRepository(db)
    p = Person()
    h = repo.add(p, "Add person")
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is p

    p.set_gender(Person.MALE)
    repo.commit(p, "Update person")

    got = list(repo.iter_all())
    assert p in got


# ---------- FamilyRepository ----------

def test_family_add_get_commit(db: DbReadBase) -> None:
    repo = FamilyRepository(db)
    f = Family()
    h = repo.add(f)
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is f
    repo.commit(f, "Update family")


# ---------- EventRepository ----------

def test_event_add_get_commit_iter(db: DbReadBase) -> None:
    repo = EventRepository(db)
    e = Event()
    h = repo.add(e)
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is e
    repo.commit(e, "Update event")
    assert e in list(repo.iter_all())


# ---------- TagRepository ----------

def test_tag_add_get_commit_find_and_handles(db: DbReadBase) -> None:
    repo = TagRepository(db)
    t = Tag()
    t.set_name("NEW")
    h = repo.add(t)
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is t

    # Test that we can retrieve the tag back
    retrieved_tag = repo.get_by_handle(h)
    assert retrieved_tag is not None

    repo.commit(t, "Update tag")


# ---------- CitationRepository ----------

def test_citation_add_get_commit(db: DbReadBase) -> None:
    repo = CitationRepository(db)
    c = Citation()
    h = repo.add(c)
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is c
    repo.commit(c, "Update citation")


# ---------- PlaceRepository ----------

def test_place_add_get_commit(db: DbReadBase) -> None:
    repo = PlaceRepository(db)
    p = Place()
    h = repo.add(p)
    assert isinstance(h, str)
    assert repo.get_by_handle(h) is p
    repo.commit(p, "Update place")


# ---------- BacklinkRepository ----------

def test_backlink_find_backlinks(db: DbReadBase) -> None:
    repo = BacklinkRepository(db)
    cast(_BacklinksDb, db).set_backlinks("E1", "Event", [("P1", object()), ("P2", object())])

    res = repo.find_backlinks("E1", "Event")
    assert isinstance(res, list)
    assert len(res) == 2
    assert res[0][0] == "P1"


# ---------- AttributeRepository ----------

def test_attribute_get_type(db: DbReadBase) -> None:
    from gramps.gen.lib import Attribute, AttributeType
    repo = AttributeRepository(db)
    
    attr = Attribute()
    attr.set_type(AttributeType.OCCUPATION)
    attr.set_value("Farmer")
    
    assert repo.get_type(attr) == AttributeType.OCCUPATION
    assert repo.get_value(attr) == "Farmer"