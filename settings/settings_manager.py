from __future__ import annotations
from functools import lru_cache

import os
from typing import TYPE_CHECKING, Callable, List

from gramps.gen.config import config as configman

if TYPE_CHECKING:
    from gramps.gen.config import ConfigManager


class SettingsManager:

    def __init__(self) -> None:
        from gramps.gen.const import USER_DATA  # pylint: disable=import-outside-toplevel

        user_configs_dir = os.path.join(USER_DATA, "UARecords", "configs")
        os.makedirs(user_configs_dir, exist_ok=True)

        self.config_file: str = os.path.join(user_configs_dir, "config.ini")
        if not os.path.exists(self.config_file):
            with open(self.config_file, "w", encoding="utf-8"):
                pass

        self._change_callbacks: List[Callable[[], None]] = []

        config_name = os.path.join(user_configs_dir, "config")
        self.config: ConfigManager = configman.register_manager(config_name)

        self.config.register("form.ai_provider", "disabled")
        self.config.register("form.ai_model", "")
        self.config.register("form.ai_api_key", "")
        self.config.register("form.birth_columns", 3)
        self.config.register("form.death_columns", 3)
        self.config.register("form.marriage_columns", 3)
        self.config.register("form.density", "normal")
        self.config.register("form.tab_density", "normal")
        self.config.register("form.person_name_length", 30)
        self.config.register("form.place_title_length", 30)
        self.config.register("form.citation_text_length", 30)

        self.config.load()

    # --- AI ---
    def get_ai_provider(self) -> str:
        v = self.config.get("form.ai_provider")
        return str(v) if v else "disabled"

    def set_ai_provider(self, value: str) -> None:
        self.config.set("form.ai_provider", value)
        self.save()

    def get_ai_model(self) -> str:
        v = self.config.get("form.ai_model")
        return str(v) if v else ""

    def set_ai_model(self, value: str) -> None:
        self.config.set("form.ai_model", value)
        self.save()

    def get_ai_api_key(self) -> str:
        v = self.config.get("form.ai_api_key")
        return str(v) if v else ""

    def set_ai_api_key(self, value: str) -> None:
        self.config.set("form.ai_api_key", value)
        self.save()

    def is_ai_available(self) -> bool:
        if self.get_ai_provider() == "disabled":
            return False
        return bool(self.get_ai_provider() and self.get_ai_model() and self.get_ai_api_key())

    def get_birth_columns(self) -> int:
        return int(self.config.get("form.birth_columns"))

    def set_birth_columns(self, v: int) -> None:
        self.config.set("form.birth_columns", int(v))
        self.save()

    def get_death_columns(self) -> int:
        return int(self.config.get("form.death_columns"))

    def set_death_columns(self, v: int) -> None:
        self.config.set("form.death_columns", int(v))
        self.save()

    def get_marriage_columns(self) -> int:
        return int(self.config.get("form.marriage_columns"))

    def set_marriage_columns(self, v: int) -> None:
        self.config.set("form.marriage_columns", int(v))
        self.save()

    def get_form_density(self) -> str:
        v = self.config.get("form.density")
        return str(v) if v else "compact"

    def set_form_density(self, value: str) -> None:
        self.config.set("form.density", value)
        self.save()

    def get_tab_density(self) -> str:
        v = self.config.get("form.tab_density")
        return str(v) if v else "normal"

    def set_tab_density(self, value: str) -> None:
        self.config.set("form.tab_density", value)
        self.save()

    def get_person_name_length(self) -> int:
        return int(self.config.get("form.person_name_length"))

    def set_person_name_length(self, v: int) -> None:
        self.config.set("form.person_name_length", int(v))
        self.save()

    def get_place_title_length(self) -> int:
        return int(self.config.get("form.place_title_length"))

    def set_place_title_length(self, v: int) -> None:
        self.config.set("form.place_title_length", int(v))
        self.save()

    def get_citation_text_length(self) -> int:
        return int(self.config.get("form.citation_text_length"))

    def set_citation_text_length(self, v: int) -> None:
        self.config.set("form.citation_text_length", int(v))
        self.save()

    def add_change_callback(self, cb: Callable[[], None]) -> None:
        if cb not in self._change_callbacks:
            self._change_callbacks.append(cb)

    def remove_change_callback(self, cb: Callable[[], None]) -> None:
        if cb in self._change_callbacks:
            self._change_callbacks.remove(cb)

    def _emit_changed(self) -> None:
        for cb in list(self._change_callbacks):
            try:
                cb()
            except Exception:
                pass

    def save(self) -> None:
        self.config.save()
        self._emit_changed()


@lru_cache(maxsize=1)
def get_settings_manager() -> SettingsManager:
    return SettingsManager()
