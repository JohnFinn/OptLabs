from __future__ import annotations
from numpy import array
from typing import List
from operator import mul
from fractions import Fraction


class LinearFunction:
    """
    >>> f = LinearFunction(18, [-2, -1, -1])
    >>> f.rearrange(0)
    >>> print(f)
    9 + -1/2*x₀ + -1/2*x₁ + -1/2*x₂
    >>> f2 = LinearFunction(30, [-1, -2, -2])
    >>> f2.substitute(0, f)
    >>> print(f2)
    21 + 1/2*x₀ + -3/2*x₁ + -3/2*x₂
    """
    subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def __init__(self, free, coefs):
        self._free = Fraction(free)
        self._coefs = array(list(map(Fraction, coefs)))

    def __call__(self, args: List[float]) -> float:
        return self._free + sum(map(mul, self._coefs, args))

    @property
    def coefs(self):
        return self._coefs

    @property
    def free(self):
        return self._free

    def substitute(self, index: int, other: LinearFunction):
        val = self._coefs[index]
        self._coefs += other._coefs * val
        self._coefs[index] = val * other._coefs[index]
        self._free += val * other._free

    def rearrange(self, index: int):
        val = self._coefs[index]
        self._coefs[index] = -1
        self._coefs = self._coefs / -val
        self._free /= -val

    def __str__(self):
        return f'{self.free} + ' + ' + '.join(map(self._str_one, range(len(self._coefs))))

    def _str_one(self, index: int) -> str:
        return f'{self._coefs[index]}*x{str(index).translate(LinearFunction.subscript)}'
