import sys
import types
from unittest.mock import Mock, MagicMock

import pytest


def _install_mock_environment():
    """Встановлює мок-середовище для тестування інтеграції WorkContext."""
    # Очищаємо модулі
    for k in list(sys.modules):
        if k in {"base_edit_form", "services.work_context", "services.form_state_base"}:
            sys.modules.pop(k, None)

    # Мок FormStateBase
    form_state_base_mod = types.ModuleType("services.form_state_base")

    class MockFormStateBase:
        def __init__(self):
            self.typed = None
            self.test_data = {}

        def update_from_dict(self, data):
            self.test_data.update(data)

        def to_dict(self):
            return self.test_data.copy()

    setattr(form_state_base_mod, "FormStateBase", MockFormStateBase)
    sys.modules["services.form_state_base"] = form_state_base_mod

    # Мок WorkContext
    work_context_mod = types.ModuleType("services.work_context")

    class MockWorkContext:
        def __init__(self, form_state=None):
            self.form_state = form_state
            self.db = None

        def reset(self):
            self.form_state = None
            self.db = None

    setattr(work_context_mod, "WorkContext", MockWorkContext)
    setattr(work_context_mod, "MockWorkContext", MockWorkContext)  # Додаємо і як MockWorkContext
    sys.modules["services.work_context"] = work_context_mod

    # Мок BaseEditForm (спрощена версія)
    base_edit_form_mod = types.ModuleType("base_edit_form")

    class MockBaseEditForm:
        def __init__(self, *, dbstate, uistate, form_id):
            self.dbstate = dbstate
            self.uistate = uistate
            self.form_id = form_id
            self.form_state = self.make_form_state()

            # Імпортуємо WorkContext після встановлення мок-модулів
            from services.work_context import WorkContext

            self.work_context = WorkContext()

        def make_form_state(self):
            return MockFormStateBase()

        def collect_snapshot_dict(self):
            # Симулюємо збір даних з форми
            return {"person_name": "Іван", "person_surname": "Петрenko", "marriage_date": "1920-05-15"}

        def _on_save(self, _button=None):
            """Симуляція методу збереження з BaseEditForm."""
            self.work_context.reset()
            self.form_state = self.make_form_state()
            self.form_state.update_from_dict(self.collect_snapshot_dict())

            self.work_context.form_state = self.form_state
            self.work_context.db = self.dbstate.db

            # Тут би був processor.run()
            # processor = self.make_processor(self.work_context)
            # processor.run()

            self.work_context.reset()

    setattr(base_edit_form_mod, "BaseEditForm", MockBaseEditForm)
    setattr(base_edit_form_mod, "MockBaseEditForm", MockBaseEditForm)  # Додаємо і як MockBaseEditForm
    sys.modules["base_edit_form"] = base_edit_form_mod


class MockDB:
    def __init__(self):
        self.db = "mock_db_instance"


class MockDBState:
    def __init__(self):
        self.db = MockDB()


class MockUIState:
    pass


def test_work_context_receives_form_state_on_save():
    """Тест перевіряє, що WorkContext отримує оновлений FormState після натискання Зберегти."""
    _install_mock_environment()

    # Отримуємо MockBaseEditForm з модуля
    import sys

    MockBaseEditForm = sys.modules["base_edit_form"].MockBaseEditForm

    # Arrange
    dbstate = MockDBState()
    uistate = MockUIState()
    form = MockBaseEditForm(dbstate=dbstate, uistate=uistate, form_id="test_form")

    # Перевіряємо початковий стан
    assert form.work_context.form_state is None, "WorkContext повинен початково не мати form_state"
    assert form.work_context.db is None, "WorkContext повинен початково не мати db"

    # Act - симулюємо натискання кнопки Зберегти
    form._on_save()

    # Assert - після обробки form_state повинен бути скинутий
    assert form.work_context.form_state is None, "WorkContext.form_state повинен бути скинутий після обробки"


def test_work_context_provides_access_to_form_state_during_processing():
    """Тест перевіряє доступ до FormState через WorkContext під час обробки."""
    _install_mock_environment()

    # Отримуємо MockBaseEditForm з модуля
    import sys

    MockBaseEditForm = sys.modules["base_edit_form"].MockBaseEditForm

    # Arrange
    dbstate = MockDBState()
    uistate = MockUIState()
    form = MockBaseEditForm(dbstate=dbstate, uistate=uistate, form_id="test_form")

    # Модифікуємо _on_save щоб зберегти стан під час обробки
    captured_form_state = None
    original_on_save = form._on_save

    def modified_on_save(_button=None):
        nonlocal captured_form_state

        # Створюємо новий form_state
        form.form_state = form.make_form_state()
        form.form_state.update_from_dict(form.collect_snapshot_dict())

        # Заповнюємо WorkContext поточним станом форми
        form.work_context.form_state = form.form_state

        # Захоплюємо стан під час "обробки"
        captured_form_state = form.work_context.form_state

        # Скидаємо WorkContext після обробки
        form.work_context.reset()

    form._on_save = modified_on_save

    # Act
    form._on_save()

    # Assert
    assert captured_form_state is not None, "FormState повинен бути доступним через WorkContext під час обробки"
    assert captured_form_state.to_dict() == {
        "person_name": "Іван",
        "person_surname": "Петрenko",
        "marriage_date": "1920-05-15",
    }, "FormState повинен містити правильні дані з форми"


