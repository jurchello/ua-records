"""
HV-only тестовий набір для UARecords (без селекторів S).
Запускається одним файлом: test_identity.py
"""

# ---- Імпорти з вашого пакета ----
from staging.ops import build_change_ops
from staging.apply import apply_ops
from staging.validate import validate_hv_graph
from services.commit_planner import plan_commit
from services import orchestrator as orch_mod
from identity.identity_map import IdentityMap
from identity.gramps_adapter import GrampsAdapter


# ======================================================================
#                   Мінімальні dummy-домени для тестів
# ======================================================================

class DummyBase:
    def __init__(self, handle: str):
        self.handle = handle
    def get_handle(self): return self.handle


class DummyPerson(DummyBase):
    def __init__(self, handle: str = ""):
        super().__init__(handle)
        self._gender = ""
        self._gid = ""
    def set_gender(self, g): self._gender = g
    def get_gender(self): return self._gender
    def set_gramps_id(self, gid): self._gid = gid
    def get_gramps_id(self): return self._gid


class DummyEventRef:
    def __init__(self, h, role=""): self._h, self._r = h, role
    def get_reference_handle(self): return self._h
    def get_role(self): return self._r


class DummyFamily(DummyBase):
    def __init__(self, handle: str, father: str = "", mother: str = ""):
        super().__init__(handle)
        self._father, self._mother = father, mother
        self._gid = ""
        self._event_refs = []
    # --- getters used by serializers ---
    def get_father_handle(self): return self._father or None
    def get_mother_handle(self): return self._mother or None
    def get_gramps_id(self): return self._gid
    def get_event_ref_list(self): return list(self._event_refs)
    # --- mutators used by patchers ---
    def set_father_handle(self, h): self._father = h
    def set_mother_handle(self, h): self._mother = h
    def add_event_ref(self, evh, role=""): self._event_refs.append(DummyEventRef(evh, role))


class FakeAdapter:
    """Проста заглушка, яку ми обгорнемо GrampsAdapter-ом."""
    def __init__(self):
        self._seq = 0
        self.add_calls = []
        self.commit_calls = []
        self.remove_calls = []
    def _new_handle(self, prefix):
        self._seq += 1
        return f"H-{prefix}-{self._seq:04d}"
    def add(self, kind, obj):
        h = self._new_handle(kind.upper())
        obj.handle = h
        self.add_calls.append((kind, h))
        return h
    def commit(self, kind, obj):
        self.commit_calls.append((kind, getattr(obj, "handle", None)))
    def remove(self, kind, handle):
        self.remove_calls.append((kind, handle))


# ======================================================================
#                Локальні мінімальні серіалізатори для прев’ю
# ======================================================================

def serialize_family_for_preview(fam: DummyFamily):
    """Канонічний JSON: важливо мати ключі 'handle' у списках для стабільного diff."""
    return {
        "gid": fam.get_gramps_id() or "",
        "spouses": (
            [{"handle": fam.get_father_handle(), "person": fam.get_father_handle()}]
            + ([{"handle": fam.get_mother_handle(), "person": fam.get_mother_handle()}]
               if fam.get_mother_handle() else [])
        ),
        "event_refs": [
            {"event": r.get_reference_handle(), "role": r.get_role()}
            for r in fam.get_event_ref_list()
        ],
    }


def serialize_person_for_preview(p: DummyPerson):
    return {"gid": p.get_gramps_id() or "", "gender": p.get_gender() or ""}


# ======================================================================
#                               ТЕСТИ
# ======================================================================

def test_ops_and_apply_create_update():
    """
    Перевіряємо, що build_change_ops знаходить create(VH) та modified(H),
    і apply_ops правильно збирає accepted_after з VH-посиланнями.
    """
    baseline = {
        ("Family", "H-F2-0001"): {
            "gid": "",
            "spouses": [{"handle": "H-MAN-0001", "person": "H-MAN-0001"}],
            "event_refs": [],
        }
    }

    after = {
        ("Person", "VH:wife1"): {"gid": "", "gender": "F"},
        ("Event", "VH:mar1"): {"type": "Marriage"},
        ("Family", "H-F2-0001"): {
            "gid": "",
            "spouses": [
                {"handle": "H-MAN-0001", "person": "H-MAN-0001"},
                {"handle": "VH:wife1", "person": "VH:wife1"},
            ],
            "event_refs": [{"event": "VH:mar1", "role": ""}],
        },
    }

    ops = build_change_ops(baseline, after)

    assert any(o.op_type == "create_object" and o.ref.oid == "VH:wife1" for o in ops)
    assert any(o.op_type == "create_object" and o.ref.oid == "VH:mar1" for o in ops)
    assert any(o.section == "modified" and o.ref.oid == "H-F2-0001" for o in ops)

    accepted = [o.id for o in ops]  # приймаємо все
    acc = apply_ops(baseline, ops, accepted)

    assert ("Person", "VH:wife1") in acc
    assert ("Event", "VH:mar1") in acc
    fam = acc[("Family", "H-F2-0001")]
    assert {"handle": "VH:wife1", "person": "VH:wife1"} in fam["spouses"]
    # event_refs має структуру [{'handle': '0', 'value': "{'event': 'VH:mar1', 'role': ''}"}]
    assert len(fam["event_refs"]) > 0
    event_ref_value = fam["event_refs"][0]["value"]
    assert "VH:mar1" in event_ref_value


