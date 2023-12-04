import enum
import math
import re

import numpy as np

from advent_of_code.base import AdventOfCodeExecutor

NUM_PAT = re.compile(r'\d+')


class SchemaFormat(enum.IntEnum):
    NONE = 0
    DIGIT = 1
    SYMBOL = 2


def to_mask_table(schematic_seq: list[str]) -> np.ndarray:
    return np.array(
        [[char_to_int(c) for c in line] for line in schematic_seq],
    )


def char_to_int(schema_value: str) -> int:
    if schema_value.isdigit():
        return SchemaFormat.DIGIT
    elif schema_value == '.':
        return SchemaFormat.NONE
    return SchemaFormat.SYMBOL


class Day3(AdventOfCodeExecutor):
    day = 3
    year = 2023

    def part_1(self) -> int:
        schematic_table = self.data.splitlines()
        mask_schematic_table = to_mask_table(schematic_table)
        total = 0
        for raw_idx, line in enumerate(mask_schematic_table):
            if SchemaFormat.DIGIT not in line:
                continue
            raws = raw_idx-1 if raw_idx > 0 else 0
            pos = []
            latest = -1
            length = 0
            for column_idx, char in enumerate(line):
                if char == 1:
                    if latest == -1:
                        latest = column_idx
                    length += 1
                elif (
                    latest != -1 and
                    (char != 1 or raw_idx == len(schematic_table) - 1)
                ):
                    pos.append((latest, latest+length))
                    latest = -1
                    length = 0

            for start, end in pos:
                start_idx = start-1 if start > 0 else 0
                if SchemaFormat.SYMBOL in mask_schematic_table[raws:raw_idx+2, start_idx:end+1]:
                    total += int("".join(schematic_table[raw_idx][start:end]))
        return total

    def part_2(self) -> int:
        # Attempt: 29229353 too low
        schematic_table = self.data.splitlines()
        total = 0
        for raw_idx, line in enumerate(schematic_table):
            if '*' not in line:
                continue
            gear_pos = line.find('*')
            gear_number = []
            for delta_raw in range(-1, 2, 1):
                if raw_idx + delta_raw < 0:
                    continue
                for num in NUM_PAT.finditer(schematic_table[raw_idx + delta_raw]):
                    num_span = num.span()
                    if (gear_pos + 1 >= num_span[0] >= gear_pos - 1) or (
                        gear_pos - 1 <= num_span[1] - 1 <= gear_pos + 1
                    ) or (
                        num_span[0] <= gear_pos <= num_span[1] - 1
                    ):
                        gear_number.append(int(num.group()))
            if len(gear_number) == 2:
                total += math.prod(gear_number)
        return total

    @property
    def default_data_part_1(self) -> tuple[str, int]:
        return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$..*...
.664...598""", 4361

    @property
    def default_data_part_2(self) -> tuple[str, int]:
        return """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..""", 467835
