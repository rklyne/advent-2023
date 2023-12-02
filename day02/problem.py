from pprint import pprint
import typing
import unittest

from data import data, example


Id = int
Draw = typing.Tuple[int, int, int]  # R G B
Game = typing.Tuple[Id, list[Draw]]
Input = list[Game]


def parse(input: str) -> Input:
    def parse_draw(draw_text: str) -> Draw:
        items = {}
        for group in draw_text.split(", "):
            n, colour = group.split(" ")
            items[colour[0]] = int(n)
        return [items.get("r", 0), items.get("g", 0), items.get("b", 0)]

    def parse_game(game_text: str) -> Game:
        # Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        id_text, draws = game_text.split(": ")
        return [int(id_text[5:]), list(map(parse_draw, draws.split("; ")))]

    return list(map(parse_game, input.split("\n")))


def part1(input: Input):
    limits: Draw = [12, 13, 14]
    possible_games = [
        game
        for game in input
        if all(
            [
                all([pair[0] <= pair[1] for pair in zip(draw, limits)])
                for draw in game[1]
            ]
        )
    ]
    return sum(
        [
            game[0]
            for game in possible_games
        ]
    )


def part2(input: Input):
    return 0


class Tests(unittest.TestCase):
    def test_parse(self):
        games = parse(example)
        self.assertEqual([1, [[4, 0, 3], [1, 2, 6], [0, 2, 0]]], games[0])

    def test_part1_example_answer(self):
        self.assertEqual(8, part1(parse(example)))

    def test_part1_answer(self):
        self.assertEqual(-1, part1(parse(data)))

    def test_part2_example_answer(self):
        self.assertEqual(-1, part2(parse(example)))

    def test_part2_answer(self):
        self.assertEqual(-1, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
