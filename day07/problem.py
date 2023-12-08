import typing
from pprint import pprint
from typing import Tuple, Dict, Iterable
import unittest
from functools import cmp_to_key

from data import data, example


Card = int
Hand = Tuple[Card, Card, Card, Card, Card]
Bet = int
Round = Tuple[Hand, Bet]
Input = list[Round]

FIVE_KIND = 100
FOUR_KIND = 90
HOUSE = 80
THREE_KIND = 70
TWO_PAIR = 60
PAIR = 50
HIGH_CARD = 10

hand_scores: typing.Dict[Tuple[int, ...], int] = {
    (5,): FIVE_KIND,
    (1, 4): FOUR_KIND,
    (2, 3): HOUSE,
    (1, 1, 3): THREE_KIND,
    (1, 2, 2): TWO_PAIR,
    (1, 1, 1, 2): PAIR,
    (1, 1, 1, 1, 1): HIGH_CARD,
}


def hand_value(hand: Round) -> int:
    cards = hand[0]
    d: Dict[Card, int] = {}
    for card in cards:
        d[card] = 1 + d.get(card, 0)
    return hand_scores[tuple(sorted(d.values()))]


J5 = FIVE_KIND - 2
J4 = FOUR_KIND - 2
JHOUSE = HOUSE - 2
J3 = THREE_KIND - 2
JTWOPAIR = TWO_PAIR - 2
J2 = PAIR - 2

hand_scores2: typing.Dict[Tuple[Card, Tuple[Card, ...]], int] = {
    (0, (5,)): FIVE_KIND,
    (0, (1, 4)): FOUR_KIND,
    (0, (2, 3)): HOUSE,
    (0, (1, 1, 3)): THREE_KIND,
    (0, (1, 2, 2)): TWO_PAIR,
    (0, (1, 1, 1, 2)): PAIR,
    (0, (1, 1, 1, 1, 1)): HIGH_CARD,
    (1, (4,)): J5,
    (1, (1, 3)): J4,
    (1, (2, 2)): max(JHOUSE, J3),
    (1, (1, 1, 2)): J3,
    (1, (1, 1, 1, 1)): J2,
    (2, (3,)): J5,
    (2, (1, 2)): max(J4, JHOUSE),
    (2, (1, 1, 1)): max(J3, JTWOPAIR),
    (3, (2,)): J5,
    (
        3,
        (
            1,
            1,
        ),
    ): J4,
    (4, (1,)): J5,
    (5, ()): J5,
}


def hand_value2(hand: Round) -> int:
    cards = hand[0]
    d: Dict[Card, int] = {}
    for card in cards:
        d[card] = 1 + d.get(card, 0)
    jokers = d.pop(JOKER, 0)
    return hand_scores2[jokers, tuple(sorted(d.values()))]


def tuple5(it: Iterable[int]) -> Hand:
    (t1, t2, t3, t4, t5) = it
    return (t1, t2, t3, t4, t5)


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

    def get_card(s: str) -> Card:
        return card_value[s]

    return [
        (tuple5(map(get_card, line.split(" ")[0])), int(line.split(" ")[1]))
        for line in input.split("\n")
    ]


def mk_cmp_hands(hand_value, card_value):
    def cmp_hands(r1: Round, r2: Round):
        by_groups = hand_value(r1) - hand_value(r2)
        if by_groups != 0:
            return by_groups
        for i in range(5):
            v = card_value(r1[0][i]) - card_value(r2[0][i])
            if v != 0:
                return v
        raise RuntimeError("Equals?", r1, r2)
    return cmp_hands


def part1(input: Input):
    cmp_hands = mk_cmp_hands(hand_value, id)
    ranked = sorted(input, key=cmp_to_key(cmp_hands))
    return sum(rank * bet for rank, (hand, bet) in enumerate(ranked, 1))


def part2(input: Input):
    def remap_card(card: Card) -> Card:
        if card == JOKER:
            return 1
        return card

    cmp_hands = mk_cmp_hands(hand_value2, card_value=remap_card)
    ranked = sorted(input, key=cmp_to_key(cmp_hands))
    pprint(ranked)
    return sum(rank * bet for rank, (hand, bet) in enumerate(ranked, 1))


JOKER = 11
WINNER_5 = 10 + 1
WINNER_1 = 2 + 5


class Tests(unittest.TestCase):
    def test_parse_example_answer(self):
        self.assertEqual(((3, 2, 10, 3, 13), 765), parse(example)[0])

    def test_part1_example_answer(self):
        self.assertEqual(6440, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(255048101, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(5905, part2(parse(example)))

    def test_part2_answer(self):
        # too high 254302015
        # too high 254281577
        # too high 254167331
        # not right 252957159
        # not right 254167331
        # not right 254049962
        self.assertEqual(-1, part2(parse(data)))

    def joker_pair_beats_high_card(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((1, 2, 3, 4, 10), 5),
                    ((1, 2, 3, 4, JOKER), 1),
                ]
            ),
        )
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    ((1, 2, 3, 4, JOKER), 5),
                    ((1, 2, 3, 4, 10), 1),
                ]
            ),
        )

    def joker_pair_lower_than_pair(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((1, 2, 3, 4, JOKER), 5),
                    ((1, 2, 4, 4, 10), 1),
                ]
            ),
        )

    def test_joker_pair_lower_than_pair_with_king_high(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((1, 2, 3, 4, JOKER), 5),
                    ((13, 2, 4, 4, 10), 1),
                ]
            ),
        )

    def test_joker_house_lower_than_house(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((2, 2, 3, 3, JOKER), 5),
                    ((2, 2, 3, 3, 3), 1),
                ]
            ),
        )

    def test_house_beats_joker_three(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((2, JOKER, 1, 3, JOKER), 5),
                    ((2, 2, 3, 3, 3), 1),
                ]
            ),
        )

    def test_joker_house_beats_three(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    ((2, 2, 3, 3, JOKER), 5),
                    ((1, 2, 3, 3, 3), 1),
                ]
            ),
        )

    def test_joker_four_beats_house(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    ((2, 2, 3, JOKER, JOKER), 5),
                    ((2, 2, 3, 3, 3), 1),
                ]
            ),
        )

    def test_joker_pair_lower_than_king_pair(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((1, 2, 3, 4, JOKER), 5),
                    ((13, 2, 3, 4, 13), 1),
                ]
            ),
        )

    def test_joker_five_lower_than_five(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((3, 3, 3, 3, JOKER), 5),
                    ((3, 3, 3, 3, 3), 1),
                ]
            ),
        )

    def test_joker_four_lower_than_four(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((3, 3, 3, 4, JOKER), 5),
                    ((3, 3, 3, 3, 4), 1),
                ]
            ),
        )

    def test_joker_loses_ties(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    ((JOKER, 2, 3, 3, JOKER), 5),
                    ((2, 3, 3, 3, 3), 1),
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
