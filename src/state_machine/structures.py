from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Step
    from .types import DriverData


@dataclass
class ExecutionResult:
    data: DriverData
    next_step: Step | None


@dataclass
class StepResult:
    data: DriverData
    next_step: Step | None
    wall_times: list[float]
