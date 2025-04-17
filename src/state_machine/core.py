from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NoReturn

from .structures import StepResult

if TYPE_CHECKING:
    from .errors import StepExecutionError
    from .structures import ExecutionResult
    from .types import DriverHistory, ExecutionAttemptResult


class StepLogger:
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

    def log_attempt_failure(
        self,
        step: Step,
        exception: Exception,
    ) -> None:
        exception_type = exception.__class__.__name__
        print(
            f"Encountered {exception_type} attempting step {step.name} "
            f"({step._most_recent_wall_time():0.2f} ms)."
        )

    def log_overall_success(self, step: Step) -> None:
        print(f"Finished step {step.name} ({step.wall_time:0.2f} ms).")


class Step(ABC):
    max_retries: int = 0

    def __init__(self, logger: StepLogger | None = None) -> None:
        self.wall_times: list[float] = []
        self._attempt = 1
        self._logger = logger if logger is not None else StepLogger()

    @property
    @abstractmethod
    def name(self) -> None:
        pass

    @property
    @abstractmethod
    def status(self) -> None:
        pass

    @property
    def attempt(self) -> int:
        return self._attempt

    @property
    def max_attempts(self) -> int:
        return 1 + max(0, self.max_retries)

    @property
    def wall_time(self) -> float:
        if not self.wall_times:
            return 0.0
        return sum(wall_time for wall_time in self.wall_times)

    @abstractmethod
    def execute(self, data: dict) -> ExecutionResult:
        pass

    def _execute(self, data: dict) -> StepResult | NoReturn:
        while self._attempt <= self.max_attempts:
            self._logger.log_attempt_start(self)
            result = self._execute_attempt(data=data)
            if isinstance(result, Exception):
                self._logger.log_attempt_failure(self, result)
            else:
                self._logger.log_attempt_success(self)
                break
            self._attempt += 1
        else:
            raise StepExecutionError(self, result)
        self._logger.log_overall_success(self)
        return StepResult(
            data=result.data,
            wall_times=self.wall_times,
            next_step=result.next_step,
        )

    def _execute_attempt(self, data: dict) -> ExecutionAttemptResult:
        start_time = dt.datetime.now()
        try:
            result: ExecutionAttemptResult = self.execute(data=data)
        except Exception as e:
            result: ExecutionAttemptResult = e
        end_time = dt.datetime.now()
        wall_time = (end_time - start_time).total_seconds() * 1000
        self.wall_times.append(wall_time)
        return result

    def _most_recent_wall_time(self) -> float:
        return self.wall_times[-1] if self.wall_times else 0.0

    def __str__(self) -> str:
        class_name = self.__class__.__name__
        max_retries = self.max_retries
        return f"{class_name}({max_retries=})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


class Driver:
    def __init__(
        self,
        first_step: Step,
        initial_data: dict | None = None,
    ) -> None:
        self.current_step = first_step
        self.data = initial_data if initial_data is not None else {}
        self.history: DriverHistory = []

    def start(self) -> None:
        while self.current_step is not None:
            step = self.current_step()
            result = step._execute(data=self.data)
            self.data = result.data
            self.history.append(step)
            self.current_step = result.next_step
        self._log_success()

    @property
    def wall_time(self) -> float:
        if not self.history:
            return 0.0
        return sum(i for item in self.history for i in item.wall_times)

    def _log_success(self) -> None:
        print("Driver execution complete.")
