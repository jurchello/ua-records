from __future__ import annotations
from lookups import all_occupations, man_castes, man_given, man_surnames
from configs.constants import MAN_MILITARY_RANKS

# pylint: disable=duplicate-code,line-too-long
MAN_SUBJECT_FRAGMENT = [
    {
        "id": "allow_empty",
        "labels": {
            "long": "Створити пусту персону",
            "middle": "Ств. пусту перс.",
            "short": "Пуста перс.",
        },
        "type": "checkbox",
        "default": False,
        "inline_label": True,
        "tooltip": "По замовчуванню вимкнено. Якщо увімкнено, персона буде створена навіть за відсутності імен/прізвищ",
        "order": {"1": 0.5, "2": 0.5, "3": 0.5, "4": 0.5, "5": 0.5},
        "span_rest": True,
    },
    {
        "id": "person",
        "labels": {"long": "Особа", "middle": "Особа", "short": "Особа"},
        "type": "person",
        "help": "**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later**Create empty person** — adds a person without names/surnames.\n\n- Useful for placeholders\n- Can be filled later",
        "order": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
    },
    {
        "id": "place",
        "labels": {"long": "Місце проживання", "middle": "Місце прож.", "short": "Місце"},
        "type": "place",
        "order": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2},
    },
    {
        "id": "original_name",
        "labels": {"long": "Ім'я (оригінал)", "middle": "Ім'я (ориг.)", "short": "Ім'я (ориг.)"},
        "type": "entry",
        "options": man_given,
        "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
    },
    {
        "id": "normalized_name",
        "labels": {"long": "Ім'я (нормалізоване)", "middle": "Ім'я (нормаліз.)", "short": "Ім'я (норм.)"},
        "type": "entry",
        "options": man_given,
        "order": {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4},
    },
    {
        "id": "original_surname",
        "labels": {"long": "Прізвище (оригінал)", "middle": "Прізвище (ориг.)", "short": "Прізв. (ориг.)"},
        "type": "entry",
        "options": man_surnames,
        "order": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5},
    },
    {
        "id": "normalized_surname",
        "labels": {"long": "Прізвище (нормалізоване)", "middle": "Прізв. (норм.)", "short": "Прізв. (норм.)"},
        "type": "entry",
        "options": man_surnames,
        "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
    },
    {
        "id": "caste",
        "labels": {"long": "Соціальний стан", "middle": "Соц. стан", "short": "Стан"},
        "type": "entry",
        "options": man_castes,
        "order": {"1": 7, "2": 7, "3": 7, "4": 7, "5": 7},
    },
    {
        "id": "occupation",
        "labels": {"long": "Професія", "middle": "Професія", "short": "Проф."},
        "type": "entry",
        "options": all_occupations,
        "order": {"1": 8, "2": 8, "3": 8, "4": 8, "5": 8},
    },
    {
        "id": "marriages_count",
        "labels": {"long": "Котрий раз у шлюбі", "middle": "№ шлюбу", "short": "Шл. №"},
        "type": "entry",
        "default": "1",
        "order": {"1": 9, "2": 9, "3": 9, "4": 9, "5": 9},
    },
    {
        "id": "military_rank",
        "labels": {"long": "Військове звання/служба", "middle": "Військ. звання/служба", "short": "Звання"},
        "type": "entry",
        "options": MAN_MILITARY_RANKS,
        "order": {"1": 10, "2": 10, "3": 10, "4": 10, "5": 10},
    },
]
