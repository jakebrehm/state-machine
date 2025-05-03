from __future__ import annotations

import datetime as dt
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, NoReturn

from .errors import StateExecutionError
from .logger import Logger, NoLogger
from .structures import StateResult

if TYPE_CHECKING:
    from .structures import ExecutionResult
    from .types import DriverHistory, ExecutionAttemptResult


class State(ABC):
    max_retries: int = 0

    def __init__(self, logger: Logger | None = None) -> None:
        self.wall_times: list[float] = []
        self._attempt = 1
        self._logger = logger if logger is not None else NoLogger()

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

    def _execute(self, data: dict) -> StateResult | NoReturn:
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
            raise StateExecutionError(self, result)
        self._logger.log_state_success(self)
        return StateResult(
            data=result.data,
            wall_times=self.wall_times,
            next_state=result.next_state,
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


class StateMachine:
    def __init__(
        self,
        first_state: State,
        initial_data: dict | None = None,
        logger: Logger | None = None,
    ) -> None:
        self.current_state: State = first_state
        self.data = initial_data if initial_data is not None else {}
        self.logger = logger if logger is not None else NoLogger()
        self.history: DriverHistory = []
        self.logger.log_driver_init()

    def start(self) -> None:
        self.logger.log_driver_start()
        while self.current_state is not None:
            state = self.current_state(logger=self.logger)
            result = state._execute(data=self.data)
            self.data = result.data
            self.history.append(state)
            self.current_state = result.next_state
        self.logger.log_driver_finish()

    @property
    def wall_time(self) -> float:
        if not self.history:
            return 0.0
        return sum(i for item in self.history for i in item.wall_times)
