#!/usr/bin/env python
from typing import Tuple, Generator, Callable, Iterable
from numpy import ndarray
from numpy.linalg import norm

Tffff = Tuple[float, float, float, float]
Tff = Tuple[float, float]
Cff = Callable[[float], float]
GTffff = Generator[Tffff, None, None]


def in_direction_of(func: Callable, direction: ndarray) -> Cff:
    """
    >>> from numpy import array
    >>> from numpy.linalg import norm
    >>>
    >>> def foo(xvec):
    ...     x0, x1 = xvec
    ...     return x0**2 + x1**2
    >>>
    >>> func = in_direction_of(foo, array([1,0]))
    >>> func(1) == foo([1, 0])
    True
    >>> func(1.34) == foo([1.34, 0])
    True
    >>> func = in_direction_of(foo, array([1,1]))
    >>> func(2**.5) == foo([1, 1])
    True
    """
    return lambda x: func(direction/norm(direction) * x)


def find_interval(func: Callable, position, step=1):
    """
    >>> left, right = find_interval_left(lambda x: x**2, 10, 1)
    >>> left <= 0
    True
    >>> right >= 0
    True
    >>> left, right = find_interval_right(lambda x: x**2, -10, 1)
    >>> left <= 0
    True
    >>> right >= 0
    True
    """
    if func(position + 1) > func(position):
        return find_interval_right(func, position, step)
    else:
        return find_interval_left(func, position, step)


def find_interval_left(func: Callable, position, step):
    """
    >>> left, right = find_interval_left(lambda x: x**2, 10, 1)
    >>> left <= 0
    True
    >>> right >= 0
    True
    >>> left, right = find_interval_right(lambda x: x**2, -10, 1)
    >>> left <= 0
    True
    >>> right >= 0
    True
    """
    left, right = find_interval_right(lambda x: func(-x), -position, step)
    return -right, -left


def find_interval_right(func: Callable, position, step):
    """
    >>> left, right = find_interval_right(lambda x: x**2, -10, 1)
    >>> left <= 0
    True
    >>> right >= 0
    True
    >>> left, right = find_interval_right(lambda x: x**2, -10, 20)
    >>> left <= 0
    True
    >>> right >= 0
    True
    """
    left = func(position)
    right_position = position + step
    right = func(right_position)
    while left > right:
        right_position += step
        left, right = right, func(right_position)
        step *= 2
    return position, right_position


def findmin(func: Cff, borders: Tff, accuracy: float) -> GTffff:
    delta = accuracy / 3
    a, b = borders
    while b - a > accuracy:
        x = (a + b) / 2
        x1, x2 = x - delta, x + delta
        yield a, b, x1, x2
        fx1, fx2 = func(x1), func(x2)
        if fx1 > fx2:
            a = x1
        elif fx1 < fx2:
            b = x2


def golden_ratio(func: Cff, borders: Tff, accuracy: float) -> GTffff:
    a, b = borders
    leftGL = (3 - 5 ** .5) / 2
    rightGR = (5 ** .5 - 1) / 2
    x1 = a + leftGL * (b - a)
    x2 = a + rightGR * (b - a)
    yield a, b, x1, x2
    fx1 = func(x1)
    fx2 = func(x2)
    while b - a > accuracy:
        if fx1 > fx2:
            a, x1, fx1 = x1, x2, fx2
            x2 = a + rightGR * (b - a)
            fx2 = func(x2)
        elif fx2 > fx1:
            b, x2, fx2 = x2, x1, fx1
            x1 = a + leftGL * (b - a)
            fx1 = func(x1)
        yield a, b, x1, x2


def fib(n: int) -> int:
    return int((((1 + 5 ** .5) / 2) ** n - ((1 - 5 ** .5) / 2) ** n) / 5 ** .5)


def find_fib(borders: Tff, accuracy: float) -> int:
    position = 10
    a, b = borders
    x = (a - b) / accuracy
    while fib(position) <= x:
        position *= 2
    return position


def fib_search(func: Cff, borders: Tff, accuracy: float) -> GTffff:
    N = find_fib(borders, accuracy)
    fibN2, fibN1 = fib(N), fib(N - 1)
    fibN = fibN2 - fibN1
    a, b = borders
    c = (b - a) / fibN2
    x1, x2 = a + fibN * c, a + fibN1 * c
    fx1, fx2 = func(x1), func(x2)
    yield a, b, x1, x2
    while b - a > accuracy:
        fibN2, fibN1 = fibN1, fibN
        fibN = fibN2 - fibN1
        if fx1 < fx2:
            b, x2, fx2 = x2, x1, fx1
            x1 = a + fibN / fibN2 * (b - a)
            fx1 = func(x1)
        elif fx1 > fx2:
            a, x1, fx1 = x1, x2, fx2
            x2 = a + fibN1 / fibN2 * (b - a)
            fx2 = func(x2)
        yield a, b, x1, x2
