from __future__ import annotations

from typing import TYPE_CHECKING, List

from gramps.gen.plug.menu import EnumeratedListOption, StringOption, NumberOption

if TYPE_CHECKING:
    from gramps.gen.plug.menu import MenuOption
    from .settings_manager import SettingsManager


class SettingsUI:

    def __init__(self, cfg: SettingsManager) -> None:
        self.cfg = cfg
        self.opts: List[MenuOption] = []

    def build_options(self) -> List[MenuOption]:
        self.opts.clear()

        self._add_ai_provider()
        self._add_ai_model()
        self._add_ai_key()

        self._add_birth_cols()
        self._add_death_cols()
        self._add_marriage_cols()

        self._add_density()

        self._add_person_len()
        self._add_place_len()
        self._add_citation_len()

        return self.opts

    # --- helpers to add options ---
    def _add_ai_provider(self) -> None:
        o = EnumeratedListOption("Провайдер ШІ", self.cfg.get_ai_provider())
        o.add_item("disabled", "Вимкнено")
        o.add_item("openai", "OpenAI")
        o.add_item("mistral", "Mistral")
        o.add_item("gemini", "Gemini")
        o.set_help("Оберіть провайдера ШІ")
        self.opts.append(o)

    def _add_ai_model(self) -> None:
        o = StringOption("Модель ШІ", self.cfg.get_ai_model())
        o.set_help("Напр., gpt-4o-mini")
        self.opts.append(o)

    def _add_ai_key(self) -> None:
        o = StringOption("API ключ", self.cfg.get_ai_api_key())
        o.set_help("API ключ провайдера ШІ")
        self.opts.append(o)

    def _add_birth_cols(self) -> None:
        o = NumberOption("Колонки народження", self.cfg.get_birth_columns(), 1, 5)
        o.set_help("1–5"); self.opts.append(o)

    def _add_death_cols(self) -> None:
        o = NumberOption("Колонки смерті", self.cfg.get_death_columns(), 1, 5)
        o.set_help("1–5"); self.opts.append(o)

    def _add_marriage_cols(self) -> None:
        o = NumberOption("Колонки шлюбу", self.cfg.get_marriage_columns(), 1, 5)
        o.set_help("1–5"); self.opts.append(o)

    def _add_density(self) -> None:
        o = EnumeratedListOption("Щільність форм", self.cfg.get_form_density())
        o.add_item("compact", "Компактний")
        o.add_item("normal", "Нормальний")
        o.add_item("spacious", "Просторий")
        o.set_help("Відстані між елементами")
        self.opts.append(o)

    def _add_person_len(self) -> None:
        o = NumberOption("Довжина імен осіб", self.cfg.get_person_name_length(), 10, 100)
        o.set_help("10–100 символів"); self.opts.append(o)

    def _add_place_len(self) -> None:
        o = NumberOption("Довжина назв місць", self.cfg.get_place_title_length(), 10, 100)
        o.set_help("10–100 символів"); self.opts.append(o)

    def _add_citation_len(self) -> None:
        o = NumberOption("Довжина тексту цитат", self.cfg.get_citation_text_length(), 10, 100)
        o.set_help("10–100 символів"); self.opts.append(o)

    def add_multiselect_option(self, title: str, selected: list[str], choices: list[tuple[str, str]]) -> None:
        _ = (title, selected, choices)

    def add_list_option(self, title: str, items: list[str]) -> None:
        _ = (title, items)