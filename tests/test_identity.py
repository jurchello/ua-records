from __future__ import annotations

from identity.builder import deep_diff
from identity.gramps_adapter import GrampsAdapter
from identity.identity_map import IdentityMap
from identity.preview import FlatRow, flatten_preview
from services import orchestrator as orch_mod
from services.commit_planner import plan_commit
from staging.apply import apply_ops
from staging.ops import build_change_ops
from staging.validate import validate_hv_graph


class DummyBase:
    def __init__(self, handle: str):
        self.handle = handle

    def get_handle(self):
        return self.handle


class DummyPerson(DummyBase):
    def __init__(self, handle: str = ""):
        super().__init__(handle)
        self._gender = ""
        self._gid = ""

    def set_gender(self, g):
        self._gender = g

    def get_gender(self):
        return self._gender

    def set_gramps_id(self, gid):
        self._gid = gid

    def get_gramps_id(self):
        return self._gid


class DummyEventRef:
    def __init__(self, h, role=""):
        self._h, self._r = h, role

    def get_reference_handle(self):
        return self._h

    def get_role(self):
        return self._r


class DummyFamily(DummyBase):
    def __init__(self, handle: str, father: str = "", mother: str = ""):
        super().__init__(handle)
        self._father, self._mother = father, mother
        self._gid = ""
        self._event_refs = []

    # --- getters used by serializers ---
    def get_father_handle(self):
        return self._father or None

    def get_mother_handle(self):
        return self._mother or None

    def get_gramps_id(self):
        return self._gid

    def get_event_ref_list(self):
        return list(self._event_refs)

    # --- mutators used by patchers ---
    def set_father_handle(self, h):
        self._father = h

    def set_mother_handle(self, h):
        self._mother = h

    def add_event_ref(self, evh, role=""):
        self._event_refs.append(DummyEventRef(evh, role))


class FakeAdapter:

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


def serialize_family_for_preview(fam: DummyFamily):
    return {
        "gid": fam.get_gramps_id() or "",
        "spouses": (
            [{"handle": fam.get_father_handle(), "person": fam.get_father_handle()}]
            + (
                [{"handle": fam.get_mother_handle(), "person": fam.get_mother_handle()}]
                if fam.get_mother_handle()
                else []
            )
        ),
        "event_refs": [{"event": r.get_reference_handle(), "role": r.get_role()} for r in fam.get_event_ref_list()],
    }


def serialize_person_for_preview(p: DummyPerson):
    return {"gid": p.get_gramps_id() or "", "gender": p.get_gender() or ""}


def test_ops_and_apply_create_update():
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

    accepted = [o.id for o in ops]
    acc = apply_ops(baseline, ops, accepted)

    assert ("Person", "VH:wife1") in acc
    assert ("Event", "VH:mar1") in acc
    fam = acc[("Family", "H-F2-0001")]
    assert {"handle": "VH:wife1", "person": "VH:wife1"} in fam["spouses"]
    assert len(fam["event_refs"]) > 0
    event_ref_value = fam["event_refs"][0]["value"]
    assert "VH:mar1" in event_ref_value


def test_validate_detects_missing_vh_target():
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

    accepted = [o.id for o in ops if not (o.op_type == "create_object" and o.ref.oid == "VH:wife1")]
    acc = apply_ops(baseline, ops, accepted)

    errs = validate_hv_graph(acc)
    assert errs, "Очікувалась помилка валідації через 'висяче' VH-посилання"
    assert any("VH:wife1" in e for e in errs)


def test_commit_planner_create_update_delete():
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
    }

    plan = plan_commit(baseline, target)

    creates = {(i.kind, i.oid) for i in plan.creates}
    updates = {(i.kind, i.oid) for i in plan.updates}
    deletes = {(i.kind, i.oid) for i in plan.deletes}

    assert ("Person", "VH:wife1") in creates
    assert ("Family", "H-F2-0001") in updates
    assert ("Event", "H-EV-1") in deletes


def test_orchestrator_allow_empty_and_update_family():

    def _builder_person(data):
        return DummyPerson("")

    def _patch_family(obj: DummyFamily, data: dict):
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
    orch_mod.PATCHERS["Family"] = _patch_family  # type: ignore

    idmap = IdentityMap()
    idmap.register_serializer("Family", serialize_family_for_preview)  # type: ignore
    idmap.register_serializer("Person", serialize_person_for_preview)  # type: ignore

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

    fake = FakeAdapter()
    adapter = GrampsAdapter(
        add_map={
            "Person": lambda obj: fake.add("Person", obj),
            "Family": lambda obj: fake.add("Family", obj),
            "Event": lambda obj: fake.add("Event", obj),
        },
        commit_map={
            "Person": lambda obj: fake.commit("Person", obj),
            "Family": lambda obj: fake.commit("Family", obj),
            "Event": lambda obj: fake.commit("Event", obj),
        },
    )

    vh_to_h = orch_mod.execute_plan(plan, idmap, adapter)

    assert "VH:wife1" in vh_to_h
    new_h = vh_to_h["VH:wife1"]
    assert new_h.startswith("H-PERSON-")

    assert fam.get_mother_handle() == new_h