def test_work_context_form_state_lifecycle():
    """Тест перевіряє повний життєвий цикл FormState у WorkContext."""
    _install_mock_environment()

    # Отримуємо класи з модулів
    import sys

    MockBaseEditForm = sys.modules["base_edit_form"].MockBaseEditForm
    MockWorkContext = sys.modules["services.work_context"].MockWorkContext

    # Arrange
    dbstate = MockDBState()
    form_state_snapshots = []

    class TrackingWorkContext(MockWorkContext):
        def reset(self):
            form_state_snapshots.append({"action": "reset", "old_form_state": self.form_state, "old_db": self.db})
            super().reset()

    form = MockBaseEditForm(dbstate=dbstate, uistate=MockUIState(), form_id="test_form")
    form.work_context = TrackingWorkContext()

    # Act - цикл: заповнення → обробка → скидання
    assert form.work_context.form_state is None, "Початковий стан: form_state = None"

    # Заповнюємо дані
    form.form_state = form.make_form_state()
    form.form_state.update_from_dict({"test_field": "test_value"})
    form.work_context.form_state = form.form_state

    assert form.work_context.form_state is not None, "Після заповнення: form_state не None"
    assert form.work_context.form_state.to_dict() == {"test_field": "test_value"}, "Дані правильно збережені"

    # Скидання
    form.work_context.reset()

    # Assert
    assert form.work_context.form_state is None, "Після скидання: form_state = None"
    assert form.work_context.db is None, "Після скидання: db = None"
    assert len(form_state_snapshots) == 1, "Повинна бути зафіксована одна операція reset"
    assert form_state_snapshots[0]["action"] == "reset", "Операція повинна бути 'reset'"
    assert form_state_snapshots[0]["old_form_state"].to_dict() == {
        "test_field": "test_value"
    }, "Старий стан правильно збережений"


def test_work_context_db_integration():
    """Тест перевіряє інтеграцію WorkContext з DB API під час збереження."""
    _install_mock_environment()

    # Отримуємо MockBaseEditForm з модуля
    import sys

    MockBaseEditForm = sys.modules["base_edit_form"].MockBaseEditForm

    # Arrange
    dbstate = MockDBState()
    form = MockBaseEditForm(dbstate=dbstate, uistate=MockUIState(), form_id="test_form")

    # Початково db не повинно бути встановлено
    assert form.work_context.db is None, "WorkContext повинен початково не мати db"

    # Модифікуємо _on_save щоб захопити стан під час процесингу
    captured_db = None
    original_on_save = form._on_save

    def modified_on_save(_button=None):
        nonlocal captured_db
        form.work_context.reset()
        form.form_state = form.make_form_state()
        form.form_state.update_from_dict(form.collect_snapshot_dict())

        form.work_context.form_state = form.form_state
        form.work_context.db = form.dbstate.db

        # Захоплюємо db під час "обробки"
        captured_db = form.work_context.db

        form.work_context.reset()

    form._on_save = modified_on_save
    form._on_save()

    # Assert
    assert captured_db == dbstate.db, "DB повинно збігатися з переданим під час обробки"
    assert form.work_context.db is None, "WorkContext.db повинен бути скинутий після обробки"


def test_work_context_survives_multiple_save_operations():
    """Тест перевіряє, що WorkContext правильно працює при множинних операціях збереження."""
    _install_mock_environment()

    # Отримуємо MockBaseEditForm з модуля
    import sys

    MockBaseEditForm = sys.modules["base_edit_form"].MockBaseEditForm

    # Arrange
    dbstate = MockDBState()
    form = MockBaseEditForm(dbstate=dbstate, uistate=MockUIState(), form_id="test_form")

    # Act & Assert - перше збереження
    form._on_save()
    assert form.work_context.form_state is None, "Після першого збереження form_state скинутий"

    # Друге збереження з іншими даними
    original_collect = form.collect_snapshot_dict
    form.collect_snapshot_dict = lambda: {"different": "data", "count": 2}

    # Модифікуємо _on_save щоб захопити стан під час процесингу
    captured_states = []
    original_on_save = form._on_save

    def modified_on_save(_button=None):
        form.work_context.reset()
        form.form_state = form.make_form_state()
        form.form_state.update_from_dict(form.collect_snapshot_dict())

        form.work_context.form_state = form.form_state
        form.work_context.db = form.dbstate.db

        # Захоплюємо стан під час "обробки"
        if form.work_context.form_state:
            captured_states.append(form.work_context.form_state.to_dict())

        form.work_context.reset()

    form._on_save = modified_on_save
    form._on_save()

    # Assert
    assert len(captured_states) == 1, "Повинен бути захоплений один стан"
    assert captured_states[0] == {"different": "data", "count": 2}, "Дані другого збереження правильні"
    assert form.work_context.form_state is None, "WorkContext знову скинутий після другого збереження"
