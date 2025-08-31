from __future__ import annotations
import pytest

gi = pytest.importorskip("gi")
gi.require_version("Gtk", "3.0") # pylint: disable=wrong-import-position
from gi.repository import Gtk  # noqa

from forms.forms.marriage.form_state import FormState
from forms.forms.marriage.validator import MarriageValidator
from services.state_collector import StateCollector
from services.work_context import WorkContext


class _FakeRow:
    """
    Мінімальний “рядок” для StateCollector:
    - widgets: field_id -> Gtk.Entry (прямо, без EventBox — StateCollector це вміє)
    - handles/objects/types: для DnD не потрібні у цьому тесті
    - prefix: як у DataRow (можемо навіть зробити “поганий” префікс, аби виявити регрес)
    - _field_specs: тільки 'id' і 'type', щоб було схоже на реальні
    """

    def __init__(self, prefix: str):
        self.prefix = prefix
        self.widgets: dict[str, Gtk.Widget] = {}
        self.handles: dict[str, str] = {}
        self.objects: dict[str, object] = {}
        self.types: dict[str, str] = {}
        self._field_specs: dict[str, dict] = {}
        self.dbstate = type("DBS", (), {"db": None})()  # не використовується тут

    def add_entry(self, full_id_in_ui: str, field_type: str, text: str):
        e = Gtk.Entry()
        e.set_text(text)
        self.widgets[full_id_in_ui] = e
        self.types[full_id_in_ui] = field_type
        self._field_specs[full_id_in_ui] = {"id": full_id_in_ui, "type": field_type}


def _identity_error_fields(issues):
    """Зручний фільтр: чи є помилка 'Наречений/Наречена → Основні дані'."""
    return {i.field for i in issues if "Основні дані" in (i.field or "")}


@pytest.mark.parametrize("use_mismatched_prefix", [False, True])
def test_statecollector_to_validator_sees_identity(monkeypatch, use_mismatched_prefix):
    """
    Інтеграційно:
    1) Симулюємо два поля-рядки (ім’я нареченого/нареченої) так, як це робить UI:
       field_id у UI = f"{prefix}_{original_id}"
       де original_id = "groom_box.subject_person.original_name" / "bride_box.subject_person.original_name"
    2) Проганяємо StateCollector.collect_row → FormState
    3) Валідатор читає з ctx.form_state і НЕ повинен скаржитись на порожню “Основні дані”.
       (Обов’язкові citation/place глушимо monkeypatch’ем, щоб не заважали суті тесту.)
    4) Варіант use_mismatched_prefix=True перевіряє, що навіть якщо префікс “з’їхав”
       (типовий регрес), наша логіка мапінгу все одно кладе значення у правильний префікс.
       Якщо колись повернеться баг з “подвійним шляхом”, цей тест впаде.
    """

    # Оригінальні ID полів з конфіга (без жодних префіксів DataRow):
    groom_name_id = "groom_box.subject_person.original_name"
    bride_name_id = "bride_box.subject_person.original_name"

    # Префікси, які DataRow підставляє на рівні UI у field_id через "_"
    # (колись тут міг бути префікс типу "groom_box_1", що й ламало збір стану)
    groom_prefix = "groom_box" if not use_mismatched_prefix else "groom_box_1"
    bride_prefix = "bride_box" if not use_mismatched_prefix else "bride_box_1"

    # Те, що реально бачить StateCollector як ключ у row.widgets:
    groom_ui_id = f"{groom_prefix}_{groom_name_id}"
    bride_ui_id = f"{bride_prefix}_{bride_name_id}"

    # Підготуємо два “рядки” як у реальному UI (мінімально необхідні)
    groom_row = _FakeRow(prefix=groom_prefix)
    groom_row.add_entry(groom_ui_id, "entry", "Іван")

    bride_row = _FakeRow(prefix=bride_prefix)
    bride_row.add_entry(bride_ui_id, "entry", "Марія")

    # Збираємо стан
    st = FormState()
    StateCollector.collect_row(groom_row, st, allow_log=False)
    StateCollector.collect_row(bride_row, st, allow_log=False)

    # Переконаймось, що значення покладені саме куди треба:
    assert st.get("groom_box", "subject_person.original_name") == "Іван"
    assert st.get("bride_box", "subject_person.original_name") == "Марія"

    # І що ніякого “подвійного” шляху не з’явилось:
    assert st.get("groom_box_1", "groom_box.subject_person.original_name") is None
    assert st.get("bride_box_1", "bride_box.subject_person.original_name") is None

    # Валідатор: заглушимо перевірки обов’язкових citation/place,
    # щоб тест фокусувався саме на видимості identity-полів:
    monkeypatch.setattr(MarriageValidator, "_required_objects", lambda self: None)

    ctx = WorkContext()
    ctx.form_state = st
    validator = MarriageValidator(ctx)

    issues = validator.validate()

    # НЕ повинно бути помилок “Наречений/Наречена → Основні дані …”
    id_err = _identity_error_fields(issues)
    assert "Наречений → Основні дані" not in id_err
    assert "Наречена → Основні дані" not in id_err
