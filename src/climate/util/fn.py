import re
from collections.abc import Iterable
from functools import reduce, partial
from operator import iconcat
from typing import Tuple, List, Any

from returns.curry import curry
from returns.maybe import Nothing, Some, Maybe
from returns.pipeline import flow

"""
Common functions
"""


def identity(arg):
    return arg


def deep_get(data: dict, path: list[str], default: Any = None) -> Any:
    """
    Takes a Dict, a path into the Dict as a list, and a default if nothing found, and returns the item at the path.
    Note, only works for a nested Dict, no Lists are supported.
    Example:
        $ deep_get({'a': {'b': 1}}, ['a', 'b'], 0)
    """
    if not isinstance(path, Iterable):
        return None
    fst, rst = first(path), rest(path)
    if fst not in data: return default
    if (fst in data) and len(rst) == 0: return data[fst]
    return deep_get(data[fst], rst, default)


def fst_rst(iterable: list) -> Tuple:
    return (first(iterable), rest(iterable))


def rest(iterable):
    return iterable[1:]


def partial_first(iterable):
    return first(iterable)


def first(iterable, default=None, key=None):
    """
    Return first element of `iterable` that evaluates true, else return None
    (or an optional default value).
    >>> first([0, False, None, [], (), 42])
    42
    >>> first([0, False, None, [], ()]) is None
    True
    >>> first([0, False, None, [], ()], default='ohai')
    'ohai'
    >>> import re
    >>> m = first(re.match(regex, 'abc') for regex in ['b.*', 'a(.*)'])
    >>> m.group(1)
    'bc'
    The optional `key` argument specifies a one-argument predicate function
    like that used for `filter()`.  The `key` argument, if supplied, must be
    in keyword form.  For example:
    >>> first([1, 1, 3, 4, 5], key=lambda x: x % 2 == 0)
    4
    """
    if key is None:
        for el in iterable:
            if el:
                return el
    else:
        for el in iterable:
            if key(el):
                return el
    return default


def find_by_type(type, iterable):
    return partial_filter(type_predicate(type), iterable).then(partial_first)


def find_by_predicate(predicate_fn: callable, iterable: list):
    return partial_filter(predicate_fn, iterable).then(partial_first)


def type_predicate(type):
    return lambda x: x['_type'] == type


def partial_filter(fn: callable, iterable: list):
    return Some(list(filter(fn, iterable)))


def find_by_filter(fn, xs):
    return next(filter(fn, xs), None)


def find(fn, xs):
    """
    fn.find(fn.equality(fn.at('a')), '1', [{'a': '1'}])
    """
    return next(select(fn, xs), None)


def maybe_find(fn, xs):
    result = find(fn, xs)
    if result:
        return Some(result)
    return Nothing


@curry
def maybe_get[T](struct: dict[T], key) -> Maybe[T]:
    result = struct.get(key, None)
    if result:
        return Some(result)
    return Nothing


def select(fn: callable, xs: list) -> filter:
    """
    returns all values from the list that are true when applying the fn to the item
    """
    return filter(fn, xs)


# + field_fn; the property to extract from the record.  Either a String or a Function which takes the record
# + test_value; the value which has == applied to determine equality
# + i; the record under test
# e.g. equality('a', "equal")({'a': "equal"})
# e.g. equality.(test_fn).("equal")({'a': "equal"})) ; where test_fn is -> x { x[:a] }
@curry
def equality(field_or_fn, test_value, i):
    if callable(field_or_fn):
        return field_or_fn(i) == test_value
    else:
        return i[field_or_fn] == test_value


@curry
def at(x, i):
    if x is None:
        return None

    if x not in i:
        return None

    return i[x]


@curry
def at_index[T](idx: int, xs: Iterable[T]) -> T:
    """
    A Curried function which takes an index and a type which can be indexed into (list or tuple)
    and returns the item at that index.

    >>> at_1 = at_index(1)
    >>> at_1([1,2,3,4])
    
    :param idx:
    :param xs:
    :return:
    """
    if xs is None or len(xs) < idx + 1:
        return None
    return xs[idx]


def match(pattern, test_string):
    return re.match(pattern, test_string)


# Curryed fn that removes elements from a collection where f.(e) is true
@curry
def remove(fn: callable, xs: list) -> List:
    return list(filter(partial(negated_fn, fn), xs))


def negated_fn(fn: callable, x):
    return not fn(x)


def remove_none(xs):
    return list(filter(identity, xs))


def not_empty(xs: list[Any]) -> bool:
    return len(xs) > 0


def only_one(xs: list[Any]) -> bool:
    return len(xs) == 1


def bool_fn_with_predicate(xs, bool_fn, predicate):
    """
    Applies a bool fn over a list which is converted to bool through the predicate.
    The bool_fn can be anything which works with a list[bool]; like any, all
    > bool_fn_with_predicate([monad.Right(1), monad.Left(2)], any, monad.maybe_value.ok)
    """
    return bool_fn(map(predicate, xs))


def compose_iter(fn_list: list, initial_val):
    return flow(initial_val, *fn_list)


def either_compose(fn_list: list, initial_val):
    return reduce(lambda m, fn: m.bind(fn), fn_list, initial_val)


def flatten(xs: list):
    return reduce(iconcat, xs, [])
