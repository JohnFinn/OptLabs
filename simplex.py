from typing import List, Iterable, Callable, VT, KT
from linear_function import LinearFunction


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
    >>> constraints = [                                                         \
        LinearFunction(18.0, [-2.0, -1.0, -1.0]),                               \
        LinearFunction(30.0, [-1.0, -2.0, -2.0]),                               \
        LinearFunction(24.0, [-2.0, -2.0, -2.0]),                               \
    ]
    >>> objective_fn = LinearFunction(0.0, [6.0, 5.0, 4.0])
    >>> maximize(constraints, objective_fn)
    [6.0, 6.0, 0]
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
        LinearFunction(18.0, [-2.0, -1.0, -1.0]),                               \
        LinearFunction(30.0, [-1.0, -2.0, -2.0]),                               \
        LinearFunction(24.0, [-2.0, -2.0, -2.0]),                               \
    ]
    >>> objective_fn = LinearFunction(0.0, [6.0, 5.0, 4.0])
    >>> _pivot(constraints, objective_fn)
    >>> print(objective_fn)
    54.0 + -3.0*x₀ + 2.0*x₁ + 1.0*x₂
    >>> for i in constraints: print(i)
    9.0 + -0.5*x₀ + -0.5*x₁ + -0.5*x₂
    21.0 + 0.5*x₀ + -1.5*x₁ + -1.5*x₂
    6.0 + 1.0*x₀ + -1.0*x₁ + -1.0*x₂
    """
    arg_number = first_index(objective_fn.coefs, lambda x: x > 0)
    index = tightest_constraint(constraints, arg_number)
    constraints[index].rearrange(arg_number)
    for c in skip_at(constraints, index):
        c.substitute(arg_number, constraints[index])
    objective_fn.substitute(arg_number, constraints[index])
    callback(arg_number, index)


def tightest_constraint(constraints: List[LinearFunction], index: int) -> int:
    """
    >>> from linear_function import LinearFunction
    >>> constraints = [                                                         \
        LinearFunction(18.0, [-2.0, -1.0, -1.0]),                               \
        LinearFunction(30.0, [-1.0, -2.0, -2.0]),                               \
        LinearFunction(24.0, [-2.0, -2.0, -2.0]),                               \
    ]
    >>> tightest_constraint(constraints, 1)
    2
    """
    return min_index(constraints, key=lambda x: -x.free/x.coefs[index])


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
