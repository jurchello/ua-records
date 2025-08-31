# UARecords — Конфігурація форм (README, UA)

Цей документ описує, як налаштовувати **форми**, **компоненти** та **фрагменти** у UARecords, а також усі підтримувані опції полів, механіку керування довжиною міток (label mode) через щільність (density), правила drag‑and‑drop, логіку макета та оновлення GUI.

> Приклади взяті з реальних модулів: `BaseEditForm`, `FieldRenderer`, `FrameBuilder`, компонентів `landowner`, `witness`, `clergyman` і фрагментів `man_subject`, `woman_subject` тощо.


## 1) Структура форм і розширення

### 1.1. Мінімальна форма
```python
from forms.components import COMPONENTS_REGISTRY
from forms.fragments import FRAGMENTS_REGISTRY
from utils.include import expand_form

FORM = {
    "marriage": {
        "id": "marriage",
        "title": "Форма шлюбу",
        "list_label": "Додати шлюб з метричної книги",
        "type": "Шлюб",
        # необов'язково: "columns": 3 (кількість «пар» мітка+контрол у фреймі)
        "tabs": [
            {
                "id": "common_box",
                "titles": {"short": "🗂️", "middle": "Загал.", "long": "Загальне", "default": "Загальне"},
                "frames": [{
                    "title": "Загальні параметри",
                    "fields": [
                        {"id": "common_box.citation", "label": "Цитата", "type": "citation", "default": "C12345"},
                        {"id": "common_box.marriage_place", "label": "Місце реєстрації шлюбу", "type": "place", "default": "P00001"},
                        {"id": "common_box.tags_for_new_people", "label": "Теги для нових персон", "type": "entry", "span_rest": True},
                    ],
                }],
            },
        ],
    }
}

# ВАЖЛИВО: Перед рендером робимо розширення $include та $fragment
FORM_EXPANDED = expand_form(FORM, COMPONENTS_REGISTRY, FRAGMENTS_REGISTRY)
```
- `tabs[].titles` — словник варіантів заголовків вкладки за режимом міток: `short | middle | long` (і опціонально `default`).  
  **BaseEditForm** під час побудови підставляє назву вкладки відповідно до поточного `label_mode`.

### 1.2. Розширення `$include` та `$fragment`
- **$include** — підключає **компонент** за ключем `component`, монтує його у вказаний шлях `mount` і може задати локальний `"title"`:
```jsonc
{ "$include": { "component": "witness", "mount": "groom_box.witness_box_1", "title": "1. Поручитель нареченого" } }
```
- **$fragment** — вмонтовує **фрагмент** (набір локальних полів без префіксів), додає до кожного поля `mount` у його `id`:
```jsonc
{"$fragment": {"fragment": "man_subject", "mount": "groom_box.subject_person"}}
```

Після `expand_form(...)` ви отримуєте повний, «плаский» опис форми без `$include`/`$fragment` — саме його рендерить GUI.


## 2) Вкладки (tabs) і зміна довжини міток (label mode)

### 2.1. Модель **Label Mode**
- Джерело правди: `configs.constants.get_label_mode()` → повертає `"short" | "middle" | "long"`.
- Синхронізація з щільністю: `sync_label_mode_from_density()` автоматично мапить:
  - `compact → short`
  - `normal → middle`
  - `spacious → long`

### 2.2. Оновлення назв вкладок
- Підписка вікна форми на зміну режиму:
  ```python
  self._label_mode_sub = subscribe_label_mode(self._on_label_mode_changed)
  ```
- На подію — оновлюємо всі таби:
  ```python
  def _on_label_mode_changed(self, _mode: str) -> None:
      self._update_tab_titles(0)
      if self._notebook:
          self._notebook.queue_draw()
  ```
- Логіка вибору підпису:
  ```python
  titles = tab_config.get("titles", {})
  text = titles.get(get_label_mode()) or titles.get("default") or base_text
  label.set_markup(GLib.markup_escape_text(text))
  label.set_tooltip_text(titles.get("long") or titles.get("default") or base_text)
  ```

