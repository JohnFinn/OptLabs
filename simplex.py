from typing import List, Iterable, Callable, VT, KT
from linear_function import LinearFunction
from numpy import inf


class Slack(int):
    pass


class Helper:
    def __init__(self, x: int, slack: int):
        self.x = list(range(x))
        self.slack = list(map(Slack, range(slack)))

    def __call__(self, arg_number, index):
        self.x[arg_number], self.slack[index] = self.slack[index], self.x[arg_number]

    def get_result(self) -> Iterable[int]:
        for index, x in enumerate(self.slack):
            if not isinstance(x, Slack):
                yield index, x


def maximize(constraints: List[LinearFunction], objective_fn: LinearFunction) -> List[float]:
    """
    >>> from linear_function import LinearFunction
    >>> from numpy import array
    >>> constraints = [                                                                             \
        LinearFunction(18, [-2, -1, -1]),                                                           \
        LinearFunction(30, [-1, -2, -2]),                                                           \
        LinearFunction(24, [-2, -2, -2]),                                                           \
    ]
    >>> objective_fn = LinearFunction(0, [6, 5, 4])
    >>> maximize(constraints, objective_fn)
    [Fraction(6, 1), Fraction(6, 1), 0]
    >>>
    >>>
    >>> A = [                                                                                       \
        [1, 2, -1, 2, 4],                                                                           \
        [0, -1, 2, 1, 3],                                                                           \
        [1, -3, 2, 2, 0],                                                                           \
    ]
    >>> b = [1, 3, 4]
    >>> c = [1, -3, 2, 1, 4]
    >>> constraints = [LinearFunction(free, -array(coefs)) for coefs, free in zip(A, b)]
    >>> objective_fn = LinearFunction(0, c)
    >>> maximize(constraints, objective_fn)
    [Fraction(26, 17), 0, Fraction(21, 17), 0, Fraction(3, 17)]
    """
    h = Helper(len(objective_fn.coefs), len(constraints))
    while any(map(lambda x: x > 0, objective_fn.coefs)):
        pivot(constraints, objective_fn, h)
    res = [0 for i in objective_fn.coefs]
    for index, n in h.get_result():
        res[n] = constraints[index].free
    return res


def do_nothing(*args, **kwargs):
    pass


def _pivot(constraints: List[LinearFunction], objective_fn: LinearFunction) -> None:
    pivot(constraints, objective_fn, do_nothing)


def pivot(constraints: List[LinearFunction], objective_fn: LinearFunction, callback: Callable[[int, int], None]) -> None:
    """
    >>> from linear_function import LinearFunction
    >>> constraints = [                                                         \
        LinearFunction(18, [-2, -1, -1]),                                       \
        LinearFunction(30, [-1, -2, -2]),                                       \
        LinearFunction(24, [-2, -2, -2]),                                       \
    ]
    >>> objective_fn = LinearFunction(0, [6, 5, 4])
    >>> _pivot(constraints, objective_fn)
    >>> print(objective_fn)
    54 + -3*x₀ + 2*x₁ + 1*x₂
    >>> for i in constraints: print(i)
    9 + -1/2*x₀ + -1/2*x₁ + -1/2*x₂
    21 + 1/2*x₀ + -3/2*x₁ + -3/2*x₂
    6 + 1*x₀ + -1*x₁ + -1*x₂
    """
    arg_number = first_index(objective_fn.coefs, lambda x: x > 0)
    index = tightest_constraint(constraints, arg_number)
    assert -constraints[index].free / constraints[index].coefs[arg_number] > 0
    constraints[index].rearrange(arg_number)
    for c in skip_at(constraints, index):
        c.substitute(arg_number, constraints[index])
    objective_fn.substitute(arg_number, constraints[index])
    callback(arg_number, index)


def tightest_constraint(constraints: List[LinearFunction], index: int) -> int:
    """
    >>> from linear_function import LinearFunction
    >>> constraints = [                                                         \
        LinearFunction(18, [-2, -1, -1]),                                       \
        LinearFunction(30, [-1, -2, -2]),                                       \
        LinearFunction(24, [-2, -2, -2]),                                       \
    ]
    >>> tightest_constraint(constraints, 1)
    2
    """
    def selector(x: LinearFunction):
        value = x.coefs[index]
        if value == 0 or same_sign(value, x.free):
            return inf
        return -x.free/value
    return min_index(constraints, key=selector)


def same_sign(a, b):
    """
    >>> same_sign(1, 1)
    True
    >>> same_sign(1, -1)
    False
    >>> same_sign(-1, -1)
    True
    >>> same_sign(-1, 1)
    False
    """
    return (a > 0) == (b > 0)



def min_index(sequence: Iterable[VT], key: Callable[[VT], KT]) -> int:
    """
    >>> min_index(range(2), key=lambda x: -x)
    1
    """
    return min(enumerate(sequence), key=lambda x: key(x[1]))[0]


def first_index(sequence: Iterable[VT], selector: Callable[[VT], bool]) -> int:
    return first(enumerate(sequence), lambda x: selector(x[1]))[0]


def first(sequence: Iterable[VT], selector: Callable[[VT], bool]) -> VT:
    for item in sequence:
        if selector(item):
            return item
    raise RuntimeError("No selected item in sequence")


def skip_at(sequence: Iterable[VT], index: int) -> Iterable[VT]:
    for i, item in enumerate(sequence):
        if index != i:
            yield item
