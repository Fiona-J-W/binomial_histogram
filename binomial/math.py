from math import factorial
from typing import Iterable
from fractions import Fraction

def choose(n: int, k: int) -> int:
    # In python 3.10 this is literally faster than math.comb and the other options I tried
    # (I’d guess that `factorial` calls gmp and comb is likely implemented badly in python):
    return factorial(n) // (factorial(n-k) * factorial(k))


def comp_hist(n: int, p: Fraction) -> Iterable[tuple[int, int, Fraction, Fraction]]:
    pos = 1
    ratio = (1 - p)**n
    acc = ratio
    yield 0, pos, ratio, acc
    for i in range(1, n + 1):
        pos_prev = pos
        pos = pos_prev * (n - i + 1) // (i)
        ratio = ratio * pos * p / pos_prev / (1 - p)
        acc += ratio
        yield i, pos, ratio, acc

