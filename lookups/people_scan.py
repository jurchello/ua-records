from __future__ import annotations
from typing import Iterable, Iterator
from gramps.gen.lib import EventType, Person
from repositories.person_repository import PersonRepository
from repositories.event_repository import EventRepository

class PeopleScanner:
    def __init__(self, person_repo: PersonRepository, event_repo: EventRepository) -> None:
        self.people = person_repo
        self.events = event_repo

    def scan(self) -> dict[str, set[str]]:
        res = {
            "man_castes": set(),
            "woman_castes": set(),
            "all_castes": set(),
            "man_given": set(),
            "woman_given": set(),
            "all_given": set(),
            "man_surnames": set(),
            "woman_surnames": set(),
            "all_surnames": set(),
            "man_military_ranks": set(),
            "man_occupations": set(),
            "woman_occupations": set(),
            "all_occupations": set(),
            "all_death_causes": set(),
        }
        for p in self.people.iter_all():
            g = self.people.get_gender(p)
            is_male = g == Person.MALE
            is_female = g == Person.FEMALE
            for a in getattr(p, "get_attribute_list", lambda: [])() or []:
                t = str(getattr(a, "get_type", lambda: getattr(a, "type", ""))() or "").strip().casefold()
                if t in {"caste","casts"}:
                    v = (getattr(a, "get_value", lambda: getattr(a, "value", ""))() or "").strip()
                    if v:
                        res["all_castes"].add(v)
                        (res["man_castes"] if is_male else res["woman_castes"] if is_female else set()).add(v)
            names = []
            pn = self.people.get_primary_name(p)
            if pn and not pn.is_empty():
                names.append(pn)
            for n in self.people.get_alternate_names(p) or []:
                if n and not n.is_empty():
                    names.append(n)
            for n in names:
                first = (n.get_first_name() or "").strip()
                if first:
                    res["all_given"].add(first)
                    (res["man_given"] if is_male else res["woman_given"] if is_female else set()).add(first)
                for s in n.get_surname_list() or []:
                    sn = (s.get_surname() or "").strip()
                    if sn:
                        res["all_surnames"].add(sn)
                        (res["man_surnames"] if is_male else res["woman_surnames"] if is_female else set()).add(sn)
            for ref in self.people.get_event_ref_list(p) or []:
                ev = self.events.get_by_handle(ref.ref)
                if not ev:
                    continue
                et = self.events.get_type(ev)
                if et == EventType.MILITARY_SERV:
                    d = (self.events.get_description(ev) or "").strip()
                    if d and is_male:
                        res["man_military_ranks"].add(d)
                elif et == EventType.DEATH:
                    d = (self.events.get_description(ev) or "").strip()
                    if d:
                        res["all_death_causes"].add(d)
                elif et == EventType.OCCUPATION:
                    d = (self.events.get_description(ev) or "").strip()
                    if d:
                        res["all_occupations"].add(d)
                        if is_male:
                            res["man_occupations"].add(d)
                        elif is_female:
                            res["woman_occupations"].add(d)
        return res