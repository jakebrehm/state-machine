from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import State


@dataclass
class ExecutionResult:
    data: dict
    next_state: State | None


@dataclass
class StateResult:
    data: dict
    next_state: State | None
    wall_times: list[float]
