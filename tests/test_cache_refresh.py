from __future__ import annotations
import time
import pytest

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
        def get_dbid(self): return "test-db"
    return DB()

def test_schedule_refresh_after_save(fake_db, monkeypatch):
    import lookups.providers as lookups
    class FakeScanner:
        def __init__(self,*a,**k): pass
        def scan(self):
            return {
                "man_castes": set(),
                "woman_castes": set(),
                "all_castes": set(),
                "man_given": set(),
                "woman_given": set(),
                "all_given": set(),
                "man_surnames": {"Петренко"},
                "woman_surnames": set(),
                "all_surnames": {"Петренко"},
                "man_military_ranks": set(),
                "man_occupations": set(),
                "woman_occupations": set(),
                "all_occupations": set(),
                "all_death_causes": set(),
            }
    monkeypatch.setattr(lookups, "PeopleScanner", FakeScanner)
    lookups.set_runtime_db(fake_db)
    a = lookups.MAN_SURNAMES()
    assert a == ["Петренко"]
    lookups.schedule_refresh_after_save(delay_sec=1)
    time.sleep(1.2)
    b = lookups.MAN_SURNAMES()
    assert b == ["Петренко"]
