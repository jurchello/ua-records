from __future__ import annotations

import pytest

from utils.include import expand_form

REG = {
    "x": {
        "component_id": "x",
        "version": 1,
        "frames": [
            {"title": "T", "fields": [{"id": "a", "model_path": "{mount}.a"}]},
            {"title": "T2", "fields": [{"id": "b", "model_path": "{mount}.b"}]},
        ],
    }
}


def test_expand_basic_mount_and_title_override():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "x", "mount": "root.m", "title": "X"}}]}]}}
    out = expand_form(form, REG)
    frames = out["root"]["tabs"][0]["frames"]
    assert len(frames) == 2
    assert frames[0]["title"] == "X"
    assert frames[0]["fields"][0]["model_path"] == "root.m.a"
    assert frames[1]["fields"][0]["model_path"] == "root.m.b"


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
    paths = [f["fields"][0]["model_path"] for f in frames]
    assert paths == ["m.a", "m.b", "n.a", "n.b"]


def test_expand_missing_keys_raises():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "x"}}]}]}}
    try:
        expand_form(form, REG)
        raise AssertionError("expected error")
    except ValueError as e:
        assert "need 'component' and 'mount'" in str(e)


def test_expand_missing_component_raises():
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "nope", "mount": "m"}}]}]}}
    try:
        expand_form(form, REG)
        raise AssertionError("expected error")
    except KeyError as e:
        assert "Unknown component" in str(e)


def test_expand_invalid_frames_raises():
    bad_reg = {"bad": {"component_id": "bad", "frames": "x"}}
    form = {"root": {"tabs": [{"frames": [{"$include": {"component": "bad", "mount": "m"}}]}]}}
    try:
        expand_form(form, bad_reg)
        raise AssertionError("expected error")
    except ValueError as e:
        assert "has no 'frames' list" in str(e)


COMP = {
    "clergy": {
        "component_id": "clergy",
        "frames": [
            {
                "title": "X",
                "fields": [
                    {"id": "p", "model_path": "{mount}.person", "type": "person"},
                    {"id": "n", "model_path": "{mount}.name", "type": "entry"},
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
    paths = [f["model_path"] for f in fr["fields"]]
    assert "root.c1.person" in paths
    assert "root.c1.name" in paths


def test_nested_include_expands_all():
    form = {
        "f": {
            "id": "f",
            "title": "T",
            "tabs": [{"id": "t", "title": "Tab", "frames": [{"$include": {"component": "wrap", "mount": "A.B"}}]}],
        }
    }
    out = expand_form(form, COMP)
    fr = out["f"]["tabs"][0]["frames"][0]
    paths = [f["model_path"] for f in fr["fields"]]
    assert "A.B.inner.person" in paths
    assert "A.B.inner.name" in paths


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
