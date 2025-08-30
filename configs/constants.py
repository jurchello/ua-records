DEFAULT_PLACE_ID_1 = "P00323"
DEFAULT_PLACE_ID_2 = "P00323"
DEFAULT_PLACE_ID_3 = "P00323"
DEFAULT_CITATION_ID = "C06917"
DEFAULT_PERSON_ID = "I10376"

# Gender codes for database
GENDER_CODE_MAN = "M"
GENDER_CODE_WOMAN = "F"
GENDER_CODE_UNKNOWN = "U"

# Gender display names for UI
GENDER_MAN = "Чоловік"
GENDER_WOMAN = "Жінка"
GENDER_UNKNOWN = "Невідомо"

ALL_GENDER_CODES = [GENDER_CODE_MAN, GENDER_CODE_WOMAN, GENDER_CODE_UNKNOWN]
ALL_GENDERS = [GENDER_MAN, GENDER_WOMAN, GENDER_UNKNOWN]

_label_mode_state = {"mode": "middle", "subs": []}
_tab_mode_state = {"mode": "middle", "subs": []}


def get_label_mode() -> str:
    return _label_mode_state["mode"]


def set_label_mode(mode: str) -> None:
    _label_mode_state["mode"] = (mode or "middle").lower()
    for cb in list(_label_mode_state["subs"]):
        try:
            cb(_label_mode_state["mode"])
        except Exception:
            pass


def subscribe_label_mode(cb):
    _label_mode_state["subs"].append(cb)
    return cb


def unsubscribe_label_mode(cb):
    try:
        _label_mode_state["subs"].remove(cb)
    except ValueError:
        pass


def get_tab_mode() -> str:
    return _tab_mode_state["mode"]


def set_tab_mode(mode: str) -> None:
    _tab_mode_state["mode"] = (mode or "middle").lower()
    for cb in list(_tab_mode_state["subs"]):
        try:
            cb(_tab_mode_state["mode"])
        except Exception:
            pass


def subscribe_tab_mode(cb):
    _tab_mode_state["subs"].append(cb)
    return cb


def unsubscribe_tab_mode(cb):
    try:
        _tab_mode_state["subs"].remove(cb)
    except ValueError:
        pass


def sync_label_mode_from_density():
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        density = get_settings_manager().get_form_density()
        if density == "compact":
            set_label_mode("short")
        elif density == "spacious":
            set_label_mode("long")
        else:
            set_label_mode("middle")
    except Exception:
        set_label_mode("middle")


def sync_tab_mode_from_density():
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        tab_density = get_settings_manager().get_tab_density()
        if tab_density == "compact":
            set_tab_mode("short")
        elif tab_density == "spacious":
            set_tab_mode("long")
        else:
            set_tab_mode("middle")
    except Exception:
        set_tab_mode("middle")


sync_label_mode_from_density()
sync_tab_mode_from_density()