> **Порада.** Щоб усе працювало динамічно, тримайте ключі вкладок саме як `short/middle/long`, а не `1/2`.


## 3) Фрейми (frames) та поля (fields)

### 3.1. Фрейм
```jsonc
{
  "title": "Наречена",
  "prefix": "...",
  "background_color": "Gdk.RGBA(0.98, 0.94, 0.85, 0.3)", // опц.
  "fields": [ /* див. нижче */ ]
}
```
`FrameBuilder` застосовує відступи/рамки з `density`. Заголовок фрейма ставиться як `Gtk.Frame` label.

### 3.2. Типи полів
Підтримуються типи:  
- `"entry"` — текстове поле з підказками (EntryCompletion) або комбобоксом, якщо `use_combobox=True`.  
- `"person"`, `"place"`, `"citation"` — DnD‑лінки на об’єкти БД (перетягування з дерева Gramps).  
- `"check"` / `"checkbox"` — логічні прапорці; можна зробити **inline** етикетку через `inline_label=True`.  
- `"spacer"` — порожній простір для вирівнювання.

### 3.3. Ключі полів (повний список)
```jsonc
{
  "id": "bride_box.subject_person.original_name",   // Унікальний ID (після розширення $fragment/$include)
  "type": "entry" | "person" | "place" | "citation" | "check" | "checkbox" | "spacer",

  // ТЕКСТ/МІТКИ
  "label": "Ім'я (оригінал)",                       // fallback, якщо немає "labels"
  "labels": {                                       // адаптивні мітки (рекомендується)
    "long": "Ім'я (нормалізоване)",
    "middle": "Ім'я (нормаліз.)",
    "short": "Ім'я (н.)",
    "default": "Ім'я"                               // опціонально
  },
  "tooltip": "Пояснення"                             // опціонально, для checkbox inline і DnD-лінків

  // ВИПАДКИ ДЛЯ entry
  "options": ["...", "..."] | some_lookup,          // опц.: словник/провайдер підказок
  "use_combobox": true,                              // опц.: замість entry з completion — випадаючий список

  // ЗНАЧЕННЯ ЗАМОВЧУВАННЯ
  "default": "значення",                             // для entry/combobox або handle/gramps_id для DnD

  // МАКЕТ / РОЗТАШУВАННЯ
  "order": { "1": 1, "2": 1, "3": 1, "default": 1 } // позиція в межах фрейма (див. §4)
           | "c1.o1, c2.o1, c3.o2",                 // альтернативний рядковий синтаксис
  "span_rest": true,                                 // зайняти весь залишок ряду (контрол розтягнеться)
  "span_pairs": 2 | { "default": 1, "3": 2 },        // зайняти N «пар» мітка+контрол (див. §4.2)
  "show_when_cols_in": [3,4,5],                      // показувати тільки при таких кількостях колонок

  // УМОВНЕ ВІДОБРАЖЕННЯ ЗА СТАНОМ
  "show_when": { "var": "{mount}.gender", "equals": "Жінка" }
             | { "var": "{mount}.gender", "in": ["Чоловік","Жінка"] },

  // МАПІНГ СТАНУ
  "state_key": "{mount}.military_rank",              // кілька контролів пишуть у спільний ключ state

  // SPACER
  "row_height": 6                                    // висота порожнього рядка/прокладки
}
```

#### 3.3.1. Мітки (`labels`) і підказки
`FieldRenderer._label_for_field` використовує `labels[mode]` де `mode = get_label_mode()`.  
Tooltip для поля (де релевантно) береться з `labels["long"]` або `labels["default"]` (як fallback).

#### 3.3.2. DnD‑поля (`person/place/citation`)
- Початковий текст береться з правил `get_dnd_rules()` (див. §5).
- Якщо заданий `"default"` як **Gramps ID**, він буде розгорнутий у назву об’єкта.
- Кнопка ✕ очищає вибір; перетягування можливе за «grip» (символ `∷`).

#### 3.3.3. Checkbox
- `inline_label=True` — підпис праворуч усередині кнопки (з автоматичним переносом).
- `max_label_chars` — опціональна межа для ширини inline‑тексту.


