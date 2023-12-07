import typing
from typing import Tuple, Dict
import unittest
from functools import cmp_to_key

from data import data, example


Card = int
Hand = Tuple[Card, Card, Card, Card, Card]
Bet = int
Round = Tuple[Hand, Bet]
Input = list[Round]


hand_scores: typing.Dict[Tuple[int, ...], int] = {
    (5,): 10,
    (1, 4): 9,
    (2, 3): 8,
    (1, 1, 3): 7,
    (1, 2, 2): 6,
    (1, 1, 1, 2): 5,
    (1, 1, 1, 1, 1): 1,
}


def hand_value(hand: Round) -> int:
    cards = hand[0]
    d: Dict[Card, int] = {}
    for card in cards:
        d[card] = 1 + d.get(card, 0)
    return hand_scores[tuple(sorted(d.values()))]


def parse(input: str) -> Input:
    card_value: Dict[str, Card] = {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    return [
        (tuple(map(card_value.get, line.split(" ")[0])), int(line.split(" ")[1]))
        for line in input.split("\n")
    ]


def cmp_hands(r1: Round, r2: Round):
    by_groups = hand_value(r1) - hand_value(r2)
    if by_groups != 0:
        return by_groups
    for i in range(5):
        v = r1[0][i] - r2[0][i]
        if v != 0:
            return v
    return 0


def part1(input: Input):
    ranked = sorted(input, key=cmp_to_key(cmp_hands))
    return sum(rank * bet for rank, (hand, bet) in enumerate(ranked, 1))


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse_example_answer(self):
        self.assertEqual(((3, 2, 10, 3, 13), 765), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(6440, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
