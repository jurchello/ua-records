from __future__ import annotations

from configs.constants import (
    DEFAULT_CITATION_ID,
    DEFAULT_PLACE_ID_1,
    NEW_PERSON_TAGS,
    EXISTING_PERSON_TAGS,
    NEW_EVENT_TAGS,
    NEW_CITATION_TAGS
)

from forms.components import COMPONENTS_REGISTRY
from forms.fragments import FRAGMENTS_REGISTRY
from utils.include import expand_form


FORM = {
    "marriage": {
        "id": "marriage",
        "title": "Форма шлюбу",
        "list_label": "Додати шлюб з метричної книги",
        "type": "Шлюб",
        "tabs": [
            {
                "id": "common_box",
                "titles": {"short": "🗂️", "middle": "Загал.", "long": "Загальне"},
                "frames": [
                    {
                        "title": "Загальні параметри",
                        "fields": [
                            {
                                "id": "common_box.citation",
                                "label": "Цитата",
                                "type": "citation",
                                "default": DEFAULT_CITATION_ID,
                                "order": {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1},
                                "span_rest": True,
                            },
                            {
                                "id": "common_box.marriage_place",
                                "labels": {
                                    "long": "Місце реєстрації шлюбу",
                                    "middle": "Місце реєстр. шл.",
                                    "short": "Місце шл.",
                                },
                                "type": "place",
                                "default": DEFAULT_PLACE_ID_1,
                                "order": {"1": 2, "2": 2, "3": 2, "4": 2, "5": 2},
                                "span_rest": True,
                            },
                            {
                                "id": "common_box.tags_for_new_people",
                                "labels": {
                                    "long": "Теги для нових персон",
                                    "middle": "Теги для нов. перс.",
                                    "short": "Теги нов. перс.",
                                },
                                "type": "entry",
                                "default": ", ".join(NEW_PERSON_TAGS),
                                "order": {"1": 3, "2": 3, "3": 3, "4": 3, "5": 3},
                                "span_rest": True,
                            },
                            {
                                "id": "common_box.tags_for_existing_people",
                                "labels": {
                                    "long": "Теги для існуючих персон",
                                    "middle": "Теги для існ. персон",
                                    "short": "Теги існ. перс.",
                                },
                                "type": "entry",
                                "default": ", ".join(EXISTING_PERSON_TAGS),
                                "order": {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4},
                                "span_rest": True,
                            },
                            {
                                "id": "common_box.tags_for_new_events",
                                "labels": {
                                    "long": "Теги для нових подій",
                                    "middle": "Теги нових подій",
                                    "short": "Теги нов. под.",
                                },
                                "type": "entry",
                                "default": ", ".join(NEW_EVENT_TAGS),
                                "order": {"1": 5, "2": 5, "3": 5, "4": 5, "5": 5},
                                "span_rest": True,
                            },
                            {
                                "id": "common_box.tags_for_citation",
                                "labels": {"long": "Теги для цитати", "middle": "Теги для цит.", "short": "Теги цит."},
                                "type": "entry",
                                "default": ", ".join(NEW_CITATION_TAGS),
                                "order": {"1": 6, "2": 6, "3": 6, "4": 6, "5": 6},
                                "span_rest": True,
                            },
                        ],
                    }
                ],
            },
            {
                "id": "groom_box",
                "titles": {"short": "🤵", "middle": "Наречений", "long": "Наречений"},
                "frames": [
                    {
                        "title": "Наречений",
                        "fields": [
                            {"$fragment": {"fragment": "man_subject", "mount": "groom_box.subject_person"}},
                            {
                                "id": "groom_box.subject_person.age",
                                "labels": {"long": "Вік", "middle": "Вік", "short": "Вік"},
                                "type": "entry",
                                "order": {"1": 11, "2": 11, "3": 11, "4": 11, "5": 11},
                            },
                        ],
                    },
                    {
                        "$include": {
                            "component": "landowner",
                            "mount": "groom_box.landowner",
                            "title": "Поміщик/Поміщиця нареченого",
                        }
                    },
                ],
            },
            {
                "id": "bride_box",
                "titles": {"short": "👰", "middle": "Наречена", "long": "Наречена"},
                "frames": [
                    {
                        "title": "Наречена",
                        "fields": [
                            {"$fragment": {"fragment": "woman_subject", "mount": "bride_box.subject_person"}},
                            {
                                "id": "bride_box.subject_person.age",
                                "labels": {"long": "Вік", "middle": "Вік", "short": "Вік"},
                                "type": "entry",
                                "order": {"1": 13, "2": 13, "3": 13, "4": 13, "5": 13},
                            },
                        ],
                    },
                    {
                        "$include": {
                            "component": "landowner",
                            "mount": "bride_box.landowner",
                            "title": "Поміщик/Поміщиця нареченої",
                        }
                    },
                ],
            },
            {
                "id": "groom_witness_1",
                "titles": {"short": "①🤝", "middle": "1 Поруч.", "long": "1. Поручитель нареченого"},
                "frames": [
                    {
                        "$include": {
                            "component": "witness",
                            "mount": "groom_box.witness_box_1",
                            "title": "1. Поручитель нареченого",
                        }
                    },
                ],
            },
            {
                "id": "groom_witness_2",
                "titles": {"short": "②🤝", "middle": "2 Поруч.", "long": "2. Поручитель нареченого"},
                "frames": [
                    {
                        "$include": {
                            "component": "witness",
                            "mount": "groom_box.witness_box_2",
                            "title": "2. Поручитель нареченого",
                        }
                    },
                ],
            },
            {
                "id": "bride_witness_1",
                "titles": {"short": "③🤝", "middle": "3 Поруч.", "long": "3. Поручитель нареченої"},
                "frames": [
                    {
                        "$include": {
                            "component": "witness",
                            "mount": "bride_box.witness_box_1",
                            "title": "3. Поручитель нареченої",
                        }
                    },
                ],
            },
            {
                "id": "bride_witness_2",
                "titles": {"short": "④🤝", "middle": "4 Поруч.", "long": "4. Поручитель нареченої"},
                "frames": [
                    {
                        "$include": {
                            "component": "witness",
                            "mount": "bride_box.witness_box_2",
                            "title": "4. Поручитель нареченої",
                        }
                    },
                ],
            },
            {
                "id": "clergymen_box",
                "titles": {"short": "⛪️", "middle": "Духів.", "long": "Священнослужителі"},
                "frames": [
                    {
                        "$include": {
                            "component": "clergyman",
                            "mount": "clergymen_box.clergyman_1",
                            "title": "Священнослужитель 1",
                        }
                    },
                    {
                        "$include": {
                            "component": "clergyman",
                            "mount": "clergymen_box.clergyman_2",
                            "title": "Священнослужитель 2",
                        }
                    },
                ],
            },
        ],
    }
}

FORM_EXPANDED = expand_form(FORM, COMPONENTS_REGISTRY, FRAGMENTS_REGISTRY)
