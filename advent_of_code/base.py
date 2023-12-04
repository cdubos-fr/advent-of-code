import os
from abc import ABC
from typing import Any
from typing import Self

import httpx
from bs4 import BeautifulSoup
from decouple import config


class AdventOfCodeExecutor(ABC):
    advent_uri: str = 'https://adventofcode.com'
    day: int
    year: int
    data: str
    part: int
    client = httpx.Client(cookies={"session": config("SESSION_ID")})

    def __init__(self, use_example: bool = False, part: int = 1, submit: bool = False) -> None:
        self.use_example = use_example
        self.part = part
        self.submit = submit

    def __enter__(self) -> Self:
        if not self.use_example:
            input_path = os.path.join(os.path.dirname(__file__), self.day_path, 'input.txt')
            if not os.path.exists(input_path):
                self.data = self.client.get(f'{self.day_uri}/input').text
                with open(input_path, mode='w') as f:
                    f.write(self.data)
            else:
                with open(input_path) as f:
                    self.data = f.read()
        else:
            self.data = self.default_data[0]
        return self

    def submition(self, result: Any) -> None:
        print("Solution:", result)
        if not self.use_example and self.submit:
            response = self.client.post(
                f'{self.day_uri}/answer',
                data={
                    "level": f"{self.part}",
                    "answer": result,
                },
                follow_redirects=True,
            )
            assert response.status_code == 200
            assert "That's not the right answer" not in response.text, (
                BeautifulSoup(response.text).find("article").find("p").text
            )

        elif self.use_example:
            assert result == self.default_data[
                1
            ], f"Invalid result, expecting: {self.default_data[1]}, found: {result}"

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self.client.close()

    def solve(self) -> Any:
        return getattr(self, f'part_{self.part}')()

    @property
    def default_data(self) -> tuple[str, Any]:
        return getattr(self, f'default_data_part_{self.part}')

    @property
    def day_uri(self) -> str:
        return f'{self.advent_uri}/{self.year}/day/{self.day}'

    @property
    def day_path(self) -> str:
        return os.path.join(f'year_{self.year}', f'day_{self.day}')