MAN_MILITARY_RANKS = [
    "Безстроково-відпускний солдат",
    "Білетний солдат",
    "Відставний капрал",
    "Відставний рядовий",
    "Відставний солдат",
    "Відставний унтер-офіцер",
    "Військова присяга",
    "Військова служба",
    "Військовополонений",
    "Вільно-відпускний",
    "Єфрейтор",
    "Запасний єфрейтор",
    "Запасний рядовий",
    "Запасний солдат",
    "Запасний унтер-офіцер",
    "Зауряд-чиновник (чиновник військового часу)",
    "Завершення військової служби",
    "Звільнений у запас канонір",
    "Зник безвісти",
    "Іменний список частини",
    "Інвалідний солдат",
    "Інвалідний унтер-офіцер",
    "Інвалідної команди рядовий",
    "Інвалідної команди рядовий солдат",
    "Інвалідної команди солдат",
    "Капітан",
    "Картотека моряків",
    "Командир взводу",
    "Контужений",
    'Медаль "За бойові заслуги"',
    'Медаль "За взяття Кенігсберга"',
    'Медаль "За оборону Кавказу"',
    'Медаль "За оборону Ленінграда"',
    'Медаль "За перемогу над Японією"',
    'Медаль "За відвагу"',
    "Медаль «За оборону Радянського Заполяр'я»",
    "Медаль «За перемогу над Німеччиною у Великій Вітчизняній війні 1941–1945 рр.»",
    "Нагороди",
    "Наказ про виключення зі списків",
    "Обліково-послужна картотека",
    "Орден",
    "Орден Вітчизняної війни І ступеня",
    "Орден Вітчизняної війни ІІ ступеня",
    "Орден Слави III ступеня",
    "Орден Червоного Прапора",
    "Орден Червоної Зірки",
    "По білету відпущений рядовий",
    "Поіменний список військової частини",
    "Поранення",
    "Побілетний кананір",
    "Побілетний солдат",
    "Побілетний унтер-офіцер",
    "Поручик",
    "Призов",
    "Призов на військову службу",
    "Прапорщик",
    "Рекрут",
    "Рядовий",
    "Рядовий солдат",
    "Служив у будівельних військах",
    "Солдат",
    "Тимчасово-відпускний солдат",
    "Унтер-офіцер",
    "Унтер-офіцер по безстроковому білету",
    "Участь у війні",
    "Хвороба",
]

WOMAN_MILITARY_RANKS = [
    "Солдатка",
    "Дружина військового",
    "Дочка військового",
    "Вдова військового",
    "Дружина солдата",
    "Дочка солдата",
    "Вдова солдата",
    "Дружина рядового",
    "Дочка рядового",
    "Вдова рядового",
    "Дружина відставного солдата",
    "Дочка відставного солдата",
    "Вдова відставного солдата",
    "Дружина запасного солдата",
    "Дочка запасного солдата",
    "Вдова запасного солдата",
    "Дружина інвалідного солдата",
    "Дочка інвалідного солдата",
    "Вдова інвалідного солдата",
    "Дружина побілетного солдата",
    "Дочка побілетного солдата",
    "Вдова побілетного солдата",
    "Дружина тимчасово-відпускного солдата",
    "Дочка тимчасово-відпускного солдата",
    "Вдова тимчасово-відпускного солдата",
    "Дружина безстроково-відпускного солдата",
    "Дочка безстроково-відпускного солдата",
    "Вдова безстроково-відпускного солдата",
    "Дружина єфрейтора",
    "Дочка єфрейтора",
    "Вдова єфрейтора",
    "Дружина запасного єфрейтора",
    "Дочка запасного єфрейтора",
    "Вдова запасного єфрейтора",
    "Дружина унтер-офіцера",
    "Дочка унтер-офіцера",
    "Вдова унтер-офіцера",
    "Дружина відставного унтер-офіцера",
    "Дочка відставного унтер-офіцера",
    "Вдова відставного унтер-офіцера",
    "Дружина капрала",
    "Дочка капрала",
    "Вдова капрала",
    "Дружина капітана",
    "Дочка капітана",
    "Вдова капітана",
    "Дружина прапорщика",
    "Дочка прапорщика",
    "Вдова прапорщика",
    "Дружина поручика",
    "Дочка поручика",
    "Вдова поручика",
    "Дружина зауряд-чиновника",
    "Дочка зауряд-чиновника",
    "Вдова зауряд-чиновника",
    "Дружина каноніра",
    "Дочка каноніра",
    "Вдова каноніра",
    "Дружина звільненого у запас каноніра",
    "Дочка звільненого у запас каноніра",
    "Вдова звільненого у запас каноніра",
]

NEW_PERSON_TAGS = [
    "Bilovody (research direction)",
    "Allow To Publish",
    "Residence actualized",
]
EXISTING_PERSON_TAGS = ["Bilovody (research direction)", "Allow To Publish"]
NEW_EVENT_TAGS = ["Allow To Publish"]
NEW_CITATION_TAGS = ["Allow To Publish"]

