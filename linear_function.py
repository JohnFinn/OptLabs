from __future__ import annotations
from numpy import array


class LinearFunction:
    """
    >>> f = LinearFunction(18.0, [-2.0, -1.0, -1.0])
    >>> f.rearrange(0)
    >>> f
    9.0 + -0.5*x₀ + -0.5*x₁ + -0.5*x₂
    >>> f2 = LinearFunction(30.0, [-1.0, -2.0, -2.0])
    >>> f2.substitute(0, f)
    >>> f2
    21.0 + 0.5*x₀ + -1.5*x₁ + -1.5*x₂
    """
    subscript = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

    def __init__(self, free, coefs):
        self._free = free
        self._coefs = array(coefs)

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

    def __repr__(self):
        return f'{self.free} + ' + ' + '.join(map(self._str_one, range(len(self._coefs))))

    def _str_one(self, index: int) -> str:
        return f'{self._coefs[index]}*x{str(index).translate(LinearFunction.subscript)}'
