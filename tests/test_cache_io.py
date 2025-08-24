from __future__ import annotations

import time
from pathlib import Path


from cache import CacheManager, CacheStatus, CacheKey, key_for_list, key_for_formstate, path_for
from constants.cache import (
    CODEC_LISTS,
    CODEC_JSON,
    CODEC_FORMSTATE,
    NAMESPACE_LISTS,
)

DBID = "TESTDB"
SCHEMA_V = "v1"


def test_lists_roundtrip(tmp_path: Path) -> None:
    cm = CacheManager(cache_dir=tmp_path)

    key = key_for_list("man_surnames", DBID, SCHEMA_V, "all")
    data = ["Шевченко", "Іваненко", "Петренко"]

    cm.write_full(key, data, ttl_sec=3600, codec=CODEC_LISTS, schema_version=SCHEMA_V)

    p = path_for(tmp_path, key)
    assert p.exists(), "cache file must be created"
    assert p.with_name(p.stem + ".meta.json").exists(), "meta file must be created"

    status, loaded = cm.read(key)
    assert status is CacheStatus.HIT
    assert loaded == data

    info = cm.info(key)
    assert info.codec == CODEC_LISTS
    assert info.schema_version == SCHEMA_V
    assert info.ttl == 3600
    assert info.exists
    assert info.bytes_size > 0

    assert cm.delete(key) is True
    assert not p.exists()


def test_json_roundtrip(tmp_path: Path) -> None:
    cm = CacheManager(cache_dir=tmp_path)

    key = CacheKey(namespace=NAMESPACE_LISTS, type="aggregated", dbid=DBID, version=SCHEMA_V, name="people_scan")
    payload = {
        "all_given": ["Петро", "Іван"],
        "all_surnames": ["Шевченко", "Іваненко"],
        "counts": {"people": 2, "events": 5},
    }

    cm.write_full(key, payload, ttl_sec=7200, codec=CODEC_JSON, schema_version=SCHEMA_V)

    p = path_for(tmp_path, key)
    assert p.exists()
    status, loaded = cm.read(key)
    assert status is CacheStatus.HIT
    assert loaded == payload

    info = cm.info(key)
    assert info.codec == CODEC_JSON
    assert info.schema_version == SCHEMA_V
    assert info.ttl == 7200

    assert cm.delete(key) is True
    assert not p.exists()


def test_formstate_roundtrip(tmp_path: Path) -> None:
    cm = CacheManager(cache_dir=tmp_path)

    key = key_for_formstate("marriage", DBID, "person-I10376", SCHEMA_V)
    form_state = {
        "schema_version": SCHEMA_V,
        "updated_at": 1234567890.0,
        "state": {
            "groom": {
                "person": {"handle": "I10376", "gramps_id": "I10376", "display": "Петро Іваненко"},
                "given_original": "Петро",
                "surname_cur_orig": "Іваненко",
            },
            "bride": {
                "person": {"handle": "I204", "gramps_id": "I204", "display": "Марія Петренко"},
                "given_original": "Марія",
                "surname_cur_orig": "Петренко",
            },
            "common": {
                "place": {"handle": "P00323", "gramps_id": "P00323", "display": "Біловоди"},
                "date": "1899-10-12",
            },
        },
    }

    cm.write_full(key, form_state, ttl_sec=1800, codec=CODEC_FORMSTATE, schema_version=SCHEMA_V)

    p = path_for(tmp_path, key)
    assert p.exists()

    status, loaded = cm.read(key)
    assert status is CacheStatus.HIT
    assert loaded == form_state

    info = cm.info(key)
    assert info.codec == CODEC_FORMSTATE
    assert info.schema_version == SCHEMA_V
    assert info.ttl == 1800

    assert cm.delete(key) is True
    assert not p.exists()


def test_ttl_behavior(tmp_path: Path) -> None:
    cm = CacheManager(cache_dir=tmp_path)

    key = key_for_list("woman_given", DBID, SCHEMA_V, "all")
    values = ["Марія", "Олена", "Ганна"]

    cm.write_full(key, values, ttl_sec=1, codec=CODEC_LISTS, schema_version=SCHEMA_V)

    status, loaded = cm.read(key, accept_stale=False)
    assert status is CacheStatus.HIT and loaded == values

    time.sleep(1.2)

    status2, _ = cm.read(key, accept_stale=False)
    assert status2 is CacheStatus.MISS

    status3, loaded3 = cm.read(key, accept_stale=True)
    assert status3 is CacheStatus.STALE and loaded3 == values

    cm.delete(key)


def test_clear_namespace(tmp_path: Path) -> None:
    cm = CacheManager(cache_dir=tmp_path)

    k1 = key_for_list("man_castes", DBID, SCHEMA_V, "all")
    k2 = key_for_list("woman_castes", DBID, SCHEMA_V, "all")
    cm.write_full(k1, ["козаки"], ttl_sec=60, codec=CODEC_LISTS, schema_version=SCHEMA_V)
    cm.write_full(k2, ["міщани"], ttl_sec=60, codec=CODEC_LISTS, schema_version=SCHEMA_V)

    p1 = path_for(tmp_path, k1)
    p2 = path_for(tmp_path, k2)
    assert p1.exists() and p2.exists()

    removed_count = cm.clear_namespace(namespace=NAMESPACE_LISTS, dbid=DBID)
    assert removed_count >= 1

    assert not p1.exists()
    assert not p2.exists()