CLERGY_OCCUPATIONS = ["Священник", "Диякон", "Ієрей"]

DENSITY_SETTINGS = {
    "compact": {
        "grid_margin": 10,
        "grid_row_spacing": 3,
        "grid_column_spacing": 6,
        "frame_margin_top": 1,
        "frame_margin_bottom": 1,
        "frame_margin_start": 2,
        "frame_margin_end": 2,
        "vbox_spacing": 2,
        "vbox_margin_top": 2,
        "vbox_margin_bottom": 2,
        "vbox_margin_start": 6,
        "vbox_margin_end": 6,
        "row_grid_spacing": 3,
        "button_margin_top": 10,
    },
    "normal": {
        "grid_margin": 20,
        "grid_row_spacing": 10,
        "grid_column_spacing": 10,
        "frame_margin_top": 2,
        "frame_margin_bottom": 2,
        "frame_margin_start": 3,
        "frame_margin_end": 3,
        "vbox_spacing": 4,
        "vbox_margin_top": 4,
        "vbox_margin_bottom": 4,
        "vbox_margin_start": 10,
        "vbox_margin_end": 10,
        "row_grid_spacing": 4,
        "button_margin_top": 20,
    },
    "spacious": {
        "grid_margin": 30,
        "grid_row_spacing": 15,
        "grid_column_spacing": 15,
        "frame_margin_top": 4,
        "frame_margin_bottom": 4,
        "frame_margin_start": 5,
        "frame_margin_end": 5,
        "vbox_spacing": 8,
        "vbox_margin_top": 8,
        "vbox_margin_bottom": 8,
        "vbox_margin_start": 15,
        "vbox_margin_end": 15,
        "row_grid_spacing": 8,
        "button_margin_top": 30,
    },
}

# Default text length for fallback DND fields
DEFAULT_TEXT_LENGTH = 30


def get_person_name_length() -> int:
    """Get max person name display length from config."""
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        return get_settings_manager().get_person_name_length()
    except Exception:
        return get_default_text_length()


def get_place_title_length() -> int:
    """Get max place title display length from config."""
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        return get_settings_manager().get_place_title_length()
    except Exception:
        return get_default_text_length()


def get_citation_text_length() -> int:
    """Get max citation text display length from config."""
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        return get_settings_manager().get_citation_text_length()
    except Exception:
        return get_default_text_length()


def get_default_text_length() -> int:
    """Get default text field length - uses person length as primary fallback."""
    try:
        # Use person name length as primary fallback
        return get_person_name_length()
    except Exception:
        return DEFAULT_TEXT_LENGTH


COLOR_EMPTY_DND = "#eaeaea"
COLOR_FILLED_DND = "#dfffce"
COLOR_EMPTY_INPUT = "#ffffff"
COLOR_FILLED_INPUT = "#dfffce"


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


def get_dnd_default() -> dict:

    return {
        "placeholder": "Перетягни сюди...",
        "width": get_default_text_length(),
    }


FORM_WINDOW_MODE = "transient"  # "detached" | "transient" | "modal"

FORM_WINDOW_KEEP_ABOVE = False  # True/False

FORM_WINDOW_TYPE_HINT = "dialog"

FORM_WINDOW_SKIP_TASKBAR = False
FORM_WINDOW_SKIP_PAGER = False


TAB_HOVER_SWITCH_DELAY_MS = 100
TAB_HOVER_SWITCH_THROTTLE_MS = 120
TAB_HOVER_SLOP_PX = 16


FORM_WINDOW_REMEMBER_POSITION: bool = True
FORM_WINDOW_ANCHOR: str = "topleft"
FORM_WINDOW_PER_FORM: bool = True


FORM_WINDOW_ALLOW_VSCROLL: bool = False

FORM_WINDOW_MAX_HEIGHT: int = -1
