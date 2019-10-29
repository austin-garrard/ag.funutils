import functools

def chain(initial, *transforms, just, none):
    def maybe(prev_result, next_transform):
        if prev_result is None:
            return None
        else:
            return next_transform(prev_result)

    result = functools.reduce(maybe, transforms, initial)

    if result is None:
        if callable(none):
            return none()
        else:
            return none
    else:
        if callable(just):
            return just(result)
        else:
            return just

