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


def make_bar(p: Fraction, max: int) -> str:
    l8 = round(p*max*8)
    ld, lm =divmod(l8, 8)
    end = ['', '▏', '▎', '▍', '▌', '▋', '▉', '▊'][lm]
    return '█' * ld + end


def print_hist(n:int, p: Fraction, term_width: Optional[int] = None, accumulated: bool = False, invert: bool = False, min: Fraction = Fraction(0)) -> None:
    wp = len(str(choose(n, n//2)))
    wn = len(str(n))
    mode = int(n*p + p)
    max_ratio = choose(n, mode) * p**mode * (1-p)**(n-mode)
    hist_width = get_width(term_width) - 27 - wp - wn
    accum_p = Fraction(0)
    accum_m = Fraction(1)
    pos = 1
    ratio = (1-p)**n
    for i in range(0, n+1):
        if i > 0:
            pos_prev = pos
            pos = pos_prev * (n-i+1) // (i)
            ratio = ratio * pos * p / pos_prev / (1-p)
        accum_p += ratio
        if ratio < min:
            accum_m -= ratio
            continue
        desc = f"{i:{wn}}: {pos:{wp}} {float(ratio):7.2%} {float(accum_p):7.2%} {float(accum_m):7.2%} "
        relative_length = ratio/max_ratio
        if accumulated and not invert:
            relative_length = accum_p
        elif accumulated and invert:
            relative_length = accum_m
        bar = make_bar(relative_length, hist_width)
        print(desc + bar)
        accum_m -= ratio


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser(args[0])
    parser.add_argument('n', type=int, help="The number of coin tosses")
    parser.add_argument('-p', "--probability", type=Fraction, default=Fraction(1,2), help="set the probability of a coin toss resulting in 1")
    parser.add_argument('-w', "--width", type=int, default=None, help="set the width of the output, defaults to terminal-width if available and 100 otherwise")
    parser.add_argument('-a', "--accumulate", action="store_true", help="show the graph for the accumulated probability")
    parser.add_argument('-i', "--invert", action="store_true", help="invert the lengths of the printed bars")
    parser.add_argument('-m', "--min", type=Fraction, default=Fraction(0), help="minimum probability needed for a value to be printed")
    parsed = parser.parse_args()
    p = parsed.probability
    if not 0 <= p <= 1:
        print(f"Error: p musst be between 0 and 1")
        return 1
    print_hist(parsed.n, p, term_width=parsed.width, accumulated=parsed.accumulate, invert=parsed.invert, min=parsed.min)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
