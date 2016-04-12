
def logging(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs, res
        return res
    return wrapper