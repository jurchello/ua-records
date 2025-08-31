from __future__ import annotations

import pytest

from utils.include import expand_form

REG = {
    "x": {
        "component_id": "x",
        "version": 1,
        "frames": [
            {"title": "T", "fields": [{"id": "{mount}.a"}]},
            {"title": "T2", "fields": [{"id": "{mount}.b"}]},
        ],
    }
}


def test_expand_basic_mount_and_title_override():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "x", "mount": "root.m", "title": "X"}}]}]}}
    out = expand_form(form, REG)
    frames = out["root"]["tabs"][0]["frames"]
    assert len(frames) == 2
    assert frames[0]["title"] == "X"
    assert frames[0]["fields"][0]["id"] == "root.m.a"
    assert frames[1]["fields"][0]["id"] == "root.m.b"


def test_expand_nested_lists_are_flattened():
    form = {
        "root": {
            "tabs": [
                {
                    "frames": [
                        {"$include": {"component": "x", "mount": "m"}},
                        {"$include": {"component": "x", "mount": "n"}},
                    ]
                }
            ]
        }
    }
    out = expand_form(form, REG)
    frames = out["root"]["tabs"][0]["frames"]
    paths = [f["fields"][0]["id"] for f in frames]
    assert paths == ["m.a", "m.b", "n.a", "n.b"]


def test_expand_missing_keys_raises():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "x"}}]}]}}  # немає mount
    with pytest.raises(ValueError) as e:
        expand_form(form, REG)
    assert "need 'component' and 'mount'" in str(e.value)


def test_expand_missing_component_raises():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "nope", "mount": "m"}}]}]}}
    with pytest.raises(KeyError) as e:
        expand_form(form, REG)
    assert "Unknown component" in str(e.value)


def test_expand_invalid_frames_raises():
    bad_reg = {"bad": {"component_id": "bad", "frames": "x"}}  # frames має бути list
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "bad", "mount": "m"}}]}]}}
    with pytest.raises(ValueError) as e:
        expand_form(form, bad_reg)
    assert "has no 'frames' list" in str(e.value)


COMP = {
    "clergy": {
        "component_id": "clergy",
        "frames": [
            {
                "title": "X",
                "fields": [
                    {"id": "{mount}.person", "type": "person"},
                    {"id": "{mount}.name", "type": "entry"},
                ],
            }
        ],
    },
    "wrap": {
        "component_id": "wrap",
        "frames": [{"$include": {"component": "clergy", "mount": "{mount}.inner"}}],
    },
}


def test_include_replaces_mount_and_overrides_title():
    form = {
        "f": {
            "id": "f",
            "title": "T",
            "tabs": [
                {
                    "id": "t1",
                    "title": "Tab",
                    "frames": [{"$include": {"component": "clergy", "mount": "root.c1", "title": "Over"}}],
                }
            ],
        }
    }
    out = expand_form(form, COMP)
    frames = out["f"]["tabs"][0]["frames"]
    assert len(frames) == 1
    fr = frames[0]
    assert fr["title"] == "Over"
    ids = [f["id"] for f in fr["fields"]]
    assert "root.c1.person" in ids
    assert "root.c1.name" in ids


def test_nested_include_expands_all():
    form = {
        "f": {
            "id": "f",
            "title": "T",
            "tabs": [
                {
                    "id": "t",
                    "title": "Tab",
                    "frames": [{"$include": {"component": "wrap", "mount": "A.B"}}],
                }
            ],
        }
    }
    out = expand_form(form, COMP)
    fr = out["f"]["tabs"][0]["frames"][0]
    ids = [f["id"] for f in fr["fields"]]
    assert "A.B.inner.person" in ids
    assert "A.B.inner.name" in ids


def test_include_errors_missing_keys():
    with pytest.raises(ValueError):
        expand_form(
            {
                "f": {
                    "id": "f",
                    "title": "x",
                    "tabs": [{"id": "t", "title": "T", "frames": [{"$include": {"component": "clergy"}}]}],
                }
            },
            COMP,
        )
    with pytest.raises(ValueError):
        expand_form(
            {
                "f": {
                    "id": "f",
                    "title": "x",
                    "tabs": [{"id": "t", "title": "T", "frames": [{"$include": {"mount": "x"}}]}],
                }
            },
            COMP,
        )


def test_include_error_unknown_component():
    form = {
        "f": {
            "id": "f",
            "title": "x",
            "tabs": [{"id": "t", "title": "T", "frames": [{"$include": {"component": "nope", "mount": "m"}}]}],
        }
    }
    with pytest.raises(KeyError):
        expand_form(form, COMP)


def test_include_error_bad_frames_type():
    bad = {"clergy": {"component_id": "clergy", "frames": "oops"}}
    form = {
        "f": {
            "id": "f",
            "title": "x",
            "tabs": [{"id": "t", "title": "T", "frames": [{"$include": {"component": "clergy", "mount": "m"}}]}],
        }
    }
    with pytest.raises(ValueError):
        expand_form(form, bad)
