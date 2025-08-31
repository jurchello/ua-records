# pylint: disable=duplicate-code
from __future__ import annotations
from lookups import all_occupations, woman_castes, woman_given, woman_surnames
from configs.constants import WOMAN_MILITARY_RANKS

WOMAN_SUBJECT_FRAGMENT = [
    {
        "id": "create_person",
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
        "options": woman_given,
        "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
    },
    {
        "id": "normalized_name",
        "labels": {"long": "Ім'я (нормалізоване)", "middle": "Ім'я (нормаліз.)", "short": "Ім'я (норм.)"},
        "type": "entry",
        "options": woman_given,
        "order": {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4},
    },
    {
        "id": "original_surname_before_marriage",
        "labels": {
            "long": "Прізвище до шлюбу (оригінал)",
            "middle": "Дошлюбне прізв. (ориг.)",
            "short": "Дошлюбне (ориг.)",
        },
        "type": "entry",
        "options": woman_surnames,
        "order": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5},
    },
    {
        "id": "normalized_surname_before_marriage",
        "labels": {
            "long": "Прізвище до шлюбу (нормалізоване)",
            "middle": "Дошлюбне прізв. (норм.)",
            "short": "Дошлюбне (норм.)",
        },
        "type": "entry",
        "options": woman_surnames,
        "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
    },
    {
        "id": "original_surname_after_marriage",
        "labels": {
            "long": "Прізвище після шлюбу (оригінал)",
            "middle": "Прізв. після шл. (ориг.)",
            "short": "Після шл. (ориг.)",
        },
        "type": "entry",
        "options": woman_surnames,
        "order": {"1": 7, "2": 7, "3": 7, "4": 7, "5": 7},
    },
    {
        "id": "normalized_surname_after_marriage",
        "labels": {
            "long": "Прізвище після шлюбу (нормалізоване)",
            "middle": "Прізв. після шл. (норм.)",
            "short": "Після шл. (норм.)",
        },
        "type": "entry",
        "options": woman_surnames,
        "order": {"1": 8, "2": 8, "3": 8, "4": 8, "5": 8},
    },
    {
        "id": "caste",
        "labels": {"long": "Соціальний стан", "middle": "Соц. стан", "short": "Стан"},
        "type": "entry",
        "options": woman_castes,
        "order": {"1": 9, "2": 9, "3": 9, "4": 9, "5": 9},
    },
    {
        "id": "occupation",
        "labels": {"long": "Професія", "middle": "Професія", "short": "Проф."},
        "type": "entry",
        "options": all_occupations,
        "order": {"1": 10, "2": 10, "3": 10, "4": 10, "5": 10},
    },
    {
        "id": "marriages_count",
        "labels": {"long": "Котрий раз у шлюбі", "middle": "№ шлюбу", "short": "Шл. №"},
        "type": "entry",
        "default": "1",
        "order": {"1": 11, "2": 11, "3": 11, "4": 11, "5": 11},
    },
    {
        "id": "military_rank",
        "labels": {"long": "Звання (по чоловіку)", "middle": "Звання (по чол.)", "short": "Звання"},
        "type": "entry",
        "options": WOMAN_MILITARY_RANKS,
        "order": {"1": 12, "2": 12, "3": 12, "4": 12, "5": 12},
    },
]
