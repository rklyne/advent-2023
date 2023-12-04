import typing
import unittest

from data import data, example

Card = typing.Tuple[list[int], list[int]]
Input = list[Card]

# This garbage doesn't type check but it runs :D
def flatten(ls) -> list[int]:
    l = []
    for item in ls:
        if isinstance(item, list):
            l.extend(flatten(item))
        else:
            l.append(item)
    return l


def parse(input: str) -> Input:
    def numbers(txt: str) -> list[int]:
        return list(map(int, filter(bool, txt.split(" "))))

    def parse_card(line: str) -> Card:
        line = line.split(": ")[1]
        winning, mine = line.split(" | ")
        return numbers(winning), numbers(mine)

    return list(map(parse_card, input.split("\n")))


def win_count(pair) -> int:
    winning, mine = pair
    return len(set(winning).intersection(set(mine)))


def part1(input: Input):
    def win_score(pair) -> int:
        count = win_count(pair)
        if count == 0:
            return 0
        return 2**(count-1)

    return sum(map(win_score, input))


def part2(input: Input):
    winners = list(map(win_count, input))
    card_wins_cards = {}
    for num, wins in enumerate(winners, 1):
        l: list[int] = []
        card_wins_cards[num] = l
        for i in range(1, wins+1):
            l.append(num + i)
    card_scores = {}
    for num, wins in enumerate(winners, 1):
        l: list[int | list] = [1]
        card_scores[num] = l
    for num, wins in enumerate(winners, 1):
        for copy in card_wins_cards[num]:
            card_scores[num].append(card_scores[copy])
    return len(flatten(card_scores.values()))


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(([41, 48, 83, 86, 17], [83, 86, 6, 31, 17, 9, 48, 53]), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(13, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(23847, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(30, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(8570000, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
