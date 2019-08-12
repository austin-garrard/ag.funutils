import functools

def chain(initial, *transforms):
    return functools.reduce(
        lambda prev_result, next_transform: next_transform(prev_result),
        transforms,
        initial
    )

built_in_map = map
def map(transform):
    return functools.partial(built_in_map, transform)

def reduce(transform, initial = None):
    if initial is None:
        return lambda iterable: functools.reduce(transform, iterable)
    else:
        return lambda iterable: functools.reduce(transform, iterable, initial)

built_in_filter = filter
def filter(condition):
    return functools.partial(built_in_filter, condition)

def sort(key = None, reverse = False):
    return lambda iterable: sorted(iterable, key=key, reverse=reverse)
