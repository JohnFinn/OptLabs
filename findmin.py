#!/usr/bin/env python
from matplotlib import pyplot
import numpy, time, random

def findmin(func, borders, accuracy):
    delta = accuracy / 3
    a, b = borders
    while b - a > accuracy:
        x = (a + b) / 2
        yield x
        x1, x2 = x - delta, x + delta
        fx1, fx2 = func(x1), func(x2)
        if fx1 > fx2:
            a = x1
        elif fx1 < fx2:
            b = x2

if __name__ == '__main__':
    def f(x):
        return x**2 + 3*x
    
    accuracy = .5
    left, right = -10, 10
    
    step = accuracy / 10 # for drawing 
    arr = numpy.arange(left, right, step)
    # res = pyplot.plot(arr, f(arr))

    pyplot.ion()
    fig = pyplot.figure()
    ax = fig.add_subplot(111)

    line1, = ax.plot(arr, f(arr), 'b-') # Returns a tuple of line objects, thus the comma
    for x in findmin(f, (left, right), accuracy):
        # line1.set_ydata(numpy.sin(x + phase))
        line2, = ax.plot(x, f(x), 'ro')
        fig.canvas.draw()
        fig.canvas.flush_events()
        input()
