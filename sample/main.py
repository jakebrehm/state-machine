"""
A sample module for the state machine package.

Showcases how the package can be used to implement an ETL pipeline, where states
can fail and have multiple attempts.
"""

import random
import time
from typing import NoReturn

from state_machine import ConsoleLogger, ExecutionResult, State, StateMachine


class Extract(State):
    name = "Extract"
    status = "Extracting data from API"

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 1
        time.sleep(1.45)
        return ExecutionResult(data=data, next_state=Transform)


class Transform(State):
    name = "Transform"
    status = "Applying transformations to data"
    max_retries = 3

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 2
        self.randomly_fail()
        time.sleep(0.10)
        return ExecutionResult(data=data, next_state=Load)

    def randomly_fail(self, chance=0.5) -> None | NoReturn:
        random_value = random.random()
        print(f"Hit random value {random_value}")
        if random_value <= chance:
            raise ValueError("Test error")


class Load(State):
    name = "Load"
    status = "Loading data into database"

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 3
        time.sleep(0.19)
        return ExecutionResult(data=data, next_state=None)


def main() -> None:
    machine = StateMachine(
        first_state=Extract,
        initial_data={"initial": True, "value": 0},
        logger=ConsoleLogger(),
    )
    machine.start()


if __name__ == "__main__":
    main()
