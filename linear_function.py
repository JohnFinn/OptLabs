from __future__ import annotations
from numpy import array


class LinearFunction:
    """
    >>> f = LinearFunction(1, [2, 3])
    >>> f
    1 + 2*x₀ + 3*x₁
    >>> f.rearrange(0)
    >>> f
    0.5 + -1.0*x₀ + 1.5*x₁
    >>> f.substitute(1, LinearFunction(4,[3,2]))
    >>> f.free
    6.5
    >>> list(f.coefs)
    [3.5, 3.0]
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
        self._coefs += val * other._coefs
        self._coefs[index] = val * other._coefs[index]
        self._free += val * other._free

    def rearrange(self, index: int):
        val = self._coefs[index]
        self._coefs = self._coefs / val
        self._free /= val
        self.coefs[index] = -1

    def __repr__(self):
        return f'{self.free} + ' + ' + '.join(map(self._str_one, range(len(self._coefs))))

    def _str_one(self, index: int) -> str:
        return f'{self._coefs[index]}*x{str(index).translate(LinearFunction.subscript)}'