## 4) Макет і вплив `columns`

### 4.1. `columns` (frame_pairs)
Фрейм відображає поля в **N парах** (N = `columns`) — кожна пара: **label + widget**.  
За замовчуванням береться `form_config["columns"]` (якщо є) або `3` у `BaseEditForm`.

### 4.2. `order` і розкладка
Поле має **ключ сортування** у межах свого фрейма:
- Варіант 1 — словник:
  ```json
  "order": { "1": 1, "2": 1, "3": 2, "default": 10 }
  ```
  де ключ — кількість пар у фреймі (`columns`), значення — позиція.
- Варіант 2 — рядок: `"c1.o1, c2.o1, c3.o2"` (cN.oM ⇢ для N колонок — порядок M).
- Якщо `order` не задано — використовується **порядок створення** (в конфігу).

### 4.3. Розтягування (`span_rest` / `span_pairs`)
- `span_rest: true` — контрол займе весь **залишок** поточного рядка (етикетка залишається в своїй клітинці).
- `span_pairs: N` — займе **N пар**. Можна задавати окремо для різних `columns`:
  ```json
  "span_pairs": { "default": 1, "3": 2 }
  ```

### 4.4. Адаптація при зміні `columns`
При зміні настройки колонок (в налаштуваннях плагіна) форма перевідкривається (`_refresh_open_forms`), розкладка перераховується, а поля відображаються з урахуванням `show_when_cols_in`, `order` та `span_*`.


## 5) DnD — правила плейсхолдерів і ширин

Налаштовується через функції в `configs.constants`:
```python
def get_dnd_rules() -> list[dict]:
    return [
        {
            "match": {"field_id": {"endswith": "person_owner"}},
            "placeholder": "Перетягни поміщика сюди...",
            "width": get_person_name_length(),
        },
        {
            "match": {"field_type": {"equals": "person"}},
            "placeholder": "Перетягни особу сюди...",
            "width": get_person_name_length(),
        },
        {
            "match": {"field_type": {"equals": "place"}},
            "placeholder": "Перетягни місце сюди...",
            "width": get_place_title_length(),
        },
        {
            "match": {"field_type": {"equals": "citation"}},
            "placeholder": "Перетягни цитату сюди...",
            "width": get_citation_text_length(),
        },
    ]
```
- `match` може перевіряти `field_id` (`equals`/`startswith`/`endswith`) та/або `field_type`.
- Якщо жодне правило не підходить — використовується `get_dnd_default()`.

Кольори DnD/entry полів:
```python
COLOR_EMPTY_DND   = "#eaeaea"
COLOR_FILLED_DND  = "#dfffce"
COLOR_EMPTY_INPUT = "#ffffff"
COLOR_FILLED_INPUT= "#dfffce"
```


## 6) Щільність форми (density) та розміри

Щільність визначається через `settings.settings_manager` (опція «Стиль форм») і зчитується у рантаймі:
```python
DENSITY_SETTINGS = {
  "compact": { "grid_margin": 10, "row_grid_spacing": 3,  "grid_column_spacing": 6, ... },
  "normal":  { "grid_margin": 20, "row_grid_spacing": 10, "grid_column_spacing": 10, ... },
  "spacious":{ "grid_margin": 30, "row_grid_spacing": 15, "grid_column_spacing": 15, ... },
}
```
- Використовується в `FrameBuilder` і `BaseEditForm` для падінгів/відступів/спейсингів.
- `sync_label_mode_from_density()` оновлює `label_mode` згідно щільності.

Довжини скорочень для підказок/DnD беруться з цих налаштувань:
```python
get_person_name_length()
get_place_title_length()
get_citation_text_length()
```


## 7) Компоненти та фрагменти

