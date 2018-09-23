#!/usr/bin/env python
from matplotlib import pyplot
import numpy, time, random

class Counter:
    '''
    >>> @Counter
    ... def foo():pass
    >>> @Counter
    ... def bar():pass
    >>> foo.count, bar.count
    (0, 0)
    >>> foo()
    >>> foo.count, bar.count
    (1, 0)
    >>> foo()
    >>> foo.count, bar.count
    (2, 0)
    >>> bar()
    >>> foo.count, bar.count
    (2, 1)
    '''
    def __init__(self, func):
        self.count = 0
        self.func = func
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        self.func(*args, **kwargs)


def findmin(func, borders, accuracy):
    delta = accuracy / 3
    a, b = borders
    while b - a > accuracy:
        x = (a + b) / 2
        x1, x2 = x - delta, x + delta
        yield a, b,x1,x2
        fx1, fx2 = func(x1), func(x2)
        if fx1 > fx2:
            a = x1
        elif fx1 < fx2:
            b = x2

def golden_ratio(func, borders, accuracy):
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
            a = x1
            x1 = x2
            fx1 = fx2
            x2 = a + rightGR * (b-a)
            fx2 = func(x2)
        elif fx2 > fx1:
            b = x2
            x2 = x1
            fx2 = fx1
            x1 = a + leftGL * (b-a)
            fx1 = func(x1)
        yield a,b,x1,x2

def fib(n):
    return int((((1+5**.5)/2)**n-((1-5**.5)/2)**n)/5**.5)

def find_fib(borders, accuracy):
    position = 10
    a, b = borders
    x = (a-b)/accuracy
    while fib(position) <= x:
        position *= 2
    return position

def fib_search(func, borders, accuracy):
    N = find_fib(borders, accuracy)
    fibN2, fibN1 = fib(N), fib(N-1)
    fibN  = fibN2 - fibN1
    a,b = borders
    c = (b-a)/fibN2
    x1, x2 = a + fibN * c, a + fibN1 * c
    fx1, fx2 = func(x1), func(x2)
    yield a,b,x1,x2
    while True:
        fibN2, fibN1 = fibN1, fibN
        fibN = fibN2 - fibN1
        c = (b-a)/fibN2
        if fx1 < fx2:
            b = x2
            x2, fx2 = x1, fx1
            x1 = a + fibN * c
            fx1 = func(x1)
        elif fx1 > fx2:
            a = x1
            x1, fx1 = x2, fx2
            x2 = a + fibN1 * c
            fx2 = func(x2)
        yield a, b, x1, x2


if __name__ == '__main__':
    def f(x):
        return x**2 + 3*x

    accuracy = .005
    left, right = -10, 10
    
    step = accuracy / 10 # for drawing 
    arr = numpy.arange(left, right, step)
    # res = pyplot.plot(arr, f(arr))

    pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    line1, = ax.plot(arr, f(arr), 'b-') # Returns a tuple of line objects, thus the comma
    xxx1, = ax.plot((left, left), (-10,200), 'b-.')
    xxx2, = ax.plot((left, left), (-10,200), 'b-.')
    left_border, = ax.plot((left, left), (-10,200), 'g-')
    right_border, = ax.plot((right, right), (-10,200), 'y-')
    for new_left, new_right,x1,x2 in golden_ratio(f, (left, right), accuracy):
        # line1.set_ydata(numpy.sin(x + phase))
        # line2, = ax.plot(x, f(x), 'ro')
        xxx1.set_xdata(x1)
        xxx2.set_xdata(x2)
        left_border.set_xdata(new_left)
        right_border.set_xdata(new_right)
        fig.canvas.draw()
        fig.canvas.flush_events()
        input()
