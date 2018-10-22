#!/usr/bin/env python
from matplotlib import pyplot
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import proj3d
from typing import Iterable, Generator, Tuple, Callable
import numpy
from uniModMin import in_direction_of, findmin, find_interval
from numpy.linalg import norm
from copy import copy
import sympy
from itertools import chain

vec = numpy.ndarray


def gradient(func: Callable[[numpy.ndarray], float], x: numpy.ndarray, delta: float) -> numpy.ndarray:
    '''
    >>> gradient(lambda x:x[0]*2, numpy.array([1.0]),.1)
    array([2.])
    >>> gradient(lambda x:x[0]*2+x[1]*3, numpy.array([1.0, 4.2]),.1)
    array([2., 3.])
    '''
    result = []
    for index in range(len(x)):
        x[index] += delta/2
        right = func(x)
        x[index] -= delta
        left = func(x)
        x[index] += delta/2
        result.append((right - left) / delta)
    return numpy.array(result)


def gradient_descent(func: Callable[[vec], float], start: vec, delta: float = .001):
    step = numpy.array([delta + 1])
    while all(abs(step) > delta):
        step = find_step(func, start, delta)
        start += step
        yield start


def find_step(func: Callable, position, delta):
    grad = -gradient(func, position, delta)
    func_slice = in_direction_of(func, position, grad)
    step = findmin(func_slice, find_interval(func_slice, 0), delta)
    return grad / norm(grad) * step


class LineDrawer:
    def __init__(self, axis, get_next_point):
        self.prev = next(get_next_point)
        self.get_next_point = get_next_point
        self.axis = axis
        self.stopped = False

    def __call__(self):
        try:
            point = next(self.get_next_point)
        except StopIteration:
            self.stopped = True
        else:
            self.axis.plot(*zip(self.prev, point), [foo(self.prev), foo(point)], 'r-')
            self.prev = copy(point)
        finally:
            return self.prev


class Combine:
    def __init__(self):
        self.funcs = []
        self.results = []

    def add(self, func: Callable):
        self.funcs.append(func)

    def __call__(self, *args, **kwargs):
        self.results.clear()
        for func in self.funcs:
            self.results.append(func(*args, **kwargs))


if __name__ == '__main__':
    def foo(x):
        x1, x2 = x[0], x[1]
        return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2
    print(foo((1, 1)))

    syms = sympy.symbols('x₁ x₂')
    func = foo(syms)
    g = sum(map(func.diff, syms))
    print(g)
    solved = sympy.solvers.solve(g)
    print(solved)
    fig = pyplot.figure()

    x = numpy.linspace(-100, 100, 2000)
    X, Y = numpy.meshgrid(x, x)
    ax3d = fig.add_subplot(1, 1, 1, projection='3d')
    ax3d.plot_surface(X, Y, foo((X, Y)))
    ax3d.set_xlabel('X1')
    ax3d.set_ylabel('X2')
    bnext3d = Button(pyplot.axes([.9, 0, 1, .1]), 'Next')

    c = Combine()
    for start in [80.0, -70.0], [-80.0, 70.0], [80.0, 70.0], [-80.0, -70.0], [0.0, 50.0], [5.0, 75.0], [-5.0, 75.0]:
        start = numpy.array(start)
        desc = gradient_descent(foo, start, .0001)
        on_click = LineDrawer(ax3d, chain((copy(start), ), desc))
        c.add(on_click)

    bnext3d.on_clicked(lambda event: c())

    pyplot.show(block=True)
    for result in c.results:
        print(result, foo(result))
