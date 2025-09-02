from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Any, List
from abc import ABC, abstractmethod

from staging.graph import AfterGraph
from staging.ops import build_change_ops, ChangeOp
from staging.apply import apply_ops
from staging.validate import validate_hv_graph

ObjKeyT = Tuple[str, str]  # (kind, oid)


@dataclass
class StagingResult:
    """Результат стадіювання (порівняння baseline ↔ after)."""
    baseline: Dict[ObjKeyT, Dict[str, Any]]
    after: Dict[ObjKeyT, Dict[str, Any]]
    ops: List[ChangeOp]
    errors: List[str]   # структурні помилки HV-графа (VH-посилання тощо)


class ProcessorBase(ABC):
    """
    Базовий процесор для сценарію:
    FormState → (build after) → diff з baseline → UI вибір → commit.
    """

    def __init__(self, work_context) -> None:
        # work_context має: form_state, db, identity_map
        self.ctx = work_context

    @abstractmethod
    def _build_after_graph(self) -> AfterGraph:
        """Побудувати цільовий стан (after) із FormState."""
        raise NotImplementedError

    @abstractmethod
    def _load_baseline(self, after_map: Dict[ObjKeyT, Dict[str, Any]]) -> Dict[ObjKeyT, Dict[str, Any]]:
        """Підвантажити поточний стан із БД для ключів, що фігурують в after_map."""
        raise NotImplementedError

    @abstractmethod
    def commit(self, accepted_after: Dict[ObjKeyT, Dict[str, Any]]) -> None:
        """Виконати запис до БД за погодженим станом."""
        raise NotImplementedError

    # --- Головні кроки пайплайну ---

    def stage(self) -> StagingResult:
        """
        Порахувати різницю між baseline (БД) та after (цільовий стан).
        Записів у БД не виконує.
        """
        after_graph = self._build_after_graph()
        after_map = after_graph.as_map()

        errors = validate_hv_graph(after_map)
        baseline = self._load_baseline(after_map)
        ops = build_change_ops(baseline, after_map)

        return StagingResult(baseline=baseline, after=after_map, ops=ops, errors=errors)

    def accept_selection(self, staging: StagingResult, accepted_ids: List[str]) -> Dict[ObjKeyT, Dict[str, Any]]:
        """Застосувати лише обрані користувачем зміни до baseline → отримаємо accepted_after."""
        return apply_ops(staging.baseline, staging.ops, accepted_ids)

    def run(self, accept_all: bool = False) -> StagingResult:
        """
        Зручний шорткат:
        - завжди рахує staging (baseline/after/ops/errors) і повертає його;
        - якщо accept_all=True і немає помилок HV-графа — комітить усі зміни.
        """
        staging = self.stage()

        # Якщо є структурні помилки HV-графа — не комітимо, повертаємо для UI
        if staging.errors:
            return staging

        if accept_all:
            accepted_ids = [op.id for op in staging.ops]
            accepted_after = self.accept_selection(staging, accepted_ids)
            self.commit(accepted_after)

        return staging