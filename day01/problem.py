import unittest

from data import data, example, example2


def to_num(line: str):
    digits = list(filter(lambda c: c.isdigit(), line))
    return int(digits[0] + digits[-1])


def parse(input: str):
    return filter(bool, input.split("\n"))


def part1(input: str):
    return sum(map(to_num, parse(input)))


def do_replacements(strings: [str]) -> [str]:
    pairs = [
            ("one", "1"),
            ("two", "2"),
            ("three", "3"),
            ("four", "4"),
            ("five", "5"),
            ("six", "6"),
            ("seven", "7"),
            ("eight", "8"),
            ("nine", "9"),
    ]

    def repl(s: str) -> str:
        count = 1
        while True:
            count += 1
            found = []
            for pair in pairs:
                idx = s.find(pair[0])
                if idx != -1:
                    found.append((idx, pair))
            if not found:
                return s
            if count > 100:
                raise RuntimeError(s)
            idx, pair = sorted(found)[0]
            s = s[:idx] + pair[1] + s[idx+1:]

    return map(repl, strings)


def part2(input: str):
    strings = do_replacements(parse(input))
    numbers = list(map(to_num, strings))
    return sum(numbers)


class Tests(unittest.TestCase):
    def test_part2_example_answer(self):
        self.assertEqual(142, part2(example))

    def test_part2_example_answer2(self):
        self.assertEqual(281, part2(example2))

    def test_part2_answer(self):
        self.assertEqual(54676, part2(data))

    def test_part1_example_answer(self):
        self.assertEqual(142, part1(example))

    def test_part1_answer(self):
        self.assertEqual(53921, part1(data))

    def test_trebuchet(self):
        self.assertEqual(77, part1("trebu7het"))

    def test_num_replacement(self):
        self.assertEqual(29, part2("two1nine"))

    def test_replacement_overlap(self):
        self.assertEqual(["x2w1ne34our"], list(do_replacements(["xtwone3four"])))


if __name__ == "__main__":
    unittest.main()
