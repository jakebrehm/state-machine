from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

if TYPE_CHECKING:
    from .core import State


class StateExecutionError(Exception):
    def __init__(self, state: State, exception: Exception) -> NoReturn:
        if state.max_retries > 0:
            message = f"exceeded {state.max_retries} retries"
        else:
            message = "failed"
        message = f"Execution of state {state.name} {message}"
        super().__init__(message)
        self.exception: Exception = exception
