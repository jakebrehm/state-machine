from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Step
    from .structures import ExecutionResult

type DriverHistory = list[Step]

type OptionalStep = Step | None

type ExecutionAttemptResult = ExecutionResult | Exception
