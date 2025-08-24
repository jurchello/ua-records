from typing import Any

USER_DATA: str

class _Locale:
    def get_addon_translator(self, path: str) -> Any: ...
    @property
    def translation(self) -> Any: ...

GRAMPS_LOCALE: _Locale