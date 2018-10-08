#!/usr/bin/env python
from matplotlib import pyplot
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from typing import Iterable, Generator, Tuple, Callable
import numpy
import uniModMin

vec = numpy.ndarray


class Arrow3D(FancyArrowPatch):

    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


def update_all_x_data(lines: Iterable[Line2D], gen: Generator[Tuple, None, None]) -> Generator[None, None, None]:
    for args in gen:
        for line, xdata in zip(lines, args):
            line.set_xdata(xdata)
        yield


def flatten(iterable: Iterable[Iterable]) -> Iterable:
    for i in iterable:
        yield from i


def gradient(func: Callable[[numpy.ndarray], float], x: numpy.ndarray, delta: float) -> numpy.ndarray:
    '''
    >>> gradient(lambda x:x[0]*2, numpy.array([1.0]),.1)
    array([2.])
    >>> gradient(lambda x:x[0]*2+x[1]*3, numpy.array([1.0, 4.2]),.1)
    array([2., 3.])
    '''
    fx = func(x)
    result = []
    for index in range(len(x)):
        x[index] += delta
        result.append((func(x) - fx) / delta)
        x[index] -= delta
    return numpy.array(result)


def first_derivative_descent(func: Callable[[vec], float], x: vec, delta: float = .001, step: float = .001):
    while True:
        grad = gradient(func, x, delta)
        x += step * grad
        yield grad


if __name__ == '__main__':
    def f(x):
        return x ** 2 + 3 * x


    accuracy = .005
    left, right = -10, 10
    arr = numpy.arange(left, right, accuracy / 10)

    # pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(1, 2, 1)


    def foo(x):
        x1, x2 = x[0], x[1]
        return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2


    x = y = numpy.linspace(-10, 10, 20)
    X, Y = numpy.meshgrid(x, y)
    Z = foo((X, Y))

    ax3d = fig.add_subplot(1, 2, 2, projection='3d')
    ax3d.plot_surface(X, Y, Z)
    ax3d.set_xlabel('X1')
    ax3d.set_ylabel('X2')

    a = Arrow3D([0, 10], [0, 10], [0, 1000000], mutation_scale=20,
                lw=1, arrowstyle="-|>", color="r")
    ax3d.add_artist(a)

    # x0 = numpy.array([7,7])
    # g = first_derivative_descent(foo, x)
    # for desc in g:
    #     ax3d.arrow()

    # ax3d.plot(
    #     [x[0]], [x[1]], [foo(x)], 'ro'
    # )

    line1 = ax.plot(arr, f(arr), 'b-')
    _, _, *yborders = ax.axis()
    coords = (0, 0), yborders
    lines = ax.plot(
        *coords, 'g-',
        *coords, 'r-',
        *coords, 'g-.',
        *coords, 'r-.',
    )

    gen = update_all_x_data(lines, uniModMin.fib_search(f, (left, right), accuracy))


    def on_click(event):
        try:
            next(gen)
        except StopIteration:
            pass
        else:
            fig.canvas.flush_events()
            fig.canvas.draw()


    bnext = Button(pyplot.axes([0, 0, .1, .1]), 'Next')
    bnext.on_clicked(on_click)
    pyplot.show()
