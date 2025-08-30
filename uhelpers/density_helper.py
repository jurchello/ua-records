from configs.constants import DENSITY_SETTINGS


def get_density_settings() -> dict[str, int]:
    try:
        from settings.settings_manager import get_settings_manager  # pylint: disable=import-outside-toplevel

        density = get_settings_manager().get_form_density()
    except Exception:
        density = "compact"  # fallback default
    return DENSITY_SETTINGS.get(density, DENSITY_SETTINGS["normal"])
