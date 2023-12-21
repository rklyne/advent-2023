from typing import Tuple, NewType, Iterable, Dict, Literal, Callable
import typing
import unittest

from data import data, example, example2


Name = NewType("Name", str)
Signal = Literal["low", "high"]
LOW: Signal = "low"
HIGH: Signal = "high"
Op = Literal["%", "&", ""]
NAND: Op = "&"
TOGGLE: Op = "%"
Instr = Tuple[Name, Op, list[Name]]
Input = list[Instr]
Pulse = Tuple[Name, Signal, Name]


def _parse(input: str) -> Iterable[Instr]:
    for line in input.split("\n"):
        name, targets = line.split(" -> ")
        op: Op = ""
        if name[0] in "&%":
            op = name[0]
            name = name[1:]
        yield (Name(name), op, [Name(t) for t in targets.split(", ")])


def parse(i: str) -> Input:
    return list(_parse(i))


def _invert(s: Signal) -> Signal:
    if s == LOW:
        return HIGH
    return LOW


ONE_HIGH = set([HIGH])


class Computer:
    _inputs: Dict[Name, Tuple[Op, list[Name]]]
    _next: Dict[Name, list[Name]]
    _prev: Dict[Name, list[Name]]
    _pending: list[Pulse]
    _records: Dict[Name, Tuple[int, int]]


    def __init__(self, inputs: Input, observer: Callable[[Pulse], None]= None):
        self._inputs = {n: (op, ns) for n, op, ns in inputs}
        self._next = {n: ns for n, op, ns in inputs}
        self._prev = {}
        for src, _, ns in inputs:
            for n in ns:
                self._prev.setdefault(n, []).append(src)
        self._pending = []
        self._records = {}
        self._loops = 0
        self._state = {n: self._initial_state(op, n) for n, op, ns in inputs}
        self._send_high = 0
        self._send_low = 0
        self.observer = observer

    def _initial_state(self, op: Op, name: Name):
        if op == TOGGLE:
            return LOW
        if op == NAND:
            return {n: LOW for n in self._prev[name]}

    def _send(self, src: Name, signal: Signal):
        for n in self._next[src]:
            self._send_to(n, signal, src)

    def _send_to(self, target: Name, signal: Signal, src: Name):
        self._pending.append((target, signal, src))
        if self.observer:
            self.observer(self._pending[-1])
        recording = src
        self._records.setdefault(recording, (0, 0))
        if signal == HIGH:
            self._send_high += 1
            self._records[recording] = (self._records[recording][0], self._records[recording][1]+1)
        else:
            self._send_low += 1
            self._records[recording] = (self._records[recording][0]+1, self._records[recording][1])

    def process_step(self, trigger: Name = Name("broadcaster"), signal: Signal = LOW):
        self._send_to(trigger, signal, "none")
        while self._pending:
            n, s, f = self._pending.pop()
            self._compute(n, s, f)
            self._loops += 1

    def _compute(self, target: Name, signal: Signal, src: Name):
        if target not in self._inputs:
            return
        op, _ = self._inputs[target]
        if op == TOGGLE:
            if signal == LOW:
                self._state[target] = _invert(self._state[target])
                self._send(target, self._state[target])
        elif op == NAND:
            state = self._state[target]
            state[src] = signal
            if set(state.values()) == ONE_HIGH:
                out = LOW
            else:
                out = HIGH
            self._send(target, out)
        elif op == "":
            self._send(target, signal)
        else:
            raise RuntimeError("oops", op)

    def read(self, n: Name) -> Tuple[int, int]:
        return self._records.get(n, (0, 0))

    def reset(self, n: Name) -> None:
        self._records[n] = (0, 0)

    def read_total(self, n: Name) -> Tuple[int, int]:
        return self._send_low, self._send_high

    def debug(self, big=False):
        small = {"loops": self._loops}
        if not big:
            return small
        small.update({
            "states": self._state
        })
        return small

    def dot(self):
        out: list[str] = []
        for src, ns in self._next.items():
            for n in ns:
                out.append(f"{src} -> {n}")
        for n in self._inputs:
            op, _ = self._inputs[n]
            out.append(f'{n} [label="{op} {n}"]')
        return "digraph {\n  " + "\n  ".join(out) + "\n}"

def part1(input: Input):
    computer = Computer(input)
    for i in range(1000):
        computer.process_step()
    low, high = computer.read_total(Name("output"))
    # print(f"loops ({low}, {high}): {computer.debug()}")
    return low * high


def steps_to(input: Input, name: str):
    computer = Computer(input)
    n = Name(name)
    c = 0
    done = False
    for i in range(1_000_000):
        computer.process_step()
        c += 1
        low, high = computer.read(n)
        if high:
            done = True
            break
    if not done:
        raise RuntimeError("overflow")
    return c


def steps_to_each(input: Input, names_in: list[str], seek: Signal) -> Dict[str, list[int]]:
    names = [Name(n) for n in names_in]
    c = 0

    tracks: Dict[str,  list[int]] = {n: [] for n in names}
    loops_to_find = 4

    def observe(signal: Pulse):
        src, pulse, dest = signal
        if pulse != seek:
            return
        if dest not in tracks:
            return
        if len(tracks[dest]) > loops_to_find:
            return
        if c not in tracks[dest]:
            tracks[dest].append(c)

    computer = Computer(input, observer=observe)
    for i in range(1_000_000):
        c += 1
        computer.process_step()
        if all([len(c) >= loops_to_find for c in tracks.values()]):
            return tracks

    raise RuntimeError("overflow")


def part2(input: Input):
    c = 0
    """
    (4096 - sum(binary_bits)) -> BOOM

    &fb (fz) -> hb, vk, kl, cg
    &fb (fz) (4057) -> 32,  1,  4,  2
    &gp (xf) () ->  vm, cb, bd, qm, pk
    &gp (xf) (3769) -> 256,  2,  4, 64, 1
    &jl (mp) -> km, lm, ms,  lr, zb, bg
    &jl (mp) (3877) ->  1,  2,  8, 128, 64, 16
    &jn (hn) ->  hs, lp, hm, ql, xt, ss
    &jn (hn) (3847) -> 128, 16, 32, 64,  1,  8
    """

    # steps = steps_to(input, "fz")
    steps = steps_to_each(input, [
        # "fb", "gp", "jl", "jn",
        "hn", "mp", "xf", "fz",
    ], HIGH)
    # steps = steps_to_each(input, [
    #     "hn", "mp", "xf", "fz",
    #     "hb", "vk", "kl", "cg",
    #     "vm", "cb", "bd", "qm", "pk",
    #     "km", "lm", "ms", "lr", "zb", "bg",
    #     "hs", "lp", "hm", "ql", "xt", "ss",
    # ], LOW)
    print(f"fz: {steps}")
    # print(f"loops ({low}, {high}): {computer.debug(True)}")
    return c


class Tests(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(("broadcaster", "", ["a", "b", "c"]), parse(example)[0])

    @unittest.skip
    def test_print_dot(self):
        print("")
        print(Computer(parse(data)).dot())
        print("")

    def test_part1_example_answer(self):
        self.assertEqual(32000000, part1(parse(example)))

    def test_part1_example2_answer(self):
        self.assertEqual(11687500, part1(parse(example2)))

    def test_part1_answer(self):
        self.assertEqual(806332748, part1(parse(data)))

    # @unittest.skip
    def test_part2_answer(self):
        # too low 695433843
        # too low 56881971201792
        # wrong   227583967598592
        # wrong 29822534917445124096
        self.assertEqual(228060006554227, part2(parse(data)))


if __name__ == "__main__":
    unittest.main()
