import functools
import operator as op
import re

from advent_of_code.base import AdventOfCodeExecutor

COLORS_PAT = {
    color: re.compile(rf'(?P<{color}>\d+) {color}')
    for color in ("red", "green", "blue")
}


class Day2(AdventOfCodeExecutor):
    day = 2
    year = 2023

    def part_1(self) -> int:
        # 12 red, 13 green, 14 blue
        expected = {
            "red": 12,
            "green": 13,
            "blue": 14,
        }
        total = 0
        for game in self.data.splitlines():
            game_id, _, game_data = game.partition(":")
            for turn in game_data.split(";"):
                if any(
                    expected[value.split()[-1]] < int(value.split()[0])
                    for value in turn.split(",")
                ):
                    break
            else:
                total += int(game_id.split()[-1])
        return total

    def part_2(self) -> int:
        total = 0
        for game in self.data.splitlines():
            *_, game_data = game.partition(":")
            total += functools.reduce(
                op.mul,
                [
                    max(int(cubes_number) for cubes_number in color_pat.findall(game_data))
                    for color_pat in COLORS_PAT.values()
                ],
            )
        return total

    @property
    def default_data_part_1(self) -> tuple[str, int]:
        return (
            """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 8,
        )

    @property
    def default_data_part_2(self) -> tuple[str, int]:
        return """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", 2286
