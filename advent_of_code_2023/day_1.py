from advent_of_code import AdventOfCodeExecutor
from operator import itemgetter
import itertools


getitem = itemgetter(0, -1)

DIGITS = {
    'one': "1",
    'two': "2",
    'three': "3",
    'four': "4",
    'five': "5",
    'six': "6",
    'seven': "7",
    'eight': "8",
    'nine': "9",
}


class Day1(AdventOfCodeExecutor):
    day = 1
    year = 2023

    def part_1(self) -> int:
        return sum(
            int("".join(getitem([value for value in lines if value.isdigit()])))
            for lines in self.data.splitlines()
        )

    def part_2(self)-> int:
        total = 0
        for line in self.data.splitlines():
            left_pos = (len(line) +1, len(line) +1)
            right_pos = (-1, -1)
            for digit in itertools.chain(DIGITS, DIGITS.values()):
                pos = line.find(digit), DIGITS.get(digit, digit)
                rpos = line.rfind(digit), DIGITS.get(digit, digit)
                if pos[0] > -1 and left_pos[0] > pos[0]:
                    left_pos = pos
                if right_pos[0] < rpos[0]:
                    right_pos = rpos
            total += int(left_pos[1] + right_pos[1])
        return total

    @property
    def default_data_part_1(self) -> tuple[str, int]:
        return ("""1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet""", 142)
    @property
    def default_data_part_2(self)-> tuple[str, int]:
        return ("""two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen""", 281)
