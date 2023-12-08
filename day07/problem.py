import typing
from typing import Tuple, Dict, Iterable
import unittest
from functools import cmp_to_key

from data import data, example, example2


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

hand_scores2: typing.Dict[Tuple[Card, Tuple[Card, ...]], int] = {
    (0, (5,)): FIVE_KIND,
    (0, (1, 4)): FOUR_KIND,
    (0, (2, 3)): HOUSE,
    (0, (1, 1, 3)): THREE_KIND,
    (0, (1, 2, 2)): TWO_PAIR,
    (0, (1, 1, 1, 2)): PAIR,
    (0, (1, 1, 1, 1, 1)): HIGH_CARD,
    (1, (4,)): FIVE_KIND,
    (1, (1, 3)): FOUR_KIND,
    (1, (2, 2)): HOUSE,
    (1, (1, 1, 2)): THREE_KIND,
    (1, (1, 1, 1, 1)): PAIR,
    (2, (3,)): FIVE_KIND,
    (2, (1, 2)): FOUR_KIND,
    (2, (1, 1, 1)): THREE_KIND,
    (3, (2,)): FIVE_KIND,
    (
        3,
        (
            1,
            1,
        ),
    ): FOUR_KIND,
    (4, (1,)): FIVE_KIND,
    (5, ()): FIVE_KIND,
}


def hand_value2(hand: Round) -> int:
    cards = hand[0]
    d: Dict[Card, int] = {}
    for card in cards:
        d[card] = 1 + d.get(card, 0)
    jokers = d.pop(JOKER, 0)
    return hand_scores2[jokers, tuple(sorted(d.values()))]

def hand_value2b(hand: Round) -> int:
    cards = hand[0]
    d: Dict[Card, int] = {}
    for card in cards:
        d[card] = 1 + d.get(card, 0)
    jokers = d.pop(JOKER, 0)
    if jokers:
        def add_cards(d, card, jokers):
            d2 = d.copy()
            d2[card] += jokers
            return d2
        tries = [
            add_cards(d, card, jokers)
            for card in d
        ]
    else:
        tries = [d]
    return max([
        hand_scores[tuple(sorted(filter(bool, d.values())))]
        for d in tries
    ])


def tuple5(it: Iterable[int]) -> Hand:
    (t1, t2, t3, t4, t5) = it
    return (t1, t2, t3, t4, t5)


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


def parse_hand(cards: str) -> Hand:
    return tuple5(map(get_card, cards))


def parse(input: str) -> Input:
    return [
        (parse_hand(line.split(" ")[0]), int(line.split(" ")[1]))
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
    # pprint(ranked)
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
        # right = 253718286
        self.assertEqual(253718286, part2(parse(data)))

    def test_part2_example2(self):
        self.assertEqual(2090, part2(parse(example2)))

    def joker_pair_beats_high_card(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2345T"), 5),
                    (parse_hand("2345J"), 1),
                ]
            ),
        )
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    (parse_hand("2345J"), 5),
                    (parse_hand("2345T"), 1),
                ]
            ),
        )

    def joker_pair_lower_than_pair(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2345J"), 5),
                    (parse_hand("2344T"), 1),
                ]
            ),
        )

    def test_joker_pair_lower_than_pair_with_king_high(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2345J"), 5),
                    (parse_hand("K244T"), 1),
                ]
            ),
        )

    def test_joker_house_lower_than_house(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2233J"), 5),
                    (parse_hand("22333"), 1),
                ]
            ),
        )

    def test_house_beats_joker_three(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2J13J"), 5),
                    (parse_hand("22333"), 1),
                ]
            ),
        )

    def test_joker_house_beats_three(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    (parse_hand("2233J"), 5),
                    (parse_hand("42333"), 1),
                ]
            ),
        )

    def test_joker_four_beats_house(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    (parse_hand("223JJ"), 5),
                    (parse_hand("22333"), 1),
                ]
            ),
        )

    def test_joker_pair_lower_than_king_pair(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("2345J"), 5),
                    (parse_hand("K233K"), 1),
                ]
            ),
        )

    def test_joker_five_lower_than_five(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("3333J"), 5),
                    (parse_hand("33333"), 1),
                ]
            ),
        )

    def test_joker_four_of_a_kind_tiebreaks_on_four(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    (parse_hand("3334J"), 5),
                    (parse_hand("33334"), 1),
                ]
            ),
        )

    def test_joker_loses_ties(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("J2345"), 5),
                    (parse_hand("22345"), 1),
                ]
            ),
        )

    def test_joker_loses_ties_q_vs_t(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("T55J5"), 5),
                    (parse_hand("QQQJA"), 1),
                ]
            ),
        )

    def test_5_jokers_loses_to_5_2s(self):
        self.assertEqual(
            WINNER_5,
            part2(
                [
                    (parse_hand("22222"), 5),
                    (parse_hand("JJJJJ"), 1),
                ]
            ),
        )

    def test_5_jokers_beats_four_kind(self):
        self.assertEqual(
            WINNER_1,
            part2(
                [
                    (parse_hand("22223"), 5),
                    (parse_hand("JJJJJ"), 1),
                ]
            ),
        )

    def test_x_beats_y(self):
        self.assertEqual(
            2090,
            part2(
                [
                    (parse_hand("57592"), 534),
                    (parse_hand("Q92KJ"), 778),
                ]
            ),
        )

    def test_example_sequence(self):
        hands = [
            "32T3K",
            "KK677",
            "T55J5",
            "QQQJA",
            "KTJJT",
        ]
        pairs = list(zip(hands, hands[1:]))
        for pair in pairs:
            self.assertEqual(
                WINNER_1,
                part2(
                    [
                        (parse_hand(pair[0]), 5),
                        (parse_hand(pair[1]), 1),
                    ]
                ),
            )


if __name__ == "__main__":
    unittest.main()
