from enum import Enum
from typing import Any
from typing import Self
from typing import Optional
from typer import Typer
from typer import Option
import httpx
from abc import ABC
from abc import abstractmethod
import importlib
from decouple import config
import os
import datetime

app = Typer()


class ModeType(str, Enum):
    full = 'full'
    test = 'test'


@app.command()
def exec(day: int, mode: ModeType = ModeType.full, part: int = 1) -> None:
    executor: AdventOfCodeExecutor = getattr(importlib.import_module(f'advent_of_code_2023.day_{day}'), f'Day{day}')
    with executor(mode=mode, part=part) as ex:
        ex.solve()


@app.command()
def init_day(day: int, folder: str, year: Optional[int] = None):
    with open(os.path.join(folder, f'day_{day}.py'), mode='w') as f:
        f.write("\n".join([
                "from advent_of_code import AdventOfCodeExecutor",
                "", ""
                f"class Day{day}(AdventOfCodeExecutor):",
                f"{' '*4}day = {day}",
                f"{' '*4}year = {year if year is not None else datetime.datetime.now().year}"
                "",
                f"{' '*4}def part_1(self) -> int:...",
                f"{' '*4}def part_2(self) -> int:...",
                f"{' '*4}@property\n{' '*4}def default_data_part_1(self)-> tuple[str, int]:...",
                f"{' '*4}@property\n{' '*4}def default_data_part_2(self)-> tuple[str, int]:...",

            ])
        )





class AdventOfCodeExecutor(ABC):
    advent_uri: str = 'https://adventofcode.com'
    day: int
    year: int
    data: str
    mode: ModeType
    part: int
    client = httpx.Client(cookies={"session": config("SESSION_ID")})

    def __init__(self, mode: ModeType = ModeType.full, part: int = 1) -> None:
        self.mode = mode
        self.part = part

    def __enter__(self) -> Self:
        if self.mode == 'full':
            self.data = self.client.get(f'{self.day_uri}/input').text
        else:
            self.data = self.default_data[0]
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        result = self.solve()
        print('Solution:', result)
        if self.mode == ModeType.full:
            response = self.client.post(f'{self.day_uri}/answer', data={"level": f"{self.part}", "answer": result}, follow_redirects=True)
            assert response.status_code == 200
            assert "That's not the right answer" not in response.text, response.text
        else:
            assert result == self.default_data[1], f"Invalid result, expecting: {self.default_data[1]}, found: {result}"
        self.client.close()

    def solve(self) -> Any:
        return getattr(self, f'part_{self.part}')()

    @property
    def default_data(self) -> tuple[str, Any]:
        return getattr(self, f'default_data_part_{self.part}')

    @property
    def day_uri(self) -> int:
        return f'{self.advent_uri}/{self.year}/day/{self.day}'
