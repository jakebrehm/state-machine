"""
A test module for the state machine package.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src"))
)
import random
import time
from typing import NoReturn

from state_machine import Driver, ExecutionResult, Step


class Extract(Step):
    name = "Extract"
    status = "Extracting data from API"

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 1
        time.sleep(1.45)
        return ExecutionResult(data=data, next_step=Transform)


class Transform(Step):
    name = "Transform"
    status = "Applying transformations to data"
    max_retries = 1

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 2
        self.randomly_fail()
        time.sleep(0.10)
        return ExecutionResult(data=data, next_step=Load)

    def randomly_fail(self, chance=0.5) -> None | NoReturn:
        random_value = random.random()
        print(f"Hit random value {random_value}")
        if random_value <= chance:
            raise ValueError("Test error")


class Load(Step):
    name = "Load"
    status = "Loading data into database"

    def execute(self, data: dict) -> ExecutionResult:
        data["value"] = 3
        time.sleep(0.19)
        return ExecutionResult(data=data, next_step=None)


def main() -> None:
    driver = Driver(
        first_step=Extract,
        initial_data={"initial": True, "value": 0},
    )
    driver.start()
    print()
    print(driver.data)
    print(driver.history)
    print(driver.wall_time)
    for step in driver.history:
        print(step.max_retries)
        print(step.wall_time)
        print(step.wall_times)


if __name__ == "__main__":
    main()
