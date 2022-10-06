#! /usr/bin/python3

from math import factorial
from functools import reduce
from operator import mul
from os import get_terminal_size
from typing import Optional
from fractions import Fraction
import argparse

def choose(n: int, k: int) -> int:
    assert n >= k >= 0
    return reduce(mul, range(n-k+1, n+1), 1) // factorial(k)


def get_width(term_width: Optional[int]) -> int:
    if term_width is None:
        try:
            term_width = get_terminal_size().columns
        except OSError:
            term_width = 100
    return term_width


def print_hist(n:int, p: Fraction, term_width: Optional[int] = None, accumulated: bool = False, invert: bool = False) -> None:
    wp = len(str(choose(n, n//2)))
    wn = len(str(n))
    mode = int(n*p + p)
    max_ratio = choose(n, mode) * p**mode * (1-p)**(n-mode)
    hist_width = get_width(term_width) - 27 - wp - wn
    accum_p = Fraction(0)
    pos = 1
    ratio = (1-p)**n
    for i in range(0, n+1):
        if i > 0:
            pos_prev = pos
            pos = pos_prev * (n-i+1) // (i)
            ratio = ratio * pos * p / pos_prev / (1-p)
        accum_p += ratio
        desc = f"{i:{wn}}: {pos:{wp}} {float(ratio):7.2%} {float(accum_p):7.2%} {float(1-accum_p):7.2%} "
        relative_length = ratio/max_ratio if not accumulated else accum_p
        if invert:
            relative_length = 1 - relative_length
        bar = '━' * round(hist_width * relative_length)
        print(desc + bar)


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser(args[0])
    parser.add_argument('n', type=int, help="The number of coin tosses")
    parser.add_argument('-p', "--probability", type=Fraction, default=Fraction(1,2), help="set the probability of a coin toss resulting in 1")
    parser.add_argument('-w', "--width", type=int, default=None, help="set the width of the output, defaults to terminal-width if available")
    parser.add_argument('-a', "--accumulate", action="store_true", help="show the graph for the accumulated probability")
    parser.add_argument('-i', "--invert", action="store_true", help="invert the lengths of the printed bars")
    parsed = parser.parse_args()
    p = parsed.p
    if not 0 <= p <= 1:
        print(f"Error: p musst be between 0 and 1")
        return 1
    print_hist(parsed.n, p, term_width=parsed.w, accumulated=parsed.a, invert=parsed.i)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
