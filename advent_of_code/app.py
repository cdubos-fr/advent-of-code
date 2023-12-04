import datetime
import importlib
import os

from typer import Typer

from advent_of_code.base import AdventOfCodeExecutor

app = Typer()


@app.command()
def exec(
    day: int,
    year: int = datetime.datetime.now().year,
    use_example: bool = False,
    part: int = 1,
    submit: bool = False,
) -> None:
    executor: type[AdventOfCodeExecutor] = getattr(
        importlib.import_module(f'advent_of_code.year_{year}.day_{day}.solve'), f'Day{day}',
    )
    with executor(use_example=use_example, part=part, submit=submit) as ex:
        result = ex.solve()
        ex.submition(result)


@app.command()
def init_day(
    day: int,
    year: int = datetime.datetime.now().year,
):
    folder = os.path.join(os.path.dirname(__file__), f"year_{year}")
    os.makedirs(os.path.join(folder, f'day_{day}'))
    with open(os.path.join(folder, 'solve.py'), mode='w') as f:
        f.write(
            "\n".join([
                "from advent_of_code.base import AdventOfCodeExecutor",
                "", ""
                    f"class Day{day}(AdventOfCodeExecutor):",
                    f"{' '*4}day = {day}",
                    f"{' '*4}year = {year}"
                    "",
                    f"{' '*4}def part_1(self) -> int:...",
                    f"{' '*4}def part_2(self) -> int:...",
                    f"{' '*4}@property\n{' '*4}def default_data_part_1(self)-> tuple[str, int]:...",
                    f"{' '*4}@property\n{' '*4}def default_data_part_2(self)-> tuple[str, int]:...",
            ]),
        )
