#!/usr/bin/env python
from matplotlib import pyplot
from matplotlib.widgets import Button
from mpl_toolkits.mplot3d import proj3d
from typing import Iterable, Generator, Tuple, Callable
import numpy
from uniModMin import in_direction_of, findmin, find_interval
from numpy.linalg import norm
from copy import copy

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


if __name__ == '__main__':
    def foo(x):
        x1, x2 = x[0], x[1]
        return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2

    fig = pyplot.figure()

    x = numpy.linspace(-100, 100, 2000)
    X, Y = numpy.meshgrid(x, x)
    start = numpy.array([80.0, -70.0])
    ax3d = fig.add_subplot(1, 1, 1, projection='3d')
    ax3d.plot_surface(X, Y, foo((X, Y)))
    ax3d.set_xlabel('X1')
    ax3d.set_ylabel('X2')
    bnext3d = Button(pyplot.axes([.9, 0, 1, .1]), 'Next')
    desc = gradient_descent(foo, start, .001)
    prev = copy(start)


    def on_click(event):
        global prev
        point = next(desc)
        ax3d.plot(*zip(prev, point), [foo(prev), foo(point)], 'r-')
        prev = copy(point)

    bnext3d.on_clicked(on_click)

    pyplot.show(block=True)
    print(prev, foo(prev))
