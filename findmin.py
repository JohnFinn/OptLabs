#!/usr/bin/env ipython
from matplotlib import pyplot
from matplotlib.widgets import Button
from matplotlib.lines import Line2D
import numpy, time, random
from counter import Counter
from typing import Tuple, Generator, Callable

Tffff = Tuple[float,float,float,float]
Tff = Tuple[float, float]
Cff = Callable[[float],float]
GTffff = Generator[Tffff,None,None]

def findmin(func:Cff, borders:Tff, accuracy:float)->GTffff:
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

def golden_ratio(func:Cff, borders:Tff, accuracy:float)->GTffff:
    a, b = borders
    leftGL = (3 - 5**.5)/2
    rightGR = (5**.5 - 1)/2
    x1 = a + leftGL * (b-a)
    x2 = a + rightGR * (b-a)
    yield a,b,x1,x2
    fx1 = func(x1)
    fx2 = func(x2)
    while b - a > accuracy:
        if fx1 > fx2:
            a, x1, fx1 = x1, x2, fx2
            x2 = a + rightGR * (b-a)
            fx2 = func(x2)
        elif fx2 > fx1:
            b, x2, fx2 = x2, x1, fx1
            x1 = a + leftGL * (b-a)
            fx1 = func(x1)
        yield a,b,x1,x2

def fib(n : int) -> int:
    return int((((1+5**.5)/2)**n-((1-5**.5)/2)**n)/5**.5)

def find_fib(borders:Tff, accuracy:float)->int:
    position = 10
    a, b = borders
    x = (a-b)/accuracy
    while fib(position) <= x:
        position *= 2
    return position

def fib_search(func:Cff, borders:Tff, accuracy:float)->GTffff:
    N = find_fib(borders, accuracy)
    fibN2, fibN1 = fib(N), fib(N-1)
    fibN  = fibN2 - fibN1
    a,b = borders
    c = (b-a)/fibN2
    x1, x2 = a + fibN * c, a + fibN1 * c
    fx1, fx2 = func(x1), func(x2)
    yield a, b, x1, x2
    while b - a > accuracy:
        fibN2, fibN1 = fibN1, fibN
        fibN = fibN2 - fibN1
        if fx1 < fx2:
            b, x2, fx2 = x2, x1, fx1
            x1 = a + fibN/fibN2 * (b-a)
            fx1 = func(x1)
        elif fx1 > fx2:
            a, x1, fx1 = x1, x2, fx2
            x2 = a + fibN1/fibN2 * (b-a)
            fx2 = func(x2)
        yield a, b, x1, x2

def updateAllXData(lines, gen):
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

    pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(arr, f(arr), 'b-') # Returns a tuple of line objects, thus the comma

    _, _, *yborders =  pyplot.axis()
    coords = (0,0), yborders
    lines = ax.plot(
        *coords, 'g-',
        *coords, 'y-',
        *coords, 'b-.',
        *coords, 'b-.',
    )

    gen = updateAllXData(lines, fib_search(f, (left, right), accuracy))
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
    input()
