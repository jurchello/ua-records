# pylint: disable=duplicate-code
from lookups import man_given, man_surnames
from configs.constants import CLERGY_OCCUPATIONS, MAN_MILITARY_RANKS

CLERGYMAN_COMPONENT = {
    "component_id": "clergyman",
    "version": 1,
    "frames": [
        {
            "title": "Священнослужитель",
            "fields": [
                {
                    "id": "{mount}.person",
                    "labels": {"long": "Особа", "middle": "Особа", "short": "Особа"},
                    "type": "person",
                    "order": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
                },
                {
                    "id": "{mount}.place",
                    "labels": {"long": "Місце", "middle": "Місце", "short": "Місце"},
                    "type": "place",
                    "order": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2},
                },
                {
                    "id": "{mount}.original_name",
                    "labels": {"long": "Ім'я (оригінал)", "middle": "Ім'я (ориг.)", "short": "Ім'я (ориг.)"},
                    "type": "entry",
                    "options": man_given,
                    "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
                },
                {
                    "id": "{mount}.normalized_name",
                    "labels": {"long": "Ім'я (нормалізоване)", "middle": "Ім'я (нормаліз.)", "short": "Ім'я (норм.)"},
                    "type": "entry",
                    "options": man_given,
                    "order": {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4},
                },
                {
                    "id": "{mount}.original_surname",
                    "labels": {"long": "Прізвище (оригінал)", "middle": "Прізвище (ориг.)", "short": "Прізв. (ориг.)"},
                    "type": "entry",
                    "options": man_surnames,
                    "order": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5},
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
                    "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
                },
                {
                    "id": "{mount}.occupation",
                    "labels": {"long": "Посада/Сан", "middle": "Посада/сан", "short": "Посада"},
                    "type": "entry",
                    "options": CLERGY_OCCUPATIONS,
                    "order": {"1": 7, "2": 7, "3": 7, "4": 7, "5": 7},
                },
                {
                    "id": "{mount}.military_rank",
                    "labels": {"long": "Військове звання/служба", "middle": "Військ. звання/служба", "short": "Звання"},
                    "type": "entry",
                    "options": MAN_MILITARY_RANKS,
                    "order": {"1": 8, "2": 8, "3": 8, "4": 8, "5": 8},
                },
            ],
        },
    ],
}
