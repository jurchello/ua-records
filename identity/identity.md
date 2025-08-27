# UARecords — identity.md (Developer Guide)

**Версія:** 2.0 (HV-only, без селекторів)  
**Мова:** українська  
**Аудиторія:** розробники Gramplet/UARecords, які інтегрують `IdentityMap` (UoW) з віртуальним циклом **staging → planner → orchestrator** та погодженням змін у модалці з чекбоксами.

---

## TL;DR

- **Identity (`identity/`)** — **Unit-of-Work** над реальними Gramps-об’єктами: відстеження `new/dirty/deleted`, побудова прев’ю, один **атомарний коміт** у БД через адаптер.
- **Staging (`staging/`)** — **віртуальний світ** у вигляді JSON: `Baseline` (як є) + `After` (як має бути), дифи → **ChangeOps**, застосування підмножини опів (**accepted**) → `accepted_after` (усе без мутації живих об’єктів).
- **Services (`services/`)** — місток між staging та identity: опційний **dedup** `VH → H`, **commit planner** (create/update/delete), **patchers** (накочують JSON на реальні об’єкти), **orchestrator** (сценарій “підготувати → показати UI → підтвердити → закомітити”).
- **Serializers (`serializers/`)** — тонкі перетворювачі Gramps-об’єктів у канонічний JSON для staging.

> У цьому підході є лише два типи ідентифікаторів:
> - **H** — реальний handle з Gramps (рядок-UUID, **без префікса**).
> - **VH:** — “віртуальний handle” для нового об’єкта до моменту створення.

---

## Глосарій

- **Baseline (B):** знімок поточного стану об’єктів із БД (тільки існуючі **H**), у канонічному JSON.
- **After (A):** віртуальний “цільовий” стан у JSON-графі; може містити **H** та **VH:**.
- **Dedup (опційно):** спроба співставити **VH** зі вже існуючим **H** (замість створення) — це лише оптимізація.
- **ChangeOp:** атомарна операція над конкретним `path` у JSON (`set/add/remove/replace`, `create_object`, `delete_object`) з **стабільним `id`** для чекбоксу.
- **accepted_after:** результат застосування тільки **позначених користувачем** ChangeOps до Baseline (в пам’яті; без змін реальних об’єктів).
- **CommitPlan:** план коміту у фазах: `creates` (матеріалізація VH), `updates` (накочування полів/зв’язків), `deletes`.
- **Patchers:** міні-адаптери, що переносять JSON у реальні Gramps-об’єкти (сеттери, побудова зв’язків).
- **IdentityMap:** тримає унікальні інстанси, відслідковує зміни, комітить через `GrampsAdapter`.
- **GrampsAdapter:** місток до Gramps-репозиторію: `add(kind,obj) -> handle`, `commit(kind,obj)` та (опційно) `remove(kind,handle)`.

---

## Потік даних (високорівнево)

```
                 +------------------------------+
                 |        Forms / Logic         |
                 |     (ваша доменна логіка)    |
                 +---------------+--------------+
                                 |
                                 v
                    +------------------------+
                    |      STAGING / AFTER   |   <-- A (H, VH)
                    +------------+-----------+
                                 |
                                 v
        +---------------------------------------------+
        |   DIFF (Baseline vs After) → ChangeOps      |
        +-------------------+-------------------------+
                            |
                     (UI: чекбокси)
                            |
                 accepted_op_ids (підмножина)
                            |
            +---------------+----------------+
            | apply(Baseline, accepted_ops) |
            |         → accepted_after      |
            +---------------+----------------+
                            |
                            v
                  +----------------------+
                  |    CommitPlanner     |
                  |  (create/update/del) |
                  +-----------+----------+
                              |
                              v
          +------------------------------------------+
          | Orchestrator (одна транзакція):          |
          |  create VH→H → patch/update → delete     |
          |  → identity.commit_all(adapter)          |
          +------------------------------------------+
```

---

## Структура проєкту

```
uarecords/
  identity/
    identity_map.py          # Unit-of-Work (реальні об’єкти)
    gramps_adapter.py        # адаптер до репозиторію Gramps
    builder.py               # deep_diff (використовується у прев’ю)
    preview.py               # плоскі рядки для UI
    __init__.py

  serializers/
    gramps_person.py         # → JSON
    gramps_event.py          # → JSON
    gramps_family.py         # → JSON
    __init__.py

  staging/
    ids.py                   # утиліти для H/VH
    graph.py                 # простий контейнер After-графа
    json_path.py             # парсер/апдейтер шляхів a.b[c]
    ops.py                   # ChangeOps builder (із flat diff)
    apply.py                 # apply(accepted_ops) → accepted_after
    validate.py              # перевірка VH-посилань
    __init__.py

  services/
    dedup_service.py         # опційний VH→H дедуп
    commit_planner.py        # розклад у creates/updates/deletes
    orchestrator.py          # сценарій виконання плану
    patchers/
      apply_helpers.py
      person.py
      event.py
      family.py
    __init__.py

  schema_types.py            # ObjKey, ID_KEYS
```

