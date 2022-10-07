from typing import Optional
from fractions import Fraction
from os import get_terminal_size

def get_width(term_width: Optional[int]) -> int:
    if term_width is None:
        try:
            term_width = get_terminal_size().columns
        except OSError:
            term_width = 100
    return term_width


def make_bar(p: Fraction, max: int) -> str:
    l8 = round(p * max * 8)
    if l8 < 1:
        return ''
    ld, lm = divmod(l8, 8)
    end = ['', '▏', '▎', '▍', '▌', '▋', '▊', '▉'][lm]
    return '█' * ld + end

def make_ratio_bar(ratio:Fraction, _:Fraction, ratio_max:Fraction, max: int) -> str:
    return make_bar(ratio/ratio_max, max)

def make_acc_bar(_1:Fraction, acc:Fraction, _2:Fraction, max: int) -> str:
    return make_bar(acc, max)

def make_inv_acc_bar(ratio:Fraction, acc:Fraction, _:Fraction, max: int) -> str:
    return make_bar(1 - acc + ratio, max)

bar_styles = {
    'normal': make_ratio_bar,
    'accum': make_acc_bar,
    'inv-accum': make_inv_acc_bar,
}