### 7.1. Компонент (component)
Компонент — це багаторазовий блок із власним набором фреймів/полів. Приклад — `landowner`:
```python
LANDOWNER_COMPONENT = {
  "component_id": "landowner",
  "version": 1,
  "frames": [
    {
      "title": "Поміщик/Поміщиця",
      "fields": [
        {"id": "{mount}.person",  "type": "person", "label": "Особа"},
        {"id": "{mount}.place",   "type": "place",  "label": "Місце"},
        {"id": "{mount}.gender",  "type": "entry",  "options": ALL_GENDERS, "default": GENDER_UNKNOWN, "use_combobox": true},

        // Поля, що залежать від статі
        {"id": "{mount}.original_name", "type": "entry", "options": man_given,  "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_WOMAN]}},
        {"id": "{mount}.normalized_name","type": "entry", "options": man_given,  "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_WOMAN]}},

        // «Поточні» прізвища (для M або U)
        {"id": "{mount}.original_surname",   "type": "entry", "options": man_surnames, "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_UNKNOWN]}},
        {"id": "{mount}.normalized_surname", "type": "entry", "options": man_surnames, "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_UNKNOWN]}},

        // Жіночі кейси: дівоче + у шлюбі
        {"id": "{mount}.original_surname_maiden",   "type": "entry", "options": woman_surnames, "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN}},
        {"id": "{mount}.normalized_surname_maiden", "type": "entry", "options": woman_surnames, "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN}},
        {"id": "{mount}.original_surname_married",  "type": "entry", "options": woman_surnames, "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN}},
        {"id": "{mount}.normalized_surname_married","type": "entry", "options": woman_surnames, "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN}},

        // Спільний стан через state_key
        {"id": "{mount}.military_rank_man",    "state_key": "{mount}.military_rank", "type": "entry", "options": MAN_MILITARY_RANKS,    "show_when": {"var": "{mount}.gender", "equals": GENDER_MAN}},
        {"id": "{mount}.military_rank_woman",  "state_key": "{mount}.military_rank", "type": "entry", "options": WOMAN_MILITARY_RANKS,  "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN}},
      ],
    },
  ],
}
```

> Зверніть увагу на використання шаблону `"{mount}.field"` — при включенні компонента ви задаєте реальний шлях (наприклад, `groom_box.landowner`), і всі ідентифікатори стануть унікальними.

### 7.2. Фрагмент (fragment)
Фрагмент — це «локальний» набір полів (ідентифікатори **без** префіксу). Під час включення їх **прикручує** до `mount`:
```python
register_fragment("woman_subject", [
    { "id": "person", "type": "person",
      "labels": {"long": "Особа", "middle": "Особа", "short": "Особа"} },
    { "id": "place",  "type": "place",
      "labels": {"long": "Місце проживання", "middle": "Місце прож.", "short": "Місце"} },

    { "id": "original_name", "type": "entry", "options": woman_given,
      "labels": {"long": "Ім'я (оригінал)", "middle": "Ім'я (ориг.)", "short": "Ім'я (ориг.)"} },
    { "id": "normalized_name", "type": "entry", "options": woman_given,
      "labels": {"long": "Ім'я (нормалізоване)","middle": "Ім'я (нормаліз.)","short": "Ім'я (норм.)"} },

    // ... інші поля ...
])
```
У фінальному вигляді (після `$fragment`) ідентифікатори стануть на кшталт `bride_box.subject_person.person`, `...place`, `...original_name`, тощо.


## 8) Динаміка GUI і життєвий цикл форми

- **Відкриття/оновлення**: при зміні налаштувань у `UARecords.save_options()` викликається:
  1) `sync_label_mode_from_density()` — змінює режим міток і розсилає подію підписникам;
  2) `_refresh_open_forms()` — кожне відкрите вікно `BaseEditForm` перезапускається через `_on_refresh_options(None)` (очищає кеші опцій, перевідкриває вікно з актуальними налаштуваннями).
- **Живий синк** полів → `BaseEditForm._enable_live_sync()` ставить сигнал `changed` / `toggled` на всі контролі для оперативного оновлення стану.
- **Збирання Gramps ID** → кнопка «Копіювати Gramps ID» обходить усі поля/стан та формує список ID для буфера обміну.


## 9) Налаштування в UI (Settings)