> **Примітка:** ми не використовуємо `types.py`, щоб не затіняти stdlib `types`.

---

## Контракти даних

### ObjKey / ідентифікатори

- `kind`: `"Person" | "Event" | "Family" | ..."`
- `oid`:
  - **H** — реальний UUID (рядок **без префікса**),
  - **VH:** — рядок із префіксом `VH:` (напр., `"VH:wife1"`).

### ChangeOp
```yaml
ChangeOp:
  id:      string          # стабільний id для чекбоксу
  section: "new" | "modified" | "deleted"
  ref:     { kind, oid }   # oid = H | VH
  path:    string          # dotted path, з [key] для списків
  before:  any
  after:   any
  op_type: "create_object" | "delete_object" | "set" | "add" | "remove" | "replace"
```

### CommitPlan
```yaml
CommitPlan:
  creates: [ { kind, oid: VH, data } ]
  updates: [ { kind, oid: H|VH, data } ]   # VH у updates допускається до remap
  deletes: [ { kind, oid: H,  data } ]
```

---

## Життєвий цикл

### 1) Baseline
- **Вхід:** список існуючих Gramps-об’єктів.
- **Процес:** серіалізація у канонічний JSON (`serializers/*`), ключі — `(kind, handle)`.
- **Вихід:** `baseline: { (kind, H): json }`.

### 2) After
- **Вхід:** форма/логіка (нові та існуючі об’єкти, **без** змін у БД).
- **Процес:** формування JSON-графа з H та VH: `after: { (kind, H|VH): json }`.  
  У payload-ах зв’язки дозволено посилати на `VH:*` (ще не створені об’єкти).

### 3) Diff → ChangeOps
- **Вхід:** `baseline`, `after`.
- **Процес:** побудова ChangeOps (`staging/ops.py`) — об’єктні create/delete та поля `set/add/remove/replace`.
- **Вихід:** `ops: ChangeOp[]` для UI (усі активні за замовчуванням).

### 4) Вибір користувача (accepted)
- **Вхід:** `ops`.
- **Процес:** користувач знімає небажані чекбокси; рекомендується live-валідація залежностей (напр., якщо payload посилається на `VH:x`, має бути прийнятий `create_object` для `VH:x`).
- **Вихід:** `accepted_op_ids`.

### 5) Apply
- **Вхід:** `baseline`, `ops`, `accepted_op_ids`.
- **Процес:** чисте застосування підмножини опів у пам’яті (`staging/apply.py`).
- **Вихід:** `accepted_after: { (kind, H|VH): json }`.

### 6) CommitPlanner
- **Вхід:** `baseline`, `accepted_after`.
- **Процес:** визначення `creates/updates/deletes` (`services/commit_planner.py`).
- **Вихід:** `CommitPlan`.

### 7) Orchestrator (одна транзакція)
- **create:** побудувати реальні об’єкти з мінімальним payload (через `patchers/*.build_*`), `idmap.add_new(...)` → отримати **H** для кожного **VH** (мапа `vh_to_h`).
- **update:** ремапнути всі посилання `VH → H` у payload-ах → накотити на вже приєднані об’єкти (`patchers/*.patch_*`) → `idmap.mark_dirty(...)`.
- **delete:** якщо є — викликати `adapter.remove(kind, handle)`.
- **commit:** `idmap.commit_all(adapter)`.

---

## Валідація HV-графа

`staging/validate.py` перевіряє, що:
- кожен рядок із `VH:` у payload-ах посилається на вузол `(kind, "VH:...")` у `after` (тобто буде створений),
- немає “висячих” посилань після фільтрації accepted-опів.

---

## Приклад: “Шлюб із невідомою дружиною”

### Відомо з БД (Baseline):
- Чоловік: `kind="Person", handle="MAN-UUID-123..."`.
- Родина:  `kind="Family", handle="F2-UUID-456..."` (поки без дружини).
- Подія шлюбу вже існує **або буде новою** (обидва варіанти можливі).

### After (HV):
```yaml
# Нова дружина
("Person","VH:wife1"):
  gid: ""
  gender: "F"
  primary_name:
    first_name: "Олена"
    surnames: [{ text: "Петренко", type: "" }]

# Нова подія шлюбу (якщо немає існуючої)
("Event","VH:mar1"):
  type: "Marriage"
  date: { yyyy: 1890, mm: 5, dd: 10 }
  place: { place: "" }

# Оновлення існуючої родини: додати дружину і посилання на подію
("Family","F2-UUID-456..."):
  spouses:
    - { person: "MAN-UUID-123..." }
    - { person: "VH:wife1" }
  event_refs:
    - { event: "VH:mar1", role: "" }
```

### Далі:
- **Diff → ChangeOps:** `create_object(VH:wife1)`, `create_object(VH:mar1)` (якщо немає H), зміни полів у `Family(F2-UUID-456...)`.
- **UI:** користувач може зняти, скажімо, заповнення `place`, але залишити дружину та сам факт події/шлюбу.
- **Apply → accepted_after:** формується узгоджений граф.
- **CommitPlan:**
  - `creates`: `Person(VH:wife1)`, `Event(VH:mar1)` (мінімальні дані).
  - `updates`: `Family(F2-UUID-456...)` (повний payload зі зв’язками).
- **Orchestrator:**
  1) create → `VH:wife1 → H:WIFE-UUID-...`, `VH:mar1 → H:EV-UUID-...`.
  2) update Family: `spouses = [MAN-UUID-..., WIFE-UUID-...]`, `event_refs += [EV-UUID-...]`.
  3) commit_all → транзакція комітиться.

---

## JSON-шляхи (приклади)

```
primary_name.first_name
primary_name.surnames[Петренко].type
event_refs[EV-UUID-...].role
spouses[MAN-UUID-...]
spouses[VH:wife1]
```

> У списках використовуються **ключі** елементів (handle або VH), а не позиції.

---

## Мінімальні payload-и на create (практично)

- **Person:** `{ gid?, gender? }` (+ ім’я за бажанням; головне — щоб фабрика створила валідний об’єкт і повернула handle).
- **Event:** `{ type }` (+ дата/місце за потреби).
- **Family:** `{ gid? }` — зазвичай зв’язки ставляться на фазі `update`.

> Повний стан накочується в `update` (patchers).

---

## Ролі модулів

### `staging/*`
- формує та порівнює JSON;  
- не викликає Gramps-API;  
- продукує ChangeOps та застосовує прийняті опи.

### `services/*`
- `dedup_service.py` — опційно зводить деякі `VH` до існуючих `H`;
- `commit_planner.py` — складає план create/update/delete;
- `patchers/*` — як саме оновити реальні об’єкти Gramps;
- `orchestrator.py` — послідовність дій у транзакції.

### `identity/*`
- `IdentityMap` — трекає нові/змінені/видалені, робить знімки та комітить;
- `GrampsAdapter` — конкретні `add/commit/remove` у вашому середовищі.

---

## Поради з UX/валідації

- Будуйте ChangeOps один раз при відкритті модалки; використовуйте стабільні `id`.
- Якщо користувач відхилив `create_object` для `VH:x`, автоматично знімайте всі опи, які посилаються на `VH:x`.
- Показуйте групування: за об’єктами, за секціями (`new/modified/deleted`), за шляхами.

---

## Тестування

- **staging:** юніт-тести чистими JSON (diff/ops/apply/validate).
- **services:** тести планувальника та оркестратора з мок-адаптером та простими фейковими об’єктами.
- **identity:** тести прев’ю та коміту (new/dirty/deleted, baseline snapshots).

---

## ЧаПи

**Q:** Чому без селекторів?  
**A:** У вашому флоу існуючі об’єкти підтягуються драг-н-дропом, отже їхні handle відомі заздалегідь (H). Селектори потрібні лише коли handle невідомий під час складання After.

**Q:** Чи можна відхилити створення `VH`, якщо на нього посилаються інші вузли?  
**A:** Так, але залежні опи мають бути зняті або автоматично вимкнені. Валідація ловитиме “висячі” посилання.

**Q:** Де логіка репозиторіїв/індексів?  
**A:** У `services/` (dedup, patchers, orchestrator). `identity/` лишається універсальним UoW.

---

## Висновок

Архітектура **staging → diff → accept → apply → plan → orchestrate → commit**:
- унеможливлює мутацію живих об’єктів до апруву;
- дає дрібнозернистий контроль змін у модалці;
- комітить все **атомарно**;
- зберігає `identity/` простим і незалежним.

Дотримуйтесь меж модулів — і інтеграція буде передбачуваною, тестованою та стійкою.
