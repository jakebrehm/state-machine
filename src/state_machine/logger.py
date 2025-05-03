from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Step


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
    def log_attempt_start(self, step: Step) -> None:
        pass

    @abstractmethod
    def log_attempt_success(self, step: Step) -> None:
        pass

    @abstractmethod
    def log_attempt_failure(self, step: Step, exception: Exception) -> None:
        pass

    @abstractmethod
    def log_step_success(self, step: Step) -> None:
        pass


class NoLogger(Logger):
    def log_driver_init(self) -> None:
        pass

    def log_driver_start(self) -> None:
        pass

    def log_driver_finish(self) -> None:
        pass

    def log_attempt_start(self, step: Step) -> None:
        pass

    def log_attempt_success(self, step: Step) -> None:
        pass

    def log_attempt_failure(self, step: Step, exception: Exception) -> None:
        pass

    def log_step_success(self, step: Step) -> None:
        pass


class ConsoleLogger(Logger):
    def log_driver_init(self) -> None:
        print("Driver successfully initialized.")

    def log_driver_start(self) -> None:
        print("Driver execution starting...")

    def log_driver_finish(self) -> None:
        print("Driver execution complete.")

    def log_attempt_start(self, step: Step) -> None:
        print(
            f"Executing step {step.name} "
            f"(attempt {step.attempt}/{step.max_attempts})..."
        )

    def log_attempt_success(self, step: Step) -> None:
        print(
            f"Successful attempt of step {step.name} "
            f"({step._most_recent_wall_time():0.2f} ms)."
        )

    def log_attempt_failure(self, step: Step, exception: Exception) -> None:
        exception_type = exception.__class__.__name__
        print(
            f"Encountered {exception_type} attempting step {step.name} "
            f"({step._most_recent_wall_time():0.2f} ms)."
        )

    def log_step_success(self, step: Step) -> None:
        print(f"Finished step {step.name} ({step.wall_time:0.2f} ms).")
