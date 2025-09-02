# Staging для безпечного внесення змін (UARecords / Gramps)

Цей модуль забезпечує **поетапне внесення змін** до БД Gramps: ви спочатку формуєте
цільовий стан, отримуєте читабельний **diff**, обираєте що саме прийняти, і лише потім
виконується транзакційний коміт. Це знімає ризик «сліпих» змін і дає прозорий контроль.

---

## Зміст

- [Терміни](#терміни)
- [Огляд модулів](#огляд-модулів)
- [Життєвий цикл staging](#життєвий-цикл-staging)
- [Режими перегляду (All vs Changed)](#режими-перегляду-all-vs-changed)
- [Baseline vs After: повний стан у превʼю](#baseline-vs-after-повний-стан-у-превю)
- [Приклад інтеграції з Processor](#приклад-інтеграції-з-processor)
- [Формування AfterGraph з FormState](#формування-aftergraph-з-formstate)
- [JSON-шляхи та селектори](#json-шляхи-та-селектори)
- [Віртуальні ID `VH:`](#віртуальні-id-vh)
- [Валідація HV-графа](#валідація-hv-графа)
- [Коміт у БД (скелет)](#коміт-у-бд-скелет)
- [Тестування та безпечний запуск](#тестування-та-безпечний-запуск)
- [FAQ](#faq)

---

## Терміни

- **Baseline** — «як є»: **поточні** дані в БД, представлені у HV-JSON (`dict`) для
  тих обʼєктів, які беруть участь у змінах.
- **After** — «як має бути»: **цільовий** стан після редагувань на основі `FormState`.
- **HV JSON** — канонічний словниковий формат («High‑Level View»), не привʼязаний
  до внутрішніх класів Gramps. Ключі обʼєктів: `(kind, oid)`.
- **ChangeOp** — елементарна зміна: створення/видалення обʼєкта або зміна окремого поля.
- **`VH:`** — префікс **віртуального** ідентифікатора (тимчасовий ID для ще не створених
  у БД обʼєктів, напр. `VH:new_cit_1`).

---

## Огляд модулів

```
staging/
├─ ids.py          # ID, h(), vh(), VH_PREFIX — робота з реальними та віртуальними ID
├─ json_path.py    # parse_path(), set_at_path(): робота з dotted-путями та селекторами [key]
├─ graph.py        # AfterGraph — контейнер для цільового стану (after)
├─ ops.py          # build_change_ops(): побудова детального diff (ChangeOp)
├─ apply.py        # apply_ops(): застосування підмножини змін до baseline
└─ validate.py     # validate_hv_graph(): перевірка посилань на VH
```

Ключові ідеї:
- **`AfterGraph`** тримає цільовий стан як мапу `{(kind, oid) -> payload_dict}`.
- **`build_change_ops(baseline, after)`** повертає детальний список змін по полях/шляхах.
- **`apply_ops(baseline, ops, accepted_ids)`** повертає **прийнятий** стан (`accepted_after`)
  після вибіркового прийняття змін.
- **`validate_hv_graph(after_map)`** знаходить поламані VH‑посилання ще до показу diff.

---

## Життєвий цикл staging

1. **Збір вводу**: користувач заповнює форму → `FormState`.
2. **Build After**: процесор формує `AfterGraph` (цільовий стан) з `FormState`.
3. **Валідація HV**: `validate_hv_graph(after_map)` — перевірка VH‑звʼязків.
4. **Завантаження baseline**: з БД читається поточний стан **тільки для залучених ключів**.
5. **Diff**: `build_change_ops(baseline, after)` → список `ChangeOp`.
6. **Review UI**: показ diff. Користувач ставить галочки (вибирає `accepted_ids`).
7. **Apply selection**: `apply_ops(...)` → `accepted_after`.
8. **Commit**: транзакційне створення/оновлення в БД (після підтвердження).

> Пункти 6–8 можуть відбуватись не в процесорі, а у зовнішньому UI‑шарі
> (див. розділ «Інтеграція з Processor»).

---

## Режими перегляду (All vs Changed)

У превʼю зручно мати **два режими**:
- **Changed only** — показати **тільки** змінені поля/обʼєкти (короткий diff).
- **All fields** — показати **повні** дерева обʼєктів ліворуч (baseline) і праворуч (after),
  з підсвіткою відмінностей.

Як це досягається:
- `build_change_ops()` повідомляє **де саме** зміни.
- Для режиму **Changed only** UI просто рендерить тільки ті вузли/поля, які згадуються в `ops`.
- Для режиму **All fields** UI **матеріалізує** повні дерева для ключів з `after_map`
  (і відповідний baseline) і підсвічує відмінності згідно з `ops`.

> Важливо: хоча **baseline** ми вантажимо **лише для ключів з after**, в UI можна показати
> **повний payload кожного з цих обʼєктів** — не лише змінені поля.

---

## Baseline vs After: повний стан у превʼю

- **Чому baseline будується «за ключами after»?**  
  Це нормально для патерну *targeted load*: ми знаємо, які обʼєкти стане(ли)
  ціллю змін, і не вантажимо всю базу — лише дотичні ключі.
- **Чи означає це, що у превʼю зникнуть незмінені поля?**  
  Ні. Для кожного `(kind, oid)` з `after_map` baseline завантажується **повністю**,
  і UI може показати повне дерево полів (режим **All fields**). Просто diff буде порожнім
  для незмінених вузлів.

---

## Приклад інтеграції з Processor

```python
# services/processor_base.py (спрощено)
from dataclasses import dataclass
from typing import Dict, Tuple, Any, List
from abc import ABC, abstractmethod
from staging.graph import AfterGraph
from staging.ops import build_change_ops, ChangeOp
from staging.apply import apply_ops
from staging.validate import validate_hv_graph

ObjKeyT = Tuple[str, str]

@dataclass
class StagingResult:
    baseline: Dict[ObjKeyT, Dict[str, Any]]
    after: Dict[ObjKeyT, Dict[str, Any]]
    ops: List[ChangeOp]
    errors: List[str]

class ProcessorBase(ABC):
    def __init__(self, work_context):
        self.ctx = work_context  # form_state, db, identity_map

    @abstractmethod
    def _build_after_graph(self) -> AfterGraph: ...
    @abstractmethod
    def _load_baseline(self, after_map: Dict[ObjKeyT, Dict[str, Any]]) -> Dict[ObjKeyT, Dict[str, Any]]: ...
    @abstractmethod
    def commit(self, accepted_after: Dict[ObjKeyT, Dict[str, Any]]) -> None: ...

    def stage(self) -> StagingResult:
        after_graph = self._build_after_graph()
        after_map = after_graph.as_map()

        errors = validate_hv_graph(after_map)
        baseline = self._load_baseline(after_map)
        ops = build_change_ops(baseline, after_map)

        return StagingResult(baseline=baseline, after=after_map, ops=ops, errors=errors)

    def accept_selection(self, staging: StagingResult, accepted_ids: List[str]):
        return apply_ops(staging.baseline, staging.ops, accepted_ids)
```

І приклад використання в UI‑шарі (псевдокод):
```python
# десь у BaseEditForm._on_save()
processor = MarriageProcessor(self.work_context)

staging = processor.stage()
if staging.errors:
    show_errors_dialog(staging.errors)
    return

# Відкрити діалог попереднього перегляду
ui_review.show_diff(self, staging)  # рендерить All/Changed режими, дає обрати accepted_ids

accepted_ids = ui_review.get_user_selection()
accepted_after = processor.accept_selection(staging, accepted_ids)

# Поки commit не реалізовано:
print("commit() ще не реалізовано — зміни не збережено.")
# processor.commit(accepted_after)
```

---

## Формування `AfterGraph` з `FormState`

```python
# приклад _build_after_graph() всередині MarriageProcessor
from staging.graph import AfterGraph
from schema_types import ObjKey  # проста структура з полями kind, oid
from staging.ids import vh       # для створення VH-id при нових обʼєктах

def _build_after_graph(self) -> AfterGraph:
    g = AfterGraph()
    fs = self.ctx.form_state

    # А) існуюча персона (оновлення):
    groom = fs.get("groom_box", "subject_person.person")  # dict або обʼєкт-репрезентація
    if groom and isinstance(groom, dict) and groom.get("object"):
        real_handle = groom["object"].get_handle()
        payload = {
            "primary_name": {
                "given": fs.get("groom_box", "subject_person.original_name"),
                "surname": fs.get("groom_box", "subject_person.original_surname"),
            },
            # ... інші поля
        }
        g.put(ObjKey(kind="Person", oid=real_handle), payload)

    # Б) нова Citation (створення):
    cit_oid = vh("new_cit_1").raw  # 'VH:new_cit_1'
    g.put(ObjKey(kind="Citation", oid=cit_oid), {
        "title": fs.get("common_box", "citation_title"),
        "source": {"handle": fs.get("common_box", "source_handle")},
    })

    return g
```

---

## JSON-шляхи та селектори

`json_path.set_at_path(obj, "field.subfield", value)` — встановлює значення за dotted‑шляхом.  
Підтримуються селектори у списках: `listField[<key>].inner` — елемент визначається за `schema_types.ID_KEYS`.

```python
from staging.json_path import set_at_path

obj = {}
set_at_path(obj, "event.citations[VH:new_cit_1].role", "primary")
# Якщо немає елемента з ключем 'VH:new_cit_1' — він буде створений.
```

---

## Віртуальні ID `VH:`

- Нові обʼєкти позначаються `VH:*` до моменту коміту.
- Будь-які посилання на ці обʼєкти теж тимчасово містять `VH:*`.
- Під час `commit` відбувається:
  1) створення всіх `VH:*` у правильному порядку (залежності),
  2) побудова мапи `vh2real`,
  3) **масова заміна** всіх входжень `VH:*` на реальні `handle`,
  4) апдейт наявних обʼєктів.

---

## Валідація HV-графа

```python
from staging.validate import validate_hv_graph

errors = validate_hv_graph(after_map)
if errors:
    # Приклад помилки: "Event:VH:e1 references missing VH:new_cit_1"
    show_errors_to_user(errors)
```

Перевірка гарантує, що всі `VH:*`‑посилання **мають відповідні обʼєкти** в `after_map`,
і ви не підете у превʼю/коміт з «висячими» референсами.

---

## Коміт у БД (скелет)

```python
def commit(self, accepted_after: Dict[ObjKeyT, Dict[str, Any]]) -> None:
    # TODO:
    # 1) Визначити залежності між VH‑обʼєктами → топологічний порядок створення.
    # 2) Створити всі нові обʼєкти (VH → real handle), скласти vh2real.
    # 3) Замінити у всіх payload'ах VH:* на vh2real.
    # 4) Оновити існуючі обʼєкти (by handle).
    # 5) Усе в межах транзакції репозиторіїв.
    print("commit(): скелет методу — реалізація поки відсутня.")
```

---

## Тестування та безпечний запуск

- **Юніт‑тести**: перевірка конструкторів `payload`, `validate_hv_graph`, `build_change_ops`, `apply_ops`.
- **Інтеграційні тести**: UI → `StateCollector` → `FormState` → `Processor.stage()` → `ui_review`.
- **Безпека**: на час тестів ізолюйте середовище через
  `GRAMPSHOME`, `GRAMPS_RESOURCES`, і/або вмикайте «сухий режим» (не викликати `commit`).
- **Processor у тестах**: зручно тримати `commit()` порожнім до готовності
  і **не викликати** його з `_on_save` (поки що), лише `stage()` + превʼю.

---

## FAQ

**Чому baseline вантажиться тільки за ключами `after`?**  
Це прискорює роботу і чітко фокусує перевірку на залучених обʼєктах. Для превʼю
показу повного стану кожного обʼєкта цього достатньо.

**Чи можна у превʼю побачити повний стан, а не лише diff?**  
Так. Режим **All fields** рендерить повні дерева `baseline` і `after` для кожного
ключа, diff лише підсвічує відмінності.

**Навіщо `AfterGraph` і `after_map`?**  
`AfterGraph` — зручний API для побудови цільового стану. `after_map = graph.as_map()` —
звичайний словник, потрібний для `validate_hv_graph`, `build_change_ops`, `apply_ops`.

**Що за помилки повертає `validate_hv_graph`?**  
Вона лінійно обходить `after_map` і збирає всі рядкові значення, що починаються з `VH:`.
Якщо довідковий обʼєкт із таким `VH:` **не представлений** в `after_map`, повертається
людяний опис помилки з конкретним `(kind, oid)` та відсутнім посиланням.

---

## Ліцензія

Цей staging‑шар є частиною UARecords. Ліцензія — згідно з основною ліцензією репозиторію.
