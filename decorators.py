import functools
import collections


def logging(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs, res
        return res
    return wrapper


def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            print "not in cache"
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer
