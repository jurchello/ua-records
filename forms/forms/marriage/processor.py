from __future__ import annotations

from typing import Dict, Tuple, Any, List

from services.processor import ProcessorBase, ObjKeyT, StagingResult
from staging.baseline_loader import BaselineLoader
from staging.graph import AfterGraph
from staging.ids import vh  # для створення віртуальних OID (VH:...)
# from staging.ids import h  # знадобиться, якщо треба явно маркувати «реальні» хендли


class MarriageProcessor(ProcessorBase):
    """
    Процесор для форми «Шлюб». Тут ти перетворюєш FormState → HV-JSON (AfterGraph),
    а також визначаєш, як виконувати commit погоджених змін.
    """

    # --- побудова цільового стану ---

    def _build_after_graph(self) -> AfterGraph:
        g = AfterGraph()

        fs = self.ctx.form_state
        im = self.ctx.identity_map
        db = self.ctx.db

        # === ПРИКЛАДИ (заглушки). Замінюй на реальне доменне перетворення. ===
        #
        # 1) Якщо у FormState уже є вибрані з БД об'єкти (цитата/місце/персони),
        #    їх OID будуть реальними handle → kind="Citation"/"Place"/"Person".
        #
        # 2) Якщо потрібно створити новий об’єкт — дай йому віртуальний OID (VH:...).
        #
        # Нижче кілька шаблонів:

        # Приклад: існуюча цитата як об’єкт у FormState (замінити на твою API)
        try:
            citation_obj = fs.get_object("common_box", "citation")
        except Exception:
            citation_obj = None

        if citation_obj:
            # Реальний об'єкт: припускаємо, що у payload ти формуєш поля, які хочеш зберегти.
            # Оскільки baseline ми серіалізуємо мінімально, різниця піде в "set"/"replace".
            handle = getattr(citation_obj, "handle", None) or getattr(citation_obj, "get_handle", lambda: None)()
            if handle:
                g.put(key=_ObjKey("Citation", handle), data={
                    # TODO: наповни канонічні поля цитати
                })

        # Приклад: створити нову Citation (віртуальна)
        # new_cit_vh = vh("new_citation")
        # g.put(key=_ObjKey("Citation", str(new_cit_vh)), data={
        #     "title": "Нова цитата",
        #     ...
        # })

        # Аналогічно для осіб / місця шлюбу тощо.

        return g

    # --- baseline через репозиторії ---

    def _load_baseline(self, after_map: Dict[ObjKeyT, Dict[str, Any]]) -> Dict[ObjKeyT, Dict[str, Any]]:
        loader = BaselineLoader(self.ctx.db)
        return loader.load(after_map)

    # --- commit погоджених змін ---

    def commit(self, accepted_after: Dict[ObjKeyT, Dict[str, Any]]) -> None:
        """
        Тут — перетворення HV-JSON → конкретні виклики репозиторіїв (create/update).
        Рекомендації:
          1) Побудуй залежності VH→VH і виконай топологічне створення.
          2) На кожне VH створюй об’єкт у БД і зберігай відповідність {vh -> real_handle}.
          3) Після створення заміни всі VH у payload на реальні handle.
          4) Для реальних handle — онови поля (commit).
          5) Все загорни в одну транзакцію, якщо це можливо на рівні gateway.
        """
        # Навмисно порожньо: цей шар — про стадіювання. Запис реалізуєш відповідно до своєї доменної моделі.
        return


# Допоміжний легковаговий ключ для AfterGraph.put (щоб не тягнути зовнішні типи)
class _ObjKey:
    __slots__ = ("kind", "oid")

    def __init__(self, kind: str, oid: str) -> None:
        self.kind = kind
        self.oid = oid