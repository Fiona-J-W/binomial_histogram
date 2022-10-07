from fractions import Fraction
from decimal import localcontext, Decimal

exp_table = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹',
    '+': '⁺',
    '-': '⁻',
}


def to_exp(n: int, space: int) -> str:
    digits = ''.join((exp_table[digit] for digit in str(n)))
    return '⁰'*(space-len(digits)) + digits


max_n_exp = 14
max_n_digits = 2**max_n_exp
max_n = 10**max_n_digits
lengths_table = [(10**i, i)
                 for i in (2**j for j in range(max_n_exp - 1, -1, -1))]


def comp_digits(n: int) -> int:
    digits = 0
    while n >= max_n:
        n //= max_n
        digits += max_n_digits
    for n_i, i in lengths_table:
        if n >= n_i:
            n //= n_i
            digits += i
    return digits + 1

def scientific_length_max(n: int, prec: int) -> int:
    raw_length = comp_digits(n)
    exp_space = comp_digits(raw_length)
    if prec == 0:
        return min(4+exp_space, raw_length)
    return min(5 + prec + exp_space, raw_length)

def to_scientific(n: int, prec: int = 2, space: int = 10) -> str:
    #assert space >= 5 + prec
    exp_space = space - 5 - prec
    assert prec >= 0
    digits = comp_digits(n)
    if digits <= space:
        return f"{n:{space}}"
    leading = str(n // (10**(digits-prec-1)))
    leading_digit = leading[0]
    decimals=leading[1:]
    exp = to_exp(digits-1, exp_space)
    if prec == 0:
        return f"{leading_digit}⋅10{exp}"
    else:
        return f"{leading_digit}.{decimals}⋅10{exp}"

def percent_length_max(prec: int) -> int:
    return 4 if prec <= 0 else 5+prec

def to_percent(x: Fraction, prec: int) -> str:
    if prec <= 0:
        wper = 4
        prec = 0
    else:
        wper = 5 + prec

    if prec < 16:
        return f"{float(x):{wper}.{prec}%}"
    else:
        with localcontext() as ctx:
            ctx.prec = prec + 2
            return f"{(Decimal(x.numerator) / Decimal(x.denominator)):{wper}.{prec}%}"