Параметри, що впливають на форми:
- **Колонки** (народження/смерть/шлюб): 1–5 → впливають на розкладку `order`, `show_when_cols_in`, `span_*`.
- **Стиль форм (density)**: `compact | normal | spacious` → керує відступами/спейсингом і **режимом міток** через `sync_label_mode_from_density()`.
- **Макс. довжини**: імен осіб / назв місць / тексту цитат → впливають на усічення/ширини DnD та полів з підказками.

> Після натискання «Зберегти» у налаштуваннях усе застосовується одразу: відкриті форми перевідкриваються, вкладки та мітки оновлюються.


## 10) Підказки і кращі практики

1. **Завжди** використовуйте `labels: {short|middle|long}` для полів **та** `titles: {short|middle|long}` для вкладок.  
2. Для широких рядків використовуйте `span_rest: true` — це легше, ніж вручну рахувати `span_pairs`.
3. Для умовних полів користуйтеся `show_when` з `equals` або `in` — зручно для розгалужень за статтю чи типом об’єкта.
4. Якщо треба синхронізувати декілька контролів в один ключ стану — застосовуйте `state_key`.
5. Для контрольованого порядку на різних `columns` використовуйте або словниковий `order`, або компактний рядковий `"cN.oM"`.
6. Не змішуйте старі ключі вкладок (`"1","2"`) з новими — використовуйте **тільки** `short/middle/long`.


## 11) Система допомоги (Help System)

### 11.1. Кнопки допомоги для полів

UARecords надає вбудовану систему контекстної допомоги для полів форм. Будь-яке поле може мати кнопку допомоги з детальним поясненням.

#### Конфігурація поля з допомогою
```jsonc
{
  "id": "bride_box.subject_person.original_name",
  "type": "entry",
  "label": "Ім'я (оригінал)",
  "help": "Введіть ім'я особи так, як воно записано в оригінальному документі.\n\n**Правила заповнення:**\n- Зберігайте оригінальне написання\n- Використовуйте кириличний або латинський алфавіт\n- *Приклад*: Іван, Мария, Johann",
  "options": ["Іван", "Петро", "Мария"]
}
```

#### Альтернативні ключі
- `"help"` — основний ключ для тексту допомоги
- `"help_text"` — альтернативний ключ (для зворотної сумісності)

#### Підтримка Markdown
Текст допомоги підтримує спрощений Markdown-синтаксис:
- `**жирний текст**` → <b>жирний текст</b>
- `*курсив*` → <i>курсив</i>
- `__підкреслення__` → <u>підкреслення</u>
- Автоматичний перенос рядків

### 11.2. Візуальні характеристики

#### Кнопка допомоги
- **Іконка**: PNG-файл `ui/assets/help.png`
- **Розмір**: 60% від висоти рядка поля (мін. 16px, макс. 48px)
- **Позиція**: Праворуч від поля з відступом 4px
- **Стиль**: Без рамки, без фокусу при кліку
- **Підказка**: "Help"

#### Діалог допомоги
- **Тип**: Модальний діалог
- **Розмір**: 400×300 пікселів (з автоматичним підігнанням контенту)
- **Заголовок**: Береться з мітки поля або ID поля
- **Контент**: Прокручуваний текст з підтримкою розмітки
- **Закриття**: Кнопка "OK" або клік поза діалогом

### 11.3. Технічна реалізація

#### Рендеринг кнопки
Кнопка допомоги додається автоматично через `FieldRenderer._attach_help()`:

```python
def _attach_help(self, widget: Gtk.Widget, field: Dict[str, str], label_text: str) -> Gtk.Widget:
    help_text = field.get("help") or field.get("help_text") or ""
    if not isinstance(help_text, str) or not help_text.strip():
        return widget  # Немає тексту допомоги - повертаємо поле як є
        
    # Створюємо контейнер: поле + кнопка допомоги
    box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
    # ... код створення кнопки ...
```

#### Обробка розмітки
Markdown-розмітка конвертується в Pango markup через `_render_help_markup()`:

```python
def _render_help_markup(self, text: str) -> str:
    s = GLib.markup_escape_text(text)  # Екранування HTML
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)  # **жирний**
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)      # *курсив*  
    s = re.sub(r"__(.+?)__", r"<u>\1</u>", s)      # __підкреслення__
    return s
```

