from __future__ import annotations

from typing import Dict, Tuple, Any, Optional

from staging.ids import VH_PREFIX  # щоб визначати «віртуальні» OID
from services.processor import ObjKeyT

# Репозиторії (використовуємо лише їх, без прямого доступу до db-API)
from repositories.person_repository import PersonRepository
from repositories.place_repository import PlaceRepository
from repositories.citation_repository import CitationRepository


class BaselineLoader:
    """
    Сервіс підвантаження baseline (поточного стану з БД) для набору ключів (kind, oid).
    Працює ТІЛЬКИ через репозиторії.
    """

    def __init__(self, db) -> None:
        self._person_repo = PersonRepository(db)
        self._place_repo = PlaceRepository(db)
        self._citation_repo = CitationRepository(db)

    # --- публічне API ---

    def load(self, after_map: Dict[ObjKeyT, Dict[str, Any]]) -> Dict[ObjKeyT, Dict[str, Any]]:
        """
        Пробігаємось по ключах із after_map і, для кожного реального OID (не VH:),
        витягуємо поточний стан з БД → серіалізуємо у HV-JSON (dict).
        Якщо об’єкта немає — не додаємо до baseline (такий буде «new»).
        """
        baseline: Dict[ObjKeyT, Dict[str, Any]] = {}

        for (kind, oid) in after_map.keys():
            # Пропускаємо віртуальні об'єкти — їх зараз у БД немає за визначенням.
            if oid.startswith(VH_PREFIX):
                continue

            payload = self._load_one(kind, oid)
            if payload is not None:
                baseline[(kind, oid)] = payload

        return baseline

    # --- внутрішнє ---

    def _load_one(self, kind: str, handle: str) -> Optional[Dict[str, Any]]:
        """
        Витягнути один об’єкт з БД через відповідний репозиторій і серіалізувати.
        Повертає dict (HV-JSON) або None, якщо об’єкт відсутній.
        """
        kind_u = kind.strip().lower()

        if kind_u == "person":
            obj = self._person_repo.get_by_handle(handle)
            return self._serialize_person(obj) if obj else None

        if kind_u == "place":
            obj = self._place_repo.get_by_handle(handle)
            return self._serialize_place(obj) if obj else None

        if kind_u == "citation":
            obj = self._citation_repo.get_by_handle(handle)
            return self._serialize_citation(obj) if obj else None

        # Невідомий тип — ігноруємо. За потреби додай свої репозиторії/серіалізатори.
        return None

    # --- серіалізація до «базового» HV-JSON ---
    # Примітка: ці серіалізатори мінімальні. За бажанням розширюй
    # їх до повного канонічного HV-представлення, щоб diff був точніший.

    def _serialize_person(self, person) -> Dict[str, Any]:
        # Мінімально: ідентифікатори. Розширюй за доменною моделлю.
        return {
            "handle": getattr(person, "handle", None) or getattr(person, "get_handle", lambda: None)(),
            "gramps_id": getattr(person, "gramps_id", None) or getattr(person, "get_gramps_id", lambda: None)(),
        }

    def _serialize_place(self, place) -> Dict[str, Any]:
        return {
            "handle": getattr(place, "handle", None) or getattr(place, "get_handle", lambda: None)(),
            "gramps_id": getattr(place, "gramps_id", None) or getattr(place, "get_gramps_id", lambda: None)(),
        }

    def _serialize_citation(self, citation) -> Dict[str, Any]:
        return {
            "handle": getattr(citation, "handle", None) or getattr(citation, "get_handle", lambda: None)(),
            "gramps_id": getattr(citation, "gramps_id", None) or getattr(citation, "get_gramps_id", lambda: None)(),
        }