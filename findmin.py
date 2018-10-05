#!/usr/bin/env python
from matplotlib import pyplot
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import axes3d, Axes3D
from typing import Iterable, Generator, Tuple
import numpy
import uniModMin

def updateAllXData(lines : Iterable[Line2D], gen : Generator[Tuple,None,None]) -> Generator[None,None,None]:
    for args in gen:
        for line, xdata in zip(lines, args):
            line.set_xdata(xdata)
        yield

if __name__ == '__main__':
    def f(x):
        return x**2 + 3*x

    accuracy = .005
    left, right = -10, 10
    arr = numpy.arange(left, right, accuracy / 10)

    # pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(1,2,1)

    def foo(x):
        x1, x2 = x[0], x[1]
        return 100 * (x2 - x1**2)**2 + (1 - x1)**2

    x = numpy.linspace(-6, 6, 30)
    y = numpy.linspace(-6, 6, 30)

    X, Y = numpy.meshgrid(x, y)
    Z = foo((X, Y))

    ax3d = fig.add_subplot(1,2,2, projection='3d')
    ax3d.plot_surface(X, Y, Z)

    line1, = ax.plot(arr, f(arr), 'b-') # Returns a tuple of line objects, thus the comma
    _, _, *yborders =  ax.axis()
    coords = (0,0), yborders
    line1, *lines = ax.plot(
        arr, f(arr), 'b-',
        *coords, 'g-',
        *coords, 'r-',
        *coords, 'g-.',
        *coords, 'r-.',
    )

    gen = updateAllXData(lines, uniModMin.fib_search(f, (left, right), accuracy))
    def on_click(event):
        try:
            next(gen)
        except StopIteration:
            pass
        else:
            fig.canvas.flush_events()
            fig.canvas.draw()

    bnext = Button(pyplot.axes([0,0,.1,.1]),'Next')
    bnext.on_clicked(on_click)
    pyplot.show()
    input()
