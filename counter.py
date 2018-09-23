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
