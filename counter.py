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
        return self.func(*args, **kwargs)


class IterCounter:
    def __init__(self, gen):
        self.gen = gen
        self.count = 0

    def __next__(self):
        res = next(self.gen)
        self.count += 1
        return res

    def __iter__(self):
        self.count = 0
        return self
