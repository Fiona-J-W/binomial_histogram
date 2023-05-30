#! /usr/bin/python3

from typing import Optional, Callable
from fractions import Fraction
from binomial.stringify import to_scientific, to_percent, scientific_length_max, percent_length_max
import argparse

from binomial import choose, comp_hist, get_width, bar_styles

Filter = Callable[[Fraction, Fraction], bool]

def print_hist(n: int, p: Fraction, term_width: Optional[int] = None,
        prec: int = 2, filter: Filter = lambda x,y:True, style: str = 'normal') -> None:
    max_pos = choose(n, n // 2)
    mode = int(n * p + p)
    max_ratio = choose(n, mode) * p**mode * (1 - p)**(n - mode)
    wp = scientific_length_max(max_pos, prec)
    wn = len(str(n))
    hist_width = get_width(term_width) - 6 - wp - wn - \
        3 * percent_length_max(prec)
    for i, pos, ratio, acc in comp_hist(n, p):
        if not filter(ratio, acc):
            continue
        desc = f"{i:{wn}}: {to_scientific(pos, prec, wp)}"\
            + f" {to_percent(ratio, prec)}"\
            + f" {to_percent(acc, prec)}"\
            + f" {to_percent(1 - acc + ratio, prec)} "
        bar = bar_styles[style](ratio, acc, max_ratio, hist_width)
        print(desc + bar)


def main(args: list[str]) -> int:
    parser = argparse.ArgumentParser(args[0])
    parser.add_argument('n',
                        type=int,
                        help="The number of coin tosses")
    parser.add_argument('-p', "--probability",
                        type=Fraction, default=Fraction(1, 2),
                        help="set the probability of a coin toss resulting in 1")
    parser.add_argument('-P', "--precission",
                        type=int, default=2,
                        help="set how many decimals will be printed for percents")
    parser.add_argument('-w', "--width",
                        type=int, default=None,
                        help="set the width of the output,"
                        + " defaults to terminal-width if available and 100 otherwise")
    parser.add_argument('-s', "--style",
                        type=str, choices=bar_styles.keys(), default='normal',
                        help="show the graph for the accumulated probability")
    parser.add_argument('-m', "--min",
                        type=Fraction, default=Fraction(0),
                        help="minimum probability in percent needed for a value to be printed")
    parsed = parser.parse_args()
    p = parsed.probability
    if not 0 <= p <= 1:
        print(f"Error: p musst be between 0 and 1")
        return 1
    print_hist(parsed.n, p,
               prec=parsed.precission,
               term_width=parsed.width,
               style=parsed.style,
               filter=lambda r,acc: bool(min(acc, 1-acc+r) > (parsed.min / 100)))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