### 11.4. Приклади використання

#### Базова допомога
```jsonc
{
  "id": "common_box.citation",
  "type": "citation", 
  "label": "Цитата",
  "help": "Оберіть або створіть цитату з джерела документа"
}
```

#### Розширена допомога з форматуванням
```jsonc
{
  "id": "bride_box.subject_person.military_rank",
  "type": "entry",
  "label": "Військовий чин",
  "help": "Вкажіть військовий чин особи згідно з документом.\n\n**Чоловічі чини:**\n- Рядовий, Капрал, Сержант\n- Прапорщик, Поручик, Штабс-капітан\n- Капітан, Майор, Підполковник\n\n**Жіночі чини:**\n- Санітарка, Медсестра\n- *Примітка*: жіночі військові чини рідко зустрічаються в цивільних документах",
  "options": ["Рядовий", "Капрал", "Сержант", "Прапорщик"]
}
```

#### Допомога для DnD-полів
```jsonc
{
  "id": "groom_box.subject_person.person",
  "type": "person",
  "label": "Особа",
  "help": "**Перетягніть особу з дерева Gramps або створіть нову.**\n\nЯкщо особа не існує в базі даних:\n1. Залиште поле порожнім\n2. Заповніть інші поля з іменем та прізвищем\n3. Система автоматично створить нову особу при збереженні\n\n*Символ ∷ дозволяє перетягувати поле*"
}
```

### 11.5. Автоматизація та правила

#### Умовна допомога
Допомога може показуватися тільки для певних умов:
```jsonc
{
  "id": "landowner.military_rank_woman",
  "type": "entry", 
  "help": "Жіночі військові чини використовувалися рідко. **Приклади**: Санітарка, Медсестра, Телефоністка",
  "show_when": {"var": "landowner.gender", "equals": "Жінка"}
}
```

#### Успадкування з компонентів/фрагментів  
Кнопки допомоги працюють з `$include` та `$fragment`:
```jsonc
{
  "$include": {
    "component": "witness",
    "mount": "groom_box.witness_1", 
    "title": "Свідок нареченого"
  }
}
```
Всі поля компонента `witness` зберігають свій текст допомоги.

### 11.6. Розробка та налагодження

#### Додавання нових кнопок допомоги
1. Додайте ключ `"help"` до конфігурації поля
2. Використовуйте Markdown для форматування
3. Тестуйте довгі тексти на предмет коректного відображення

#### Відсутня іконка
Якщо файл `ui/assets/help.png` відсутній, система буде показувати помилки. Переконайтеся, що файл існує і доступний для читання.

#### CSS-стилізація
Кнопка допомоги використовує CSS-клас `help-btn` для стилізації. CSS автоматично ініціалізується при першому використанні.

## 12) Довідник ключів (швидка шпаргалка)

### На рівні форми
- `id`, `title`, `list_label`, `type`, `columns?`
- `tabs`: список вкладок

### На рівні вкладки
- `id`, `titles: {short|middle|long|default}`, `frames`

### На рівні фрейма
- `title`, `prefix?`, `background_color?`, `fields`

### Поле
- Обов'язково: `id`, `type`
- Текст: `label?`, `labels?{short|middle|long|default}`, `tooltip?`
- **Допомога**: `help?`, `help_text?` — текст допомоги з підтримкою Markdown
- Value: `default?`, `options?`, `use_combobox?`
- Макет: `order?`, `span_rest?`, `span_pairs?`, `show_when_cols_in?`
- Умовність: `show_when? { var, equals | in }`
- Стан: `state_key?`
- Spacer: `row_height?`

### Підтримувані типи
- `entry`, `person`, `place`, `citation`, `check`/`checkbox`, `spacer`


---

Якщо потрібні приклади «під ключ» під ваш проєкт — додайте свій конфіг у `FORM`, використовуйте `$include`/`$fragment` і дотримуйтеся цих правил. Система рендеру автоматично підлаштує макет та тексти під обраний стиль і кількість колонок.