def test_validate_detects_missing_vh_target():
    """
    Валідація має впіймати, якщо ми відхилили create(VH), але посилання на VH лишилось.
    """
    baseline = {
        ("Family", "H-F2-0001"): {
            "spouses": [{"handle": "H-MAN-0001", "person": "H-MAN-0001"}],
            "event_refs": [],
        }
    }
    after = {
        ("Family", "H-F2-0001"): {
            "spouses": [
                {"handle": "H-MAN-0001", "person": "H-MAN-0001"},
                {"handle": "VH:wife1", "person": "VH:wife1"},
            ],
            "event_refs": [],
        }
    }

    ops = build_change_ops(baseline, after)

    # Імітуємо відхилення створення Person(VH:wife1)
    accepted = [o.id for o in ops if not (o.op_type == "create_object" and o.ref.oid == "VH:wife1")]
    acc = apply_ops(baseline, ops, accepted)

    errs = validate_hv_graph(acc)
    assert errs, "Очікувалась помилка валідації через 'висяче' VH-посилання"
    assert any("VH:wife1" in e for e in errs)


def test_commit_planner_create_update_delete():
    """
    Планувальник має класифікувати create/update/delete між baseline і target.
    """
    baseline = {
        ("Family", "H-F2-0001"): {
            "gid": "",
            "spouses": [{"handle": "H-MAN-0001", "person": "H-MAN-0001"}],
        },
        ("Event", "H-EV-1"): {"type": "Marriage"},
    }
    target = {
        ("Family", "H-F2-0001"): {
            "gid": "",
            "spouses": [
                {"handle": "H-MAN-0001", "person": "H-MAN-0001"},
                {"handle": "VH:wife1", "person": "VH:wife1"},
            ],
        },
        ("Person", "VH:wife1"): {"gender": "F"},
        # ("Event","H-EV-1") — відсутній у target → delete
    }

    plan = plan_commit(baseline, target)

    creates = {(i.kind, i.oid) for i in plan.creates}
    updates = {(i.kind, i.oid) for i in plan.updates}
    deletes = {(i.kind, i.oid) for i in plan.deletes}

    assert ("Person", "VH:wife1") in creates
    assert ("Family", "H-F2-0001") in updates
    assert ("Event", "H-EV-1") in deletes


def test_orchestrator_create_person_and_update_family():
    """
    Інтеграційно: створюємо Person(VH), ремапимо у H, патчимо Family (mother = нова дружина).
    """
    # Підміняємо оркестраторські BUILDERS/PATCHERS, щоб працювати з нашими dummy
    def _builder_person(data):  # створення об’єкта для VH
        return DummyPerson("")

    def _patch_family(obj: DummyFamily, data: dict):
        # mother := той spouse, що не father
        father = obj.get_father_handle() or ""
        mother = ""
        for s in data.get("spouses", []):
            pid = s.get("person") or s.get("handle") or ""
            if pid and pid != father:
                mother = pid
        if mother:
            obj.set_mother_handle(mother)
        for er in data.get("event_refs", []):
            evh = er.get("event")
            if evh:
                obj.add_event_ref(evh, er.get("role", ""))
        return obj

    orch_mod.BUILDERS["Person"] = _builder_person
    orch_mod.PATCHERS["Family"] = _patch_family

    # IdentityMap + локальні серіалізатори для прев’ю/знімків
    idmap = IdentityMap()
    idmap.register_serializer("Family", serialize_family_for_preview)
    idmap.register_serializer("Person", serialize_person_for_preview)

    # Приєднуємо існуючі об’єкти (baseline)
    fam = DummyFamily("H-F2-0001", father="H-MAN-0001")
    man = DummyPerson("H-MAN-0001")
    idmap.attach("Family", fam)
    idmap.attach("Person", man)

    baseline_json = {("Family", "H-F2-0001"): serialize_family_for_preview(fam)}
    target_after = {
        ("Person", "VH:wife1"): {"gender": "F"},
        ("Family", "H-F2-0001"): {
            "gid": "",
            "spouses": [
                {"handle": "H-MAN-0001", "person": "H-MAN-0001"},
                {"handle": "VH:wife1", "person": "VH:wife1"},
            ],
            "event_refs": [],
        },
    }

    plan = plan_commit(baseline_json, target_after)

    # Готуємо адаптер: GrampsAdapter, що делегує у FakeAdapter
    fake = FakeAdapter()
    adapter = GrampsAdapter(
        add_map={
            "Person": lambda obj: fake.add("Person", obj),
            "Family": lambda obj: fake.add("Family", obj), 
            "Event": lambda obj: fake.add("Event", obj)
        },
        commit_map={
            "Person": lambda obj: fake.commit("Person", obj),
            "Family": lambda obj: fake.commit("Family", obj),
            "Event": lambda obj: fake.commit("Event", obj)
        },
    )

    vh_to_h = orch_mod.execute_plan(plan, idmap, adapter)

    # Перевіряємо, що для дружини виданий справжній H
    assert "VH:wife1" in vh_to_h
    new_h = vh_to_h["VH:wife1"]
    assert new_h.startswith("H-PERSON-")

    # Перевіряємо, що family пропатчений (mother == нова дружина)
    assert fam.get_mother_handle() == new_h


def test_identity_map_preview_modified():
    """
    Перевірка прев’ю IdentityMap: локальна зміна → modified з дельтою.
    """
    idmap = IdentityMap()
    idmap.register_serializer("Family", serialize_family_for_preview)

    fam = DummyFamily("H-F2-0001", father="H-MAN-0001")
    idmap.attach("Family", fam)

    fam.set_mother_handle("H-WIFE-0009")
    idmap.mark_dirty("Family", "H-F2-0001")

    prev = idmap.build_preview()
    assert prev["modified"], "Очікуємо modified-елемент у прев’ю"
    item = prev["modified"][0]
    assert item["kind"] == "Family"
    assert item["handle"] == "H-F2-0001"
    assert item["delta"] != {}