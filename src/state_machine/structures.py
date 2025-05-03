from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Step


@dataclass
class ExecutionResult:
    data: dict
    next_step: Step | None


@dataclass
class StepResult:
    data: dict
    next_step: Step | None
    wall_times: list[float]