def test_identity_map_preview_modified():
    idmap = IdentityMap()
    idmap.register_serializer("Family", serialize_family_for_preview)  # type: ignore

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


class Obj:
    def __init__(self, handle: str, data: dict):
        self.handle = handle
        self.data = data

    def get_handle(self):
        return self.handle


def serialize_generic(o: Obj):
    return dict(o.data)


def test_deep_diff_scalars_and_dicts():
    assert deep_diff(1, 1) == {}
    assert deep_diff("a", "a") == {}
    assert deep_diff(None, None) == {}
    assert deep_diff("a", "b") == {"from": "a", "to": "b"}
    left = {"a": 1, "b": {"c": 2}}
    right = {"a": 1, "b": {"c": 3}}
    assert deep_diff(left, right) == {"b": {"c": {"from": 2, "to": 3}}}


def test_deep_diff_flat_lists_of_scalars():
    a = ["x", "y", "z"]
    b = ["y", "z", "w"]
    d = deep_diff(a, b)
    assert d["removed"] == ["x"]
    assert d["added"] == ["w"]


def test_deep_diff_list_of_dicts_by_ids_removed_added_changed():
    a = [{"handle": "h1", "v": 1}, {"handle": "h2", "v": 2}, {"v": "loose"}]
    b = [{"handle": "h2", "v": 3}, {"handle": "h3", "v": 9}, {"v": "loose"}]
    d = deep_diff(a, b)
    assert {"handle": "h1", "v": 1} in d.get("removed", [])
    assert {"handle": "h3", "v": 9} in d.get("added", [])
    assert "changed" in d and "h2" in d["changed"] and d["changed"]["h2"]["v"] == {"from": 2, "to": 3}
    assert "loose" not in " ".join(map(str, d.get("removed", [])))
    assert "loose" not in " ".join(map(str, d.get("added", [])))


def test_flatten_preview_new_modified_deleted_rows_and_statuses():
    preview = {
        "new": [
            {
                "kind": "Person",
                "handle": "H-P-1",
                "before": {},
                "after": {"gid": "I1", "names": [{"id": "n1", "first": "Ivan"}]},
            },
        ],
        "modified": [
            {
                "kind": "Family",
                "handle": "H-F-1",
                "before": {"gid": "", "spouses": [{"handle": "H-M-1"}]},
                "after": {"gid": "", "spouses": [{"handle": "H-M-1"}, {"handle": "H-W-1"}]},
            },
        ],
        "deleted": [
            {"kind": "Event", "handle": "H-E-1", "before": {"type": "Marriage"}},
        ],
    }
    rows = flatten_preview(preview)
    assert any(
        isinstance(r, FlatRow) and r.section == "new" and r.kind == "Person" and r.handle == "H-P-1" for r in rows
    )
    assert any(
        r.section == "modified" and r.kind == "Family" and "spouses[H-W-1]" in r.path and r.status == 2 for r in rows
    )
    assert any(r.section == "deleted" and r.kind == "Event" and r.status == 1 for r in rows)


def test_identity_map_add_modify_delete_and_commit_flow():
    idm = IdentityMap()
    idm.register_serializer("Thing", serialize_generic)  # type: ignore
    a = Obj("H-A", {"x": 1})
    b = Obj("H-B", {"x": 2})
    idm.attach("Thing", a)
    idm.attach("Thing", b)
    a.data["x"] = 5
    idm.mark_dirty("Thing", "H-A")
    idm.mark_deleted("Thing", "H-B")
    calls = {"add": [], "commit": [], "remove": []}

    class Adapter:
        def add(self, kind, obj):
            calls["add"].append((kind, obj.get_handle()))
            return obj.get_handle()

        def commit(self, kind, obj):
            calls["commit"].append((kind, obj.get_handle()))

        def remove(self, kind, handle):
            calls["remove"].append((kind, handle))

    prev = idm.build_preview()
    assert prev["modified"] and any(it["handle"] == "H-A" for it in prev["modified"])
    assert prev["deleted"] and any(it["handle"] == "H-B" for it in prev["deleted"])
    idm.commit_all(Adapter())
    assert ("Thing", "H-A") in calls["commit"]
    assert ("Thing", "H-B") in calls["remove"]


def test_identity_map_defer_actions_are_executed_before_commit():
    idm = IdentityMap()
    idm.register_serializer("Thing", serialize_generic)  # type: ignore
    x = Obj("H-X", {"v": 0})
    y = Obj("H-Y", {"v": 0})
    idm.attach("Thing", x)
    idm.attach("Thing", y)

    def bump(a: Obj, b: Obj, delta: int = 1):
        a.data["v"] += delta
        b.data["v"] += delta

    idm.defer(bump, ("Thing", "H-X"), ("Thing", "H-Y"), delta=3)
    idm.mark_dirty("Thing", "H-X")
    idm.mark_dirty("Thing", "H-Y")

    class Adapter:
        def add(self, kind, obj):
            return obj.get_handle()

        def commit(self, kind, obj):
            pass

    idm.commit_all(Adapter())
    prev = idm.build_preview()
    assert not prev["modified"]
    assert x.data["v"] == 3 and y.data["v"] == 3
