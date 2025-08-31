from __future__ import annotations
from typing import List
from configs.constants import ALL_GENDERS
from services.validator_base import ValidatorBase, ValidationIssue


class MarriageValidator(ValidatorBase):

    def _get_user_friendly_path(self, technical_path: str) -> str:
        """Convert technical field paths to user-friendly descriptions"""
        path_map = {
            "common_box.citation": "Загальне → Цитата",
            "common_box.marriage_place": "Загальне → Місце реєстрації шлюбу",
            "groom_box.subject_person": "Наречений → Основні дані",
            "bride_box.subject_person": "Наречена → Основні дані",
            "groom_box.subject_person.age": "Наречений → Вік",
            "bride_box.subject_person.age": "Наречена → Вік",
            "groom_box.subject_person.marriage_number": "Наречений → Номер шлюбу",
            "bride_box.subject_person.marriage_number": "Наречена → Номер шлюбу",
            "groom_box.landowner.gender": "Наречений → Поміщик → Стать",
            "bride_box.landowner.gender": "Наречена → Поміщик → Стать",
        }
        return path_map.get(technical_path, technical_path)

    def add(self, field: str, message: str) -> None:
        """Override to use user-friendly field paths"""
        user_friendly_field = self._get_user_friendly_path(field)
        super().add(user_friendly_field, message)

    def _required_objects(self) -> None:
        if not self.ctx.form_state.get_object("common_box", "citation"):
            self.add("common_box.citation", "Цитата обовʼязкова")
        if not self.ctx.form_state.get_object("common_box", "marriage_place"):
            self.add("common_box.marriage_place", "Місце обовʼязкове")

    def _allow_empty(self, base: str) -> bool:
        v1 = bool(self.ctx.form_state.get(base, "create_person"))
        v2 = bool(self.ctx.form_state.get(f"{base}.subject_person", "create_person"))
        return v1 or v2

    def _subject_person_dc(self, base: str):
        return self.ctx.form_state.get(base, "subject_person")

    def _landowner_dc(self, base: str):
        return self.ctx.form_state.get(base, "landowner")

    def _validate_party(self, base: str, label: str) -> None:
        sp = self._subject_person_dc(base)
        self.validate_min_identity_dc(
            sp,
            person_field="person",
            name_fields=("original_name", "normalized_name"),
            surname_fields=("original_surname", "normalized_surname"),
            allow_empty=self._allow_empty(base),
            field_path=f"{base}.subject_person",
            label=label,
        )
        self.validate_age_dc(sp, field="age", lo=0, hi=120, field_path=f"{base}.subject_person.age", label=label)
        self.validate_int_range_dc(
            sp, field="marriage_number", lo=1, hi=10, field_path=f"{base}.subject_person.marriage_number", label=label
        )

    def _validate_gender(self, bases: List[str]) -> None:
        for b in bases:
            lo = self._landowner_dc(b)
            self.validate_choice_dc(
                lo, field="gender", allowed=ALL_GENDERS, field_path=f"{b}.landowner.gender", label="Стать"
            )

    def validate(self) -> List[ValidationIssue]:
        self._required_objects()
        self._validate_party("groom_box", "Наречений")
        self._validate_party("bride_box", "Наречена")
        self._validate_gender(["groom_box", "bride_box"])
        return super().validate()
