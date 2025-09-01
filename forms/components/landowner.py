# pylint: disable=duplicate-code,line-too-long
from lookups import all_occupations, man_castes, man_given, man_surnames, woman_surnames
from configs.constants import (
    MAN_MILITARY_RANKS,
    WOMAN_MILITARY_RANKS,
    GENDER_MAN,
    GENDER_WOMAN,
    GENDER_UNKNOWN,
    ALL_GENDERS,
)

LANDOWNER_COMPONENT = {
    "component_id": "landowner",
    "version": 1,
    "frames": [
        {
            "title": "Поміщик/Поміщиця",
            "fields": [
                {
                    "id": "{mount}.allow_empty",
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
                    "id": "{mount}.person",
                    "labels": {"long": "Особа", "middle": "Особа", "short": "Особа"},
                    "type": "person",
                    "order": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
                },
                {
                    "id": "{mount}.place",
                    "labels": {"long": "Місце проживання", "middle": "Місце прож.", "short": "Місце"},
                    "type": "place",
                    "order": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2},
                },
                {
                    "id": "{mount}.gender",
                    "labels": {"long": "Стать", "middle": "Стать", "short": "Стать"},
                    "type": "entry",
                    "options": ALL_GENDERS,
                    "use_combobox": True,
                    "default": GENDER_UNKNOWN,
                    "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
                },
                # Імена (для M або W)
                {
                    "id": "{mount}.original_name",
                    "labels": {"long": "Ім'я (оригінал)", "middle": "Ім'я (ориг.)", "short": "Ім'я (ориг.)"},
                    "type": "entry",
                    "options": man_given,
                    "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_WOMAN]},
                    "order": {"1": 4, "2": 5, "3": 4, "4": 4, "5": 4},
                },
                {
                    "id": "{mount}.normalized_name",
                    "labels": {"long": "Ім'я (нормалізоване)", "middle": "Ім'я (нормаліз.)", "short": "Ім'я (норм.)"},
                    "type": "entry",
                    "options": man_given,
                    "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_WOMAN]},
                    "order": {"1": 5, "2": 4, "3": 5, "4": 5, "5": 5},
                },
                # Поточні прізвища (для M або U)
                {
                    "id": "{mount}.original_surname",
                    "labels": {"long": "Прізвище (оригінал)", "middle": "Прізвище (ориг.)", "short": "Прізв. (ориг.)"},
                    "type": "entry",
                    "options": man_surnames,
                    "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_UNKNOWN]},
                    "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
                },
                {
                    "id": "{mount}.normalized_surname",
                    "labels": {
                        "long": "Прізвище (нормалізоване)",
                        "middle": "Прізв. (норм.)",
                        "short": "Прізв. (норм.)",
                    },
                    "type": "entry",
                    "options": man_surnames,
                    "show_when": {"var": "{mount}.gender", "in": [GENDER_MAN, GENDER_UNKNOWN]},
                    "order": {"1": 7, "2": 7, "3": 7, "4": 7, "5": 7},
                },
                # Жіночі кейси
                {
                    "id": "{mount}.original_surname_maiden",
                    "labels": {
                        "long": "Прізвище дівоче (оригінал)",
                        "middle": "Дівоче прізв. (ориг.)",
                        "short": "Дівоче (ориг.)",
                    },
                    "type": "entry",
                    "options": woman_surnames,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN},
                    "order": {"1": 8, "2": 8, "3": 8, "4": 8, "5": 8},
                },
                {
                    "id": "{mount}.normalized_surname_maiden",
                    "labels": {
                        "long": "Прізвище дівоче (нормалізоване)",
                        "middle": "Дівоче прізв. (норм.)",
                        "short": "Дівоче (норм.)",
                    },
                    "type": "entry",
                    "options": woman_surnames,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN},
                    "order": {"1": 9, "2": 9, "3": 9, "4": 9, "5": 9},
                },
                {
                    "id": "{mount}.original_surname_married",
                    "labels": {
                        "long": "Прізвище у шлюбі (оригінал)",
                        "middle": "Шлюбне прізв. (ориг.)",
                        "short": "Шлюбне (ориг.)",
                    },
                    "type": "entry",
                    "options": woman_surnames,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN},
                    "order": {"1": 10, "2": 10, "3": 10, "4": 10, "5": 10},
                },
                {
                    "id": "{mount}.normalized_surname_married",  # ← виправлено id
                    "labels": {
                        "long": "Прізвище у шлюбі (нормалізоване)",
                        "middle": "Шлюбне прізв. (норм.)",
                        "short": "Шлюбне (норм.)",
                    },
                    "type": "entry",
                    "options": woman_surnames,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN},
                    "order": {"1": 11, "2": 11, "3": 11, "4": 11, "5": 11},
                },
                {
                    "id": "{mount}.caste",
                    "labels": {"long": "Соціальний стан", "middle": "Соц. стан", "short": "Стан"},
                    "type": "entry",
                    "options": man_castes,
                    "order": {"1": 12, "2": 12, "3": 12, "4": 12, "5": 12},
                },
                {
                    "id": "{mount}.occupation",
                    "labels": {"long": "Професія", "middle": "Професія", "short": "Проф."},
                    "type": "entry",
                    "options": all_occupations,
                    "order": {"1": 13, "2": 13, "3": 13, "4": 13, "5": 13},
                },
                # Військове звання (одне поле з різними опціями залежно від статі)
                {
                    "id": "{mount}.military_rank",
                    "labels": {"long": "Військове звання/служба", "middle": "Військ. звання/служба", "short": "Звання"},
                    "type": "entry",
                    "options": MAN_MILITARY_RANKS,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_MAN},
                    "order": {"1": 14, "2": 14, "3": 14, "4": 14, "5": 14},
                },
                {
                    "id": "{mount}.military_rank",
                    "labels": {
                        "long": "Військове звання (по чоловіку)",
                        "middle": "Звання (по чол.)",
                        "short": "Звання",
                    },
                    "type": "entry",
                    "options": WOMAN_MILITARY_RANKS,
                    "show_when": {"var": "{mount}.gender", "equals": GENDER_WOMAN},
                    "order": {"1": 15, "2": 15, "3": 15, "4": 15, "5": 15},
                },
            ],
        },
    ],
}
