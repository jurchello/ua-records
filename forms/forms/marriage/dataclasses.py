from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from gramps.gen.lib import Citation, Place
    from gramps.gen.lib import Person as GrampsPerson

    class WrappedPerson(TypedDict, total=False):
        object: GrampsPerson
        handle: str
        gramps_id: str

    class WrappedPlace(TypedDict, total=False):
        object: Place
        handle: str
        gramps_id: str

    class WrappedCitation(TypedDict, total=False):
        object: Citation
        handle: str
        gramps_id: str

else:
    WrappedPerson = dict
    WrappedPlace = dict
    WrappedCitation = dict


@dataclass
class Person:
    create_person: bool = False
    person: WrappedPerson | None = None
    place: WrappedPlace | None = None
    gender: str | None = None
    caste: str | None = None
    occupation: str | None = None
    age: str | None = None
    marriages_count: str | None = None
    military_rank: str | None = None
    original_name: str | None = None
    normalized_name: str | None = None
    original_surname: str | None = None
    normalized_surname: str | None = None
    original_surname_before_marriage: str | None = None
    normalized_surname_before_marriage: str | None = None
    original_surname_after_marriage: str | None = None
    normalized_surname_after_marriage: str | None = None
    original_surname_maiden: str | None = None
    normalized_surname_maiden: str | None = None
    original_surname_married: str | None = None
    normalized_surname_married: str | None = None


@dataclass
class CommonBox:
    citation: WrappedCitation | None = None
    marriage_place: WrappedPlace | None = None
    tags_for_new_people: str | None = None
    tags_for_existing_people: str | None = None
    tags_for_new_events: str | None = None
    tags_for_citation: str | None = None


@dataclass
class WitnessBox:
    subject_person: Person = field(default_factory=Person)
    landowner: Person = field(default_factory=Person)


@dataclass
class GroomBox:
    subject_person: Person = field(default_factory=Person)
    landowner: Person = field(default_factory=Person)
    witness_box_1: WitnessBox = field(default_factory=WitnessBox)
    witness_box_2: WitnessBox = field(default_factory=WitnessBox)


BrideBox = GroomBox


@dataclass
class ClergymenBox:
    clergyman_1: Person = field(default_factory=Person)
    clergyman_2: Person = field(default_factory=Person)


@dataclass
class FormStateTyped:
    common_box: CommonBox = field(default_factory=CommonBox)
    groom_box: GroomBox = field(default_factory=GroomBox)
    bride_box: BrideBox = field(default_factory=BrideBox)
    clergymen_box: ClergymenBox = field(default_factory=ClergymenBox)
