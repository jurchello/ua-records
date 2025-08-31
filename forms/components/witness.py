# pylint: disable=duplicate-code,line-too-long
from lookups import all_occupations, man_castes, man_given, man_surnames
from configs.constants import MAN_MILITARY_RANKS

WITNESS_COMPONENT = {
    "component_id": "witness",
    "version": 1,
    "frames": [
        {
            "title": "Поручитель",
            "fields": [
                {
                    "id": "{mount}.subject_person.create_person",
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
                    "id": "{mount}.subject_person.person",
                    "labels": {"long": "Особа", "middle": "Особа", "short": "Особа"},
                    "type": "person",
                    "order": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
                },
                {
                    "id": "{mount}.subject_person.place",
                    "labels": {"long": "Місце проживання", "middle": "Місце прож.", "short": "Місце"},
                    "type": "place",
                    "order": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2},
                },
                {
                    "id": "{mount}.subject_person.original_name",
                    "labels": {"long": "Ім'я (оригінал)", "middle": "Ім'я (ориг.)", "short": "Ім'я (ориг.)"},
                    "type": "entry",
                    "options": man_given,
                    "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
                },
                {
                    "id": "{mount}.subject_person.normalized_name",
                    "labels": {"long": "Ім'я (нормалізоване)", "middle": "Ім'я (нормаліз.)", "short": "Ім'я (норм.)"},
                    "type": "entry",
                    "options": man_given,
                    "order": {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4},
                },
                {
                    "id": "{mount}.subject_person.original_surname",
                    "labels": {"long": "Прізвище (оригінал)", "middle": "Прізвище (ориг.)", "short": "Прізв. (ориг.)"},
                    "type": "entry",
                    "options": man_surnames,
                    "order": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5},
                },
                {
                    "id": "{mount}.subject_person.normalized_surname",
                    "labels": {
                        "long": "Прізвище (нормалізоване)",
                        "middle": "Прізв. (норм.)",
                        "short": "Прізв. (норм.)",
                    },
                    "type": "entry",
                    "options": man_surnames,
                    "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
                },
                {
                    "id": "{mount}.subject_person.caste",
                    "labels": {"long": "Соціальний стан", "middle": "Соц. стан", "short": "Стан"},
                    "type": "entry",
                    "options": man_castes,
                    "order": {"1": 7, "2": 7, "3": 7, "4": 7, "5": 7},
                },
                {
                    "id": "{mount}.subject_person.occupation",
                    "labels": {"long": "Професія", "middle": "Професія", "short": "Проф."},
                    "type": "entry",
                    "options": all_occupations,
                    "order": {"1": 8, "2": 8, "3": 8, "4": 8, "5": 8},
                },
                {
                    "id": "{mount}.subject_person.military_rank",
                    "labels": {"long": "Військове звання/служба", "middle": "Військ. звання/служба", "short": "Звання"},
                    "type": "entry",
                    "options": MAN_MILITARY_RANKS,
                    "order": {"1": 9, "2": 9, "3": 9, "4": 9, "5": 9},
                },
            ],
        },
        {
            "$include": {
                "component": "landowner",
                "mount": "{mount}.landowner",
                "title": "Поміщик/Поміщиця поручителя",
            }
        },
    ],
}
