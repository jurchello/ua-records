from __future__ import annotations

import pytest

# These tests assume your project has ua_records.lookups.providers implemented
# as discussed. We monkeypatch PeopleScanner and the CacheManager location
# to use a temporary directory so tests are hermetic.


@pytest.fixture(autouse=True)
def patch_cache_dir(tmp_path, monkeypatch):
    import lookups.providers as lookups
    from cache import CacheManager

    lookups._cm = CacheManager(cache_dir=tmp_path)  # type: ignore[attr-defined]
    lookups.clear_options_cache()
    yield


@pytest.fixture
def fake_db():
    class DB:
        def get_dbid(self):
            return "test-db"

    return DB()


@pytest.fixture
def patch_scanner(monkeypatch):
    import lookups.providers as lookups

    class FakeScanner:
        def __init__(self, *a, **k):
            pass

        def scan(self):
            return {
                "man_castes": {"козак"},
                "woman_castes": {"міщанка"},
                "all_castes": {"козак", "міщанка"},
                "man_given": {"Іван"},
                "woman_given": {"Марія"},
                "all_given": {"Іван", "Марія"},
                "man_surnames": {"Петренко"},
                "woman_surnames": {"Іванчук"},
                "all_surnames": {"Петренко", "Іванчук"},
                "man_military_ranks": {"рядовий"},
                "man_occupations": {"коваль"},
                "woman_occupations": {"швачка"},
                "all_occupations": {"коваль", "швачка"},
                "all_death_causes": {"туберкульоз легень", "старість"},
            }

    monkeypatch.setattr(lookups, "PeopleScanner", FakeScanner)
    return FakeScanner


def test_lists_are_returned_and_sorted(fake_db, patch_scanner, monkeypatch):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    assert lookups.man_surnames() == ["Петренко"]
    assert lookups.woman_surnames() == ["Іванчук"]
    assert lookups.all_surnames() == ["Іванчук", "Петренко"]
    assert lookups.man_given() == ["Іван"]
    assert lookups.woman_given() == ["Марія"]
    assert lookups.all_given() == ["Іван", "Марія"]
    assert lookups.man_castes() == ["козак"]
    assert lookups.woman_castes() == ["міщанка"]
    assert lookups.all_castes() == ["козак", "міщанка"]
    assert lookups.man_military_ranks() == ["рядовий"]
    assert lookups.all_occupations() == ["коваль", "швачка"]
    assert lookups.man_occupations() == ["коваль"]
    assert lookups.woman_occupations() == ["швачка"]
    assert sorted(lookups.all_death_causes()) == ["старість", "туберкульоз легень"]


def test_cache_hit_and_stale_flow(fake_db, patch_scanner, tmp_path):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    first = lookups.man_surnames()
    assert first == ["Петренко"]
    # Force-refresh writes fresh values (HIT)
    lookups.force_refresh()
    second = lookups.man_surnames()
    assert second == ["Петренко"]
    # Simulate TTL expiry by rewriting meta with tiny ttl
    k = lookups._key("man_surnames", fake_db)  # type: ignore[attr-defined]
    info = lookups._cm.info(k)  # type: ignore[attr-defined]
    meta_path = info.path.with_suffix(".meta.json")
    meta = meta_path.read_text(encoding="utf-8")
    meta = meta.replace('"ttl": 86400', '"ttl": 0')
    meta_path.write_text(meta, encoding="utf-8")
    stale = lookups.man_surnames()
    assert stale == ["Петренко"]  # still served due to accept_stale=True


def test_requires_runtime_db(monkeypatch):
    import lookups.providers as lookups

    lookups.clear_options_cache()
    lookups._STATE["runtime_db"] = None  # type: ignore
    with pytest.raises(RuntimeError):
        lookups.man_surnames()


def test_reads_from_file_cache_after_memory_clear(fake_db, patch_scanner):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    _ = lookups.all_given()
    lookups.clear_options_cache()
    assert lookups.all_given() == ["Іван", "Марія"]


def test_occupations_blacklist(fake_db, monkeypatch):
    import lookups.providers as lookups

    class FakeScanner:
        def __init__(self, *a, **k):
            pass

        def scan(self):
            return {
                "all_occupations": {"Occupation of Baker", "коваль"},
                "man_occupations": {"Occupation of Baker", "коваль"},
                "woman_occupations": set(),
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
                "all_death_causes": set(),
            }

    monkeypatch.setattr(lookups, "PeopleScanner", FakeScanner)
    lookups.set_runtime_db(fake_db)
    assert lookups.all_occupations() == ["коваль"]
    assert lookups.man_occupations() == ["коваль"]


def test_force_refresh_writes_all_lists(fake_db, patch_scanner):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    lookups.force_refresh()
    assert lookups.man_castes() == ["козак"]
    assert lookups.all_surnames() == ["Іванчук", "Петренко"]


def test_scan_cached_dict_not_written_as_list(fake_db, patch_scanner):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    lookups.all_given()
    status, val = lookups._cm.read(lookups._key("_people_scan", fake_db), accept_stale=True)  # type: ignore
    assert not (status.name in ("HIT", "STALE") and isinstance(val, list))


def test_schedule_refresh_calls_force_refresh_once(fake_db, monkeypatch):
    import lookups.providers as lookups

    lookups.set_runtime_db(fake_db)
    called = {"n": 0}
    monkeypatch.setattr(lookups, "force_refresh", lambda db=None: called.__setitem__("n", called["n"] + 1))

    class DeferrableTimer:
        def __init__(self, delay, fn):
            self.fn = fn
            self.canceled = False

        def cancel(self):
            self.canceled = True

        def start(self):
            pass

        daemon = True

    monkeypatch.setattr("lookups.providers.threading.Timer", DeferrableTimer)

    lookups.schedule_refresh_after_save(delay_sec=1)
    lookups.schedule_refresh_after_save(delay_sec=1)
    t = lookups._STATE["refresh_timer"]  # type: ignore[attr-defined]
    assert t is not None
    if not t.canceled:
        t.fn()

    assert called["n"] == 1
