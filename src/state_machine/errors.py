from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from .core import Step


class StepExecutionError(Exception):
    def __init__(self, step: Step, exception: Exception) -> NoReturn:
        if step.max_retries > 0:
            message = f"exceeded {step.max_retries} retries"
        else:
            message = "failed"
        message = f"Execution of step {step.name} {message}"
        super().__init__(message)
        self.exception: Exception = exception
