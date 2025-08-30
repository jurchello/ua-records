from identity.preview import flatten_preview


def test_flatten_preview_new_modified_deleted_and_statuses():
    prev = {
        "new": [
            {
                "kind": "Person",
                "handle": "H-P1",
                "before": {},
                "after": {"gid": "I1", "names": [{"handle": "N1", "val": "Ivan"}]},
            },
        ],
        "modified": [
            {
                "kind": "Family",
                "handle": "H-F1",
                "before": {"gid": "F000", "spouses": [{"handle": "H-M1", "person": "H-M1"}]},
                "after": {
                    "gid": "F001",
                    "spouses": [{"handle": "H-M1", "person": "H-M1"}, {"handle": "H-W1", "person": "H-W1"}],
                },
            }
        ],
        "deleted": [
            {"kind": "Event", "handle": "H-E1", "before": {"type": "Marriage", "date": "1900-01-01"}},
        ],
    }

    rows = flatten_preview(prev)
    keys = {(r.section, r.kind, r.handle, r.path) for r in rows}
    assert ("new", "Person", "H-P1", "gid") in keys
    assert any(r.path.startswith("names[") for r in rows if r.section == "new" and r.kind == "Person")

    assert ("modified", "Family", "H-F1", "gid") in keys
    spouse_paths = [r for r in rows if r.section == "modified" and r.kind == "Family" and r.path.startswith("spouses[")]
    assert spouse_paths

    st_gid = next(r.status for r in rows if r.section == "modified" and r.kind == "Family" and r.path == "gid")
    assert st_gid == 3
