from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import State


class Logger(ABC):
    @abstractmethod
    def log_driver_init(self) -> None:
        pass

    @abstractmethod
    def log_driver_start(self) -> None:
        pass

    @abstractmethod
    def log_driver_finish(self) -> None:
        pass

    @abstractmethod
    def log_attempt_start(self, state: State) -> None:
        pass

    @abstractmethod
    def log_attempt_success(self, state: State) -> None:
        pass

    @abstractmethod
    def log_attempt_failure(self, state: State, exception: Exception) -> None:
        pass

    @abstractmethod
    def log_state_success(self, state: State) -> None:
        pass


class NoLogger(Logger):
    def log_driver_init(self) -> None:
        pass

    def log_driver_start(self) -> None:
        pass

    def log_driver_finish(self) -> None:
        pass

    def log_attempt_start(self, state: State) -> None:
        pass

    def log_attempt_success(self, state: State) -> None:
        pass

    def log_attempt_failure(self, state: State, exception: Exception) -> None:
        pass

    def log_state_success(self, state: State) -> None:
        pass


class ConsoleLogger(Logger):
    def log_driver_init(self) -> None:
        print("Driver successfully initialized.")

    def log_driver_start(self) -> None:
        print("Driver execution starting...")

    def log_driver_finish(self) -> None:
        print("Driver execution complete.")

    def log_attempt_start(self, state: State) -> None:
        print(
            f"Executing state {state.name} "
            f"(attempt {state.attempt}/{state.max_attempts})..."
        )

    def log_attempt_success(self, state: State) -> None:
        print(
            f"Successful attempt of state {state.name} "
            f"({state._most_recent_wall_time():0.2f} ms)."
        )

    def log_attempt_failure(self, state: State, exception: Exception) -> None:
        exception_type = exception.__class__.__name__
        print(
            f"Encountered {exception_type} attempting state {state.name} "
            f"({state._most_recent_wall_time():0.2f} ms)."
        )

    def log_state_success(self, state: State) -> None:
        print(f"Finished state {state.name} ({state.wall_time:0.2f} ms).")
