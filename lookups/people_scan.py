# pylint: disable=duplicate-code
from __future__ import annotations

from gramps.gen.lib import EventType, Person

from repositories.event_repository import EventRepository
from repositories.person_repository import PersonRepository


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

            attrs = p.get_attribute_list() if hasattr(p, "get_attribute_list") else []
            for attr in attrs or []:
                get_type = getattr(attr, "get_type", None)
                if callable(get_type):
                    t = get_type() or ""
                else:
                    t = getattr(attr, "type", "") or ""
                t = str(t).strip().casefold()

                if t in {"caste", "casts"}:
                    get_value = getattr(attr, "get_value", None)
                    if callable(get_value):
                        v = get_value() or ""
                    else:
                        v = getattr(attr, "value", "") or ""
                    v = v.strip()
                    if v:
                        res["all_castes"].add(v)
                        if is_male:
                            res["man_castes"].add(v)
                        elif is_female:
                            res["woman_castes"].add(v)

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
                    if is_male:
                        res["man_given"].add(first)
                    elif is_female:
                        res["woman_given"].add(first)
                for s in n.get_surname_list() or []:
                    sn = (s.get_surname() or "").strip()
                    if sn:
                        res["all_surnames"].add(sn)
                        if is_male:
                            res["man_surnames"].add(sn)
                        elif is_female:
                            res["woman_surnames"].add(sn)

            for ref in self.people.get_event_ref_list(p) or []:
                ev = self.events.get_by_handle(ref.ref)
                if not ev:
                    continue
                et = self.events.get_type(ev)
                d = (self.events.get_description(ev) or "").strip()
                if et == EventType.MILITARY_SERV:
                    if d and is_male:
                        res["man_military_ranks"].add(d)
                elif et == EventType.DEATH:
                    if d:
                        res["all_death_causes"].add(d)
                elif et == EventType.OCCUPATION:
                    if d:
                        res["all_occupations"].add(d)
                        if is_male:
                            res["man_occupations"].add(d)
                        elif is_female:
                            res["woman_occupations"].add(d)

        return res
