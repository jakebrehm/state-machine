from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import State
    from .structures import ExecutionResult

type DriverHistory = list[State]

type ExecutionAttemptResult = ExecutionResult | Exception
