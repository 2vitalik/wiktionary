import functools

from projects.inflection.modules.dev.dev_py import tools as _


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def __getattr__(self, item):
        # print(f"Error: AttrDict doesn't have attribute: \"{item}\"")
        return

    def copy(self):
        return AttrDict(self.__dict__)


# class Dict(dict):
#     # def __init__(self, **kwargs):
#     #     for key, value in kwargs:
#     #         setattr(self, key, value)
#
#     class AttributeDict(dict):
#         __getattr__ = dict.__getitem__
#         __setattr__ = dict.__setitem__
#
#     # def __getattr__(self, item):
#     #     return


# TODO: или использовать просто `object` в тех местах?

# todo: log -- который выводит на mw.log только если режим дебага?


def table_len(table):
    return len(table)


class syllables:
    @staticmethod
    def get_syllables(value):
        return value  # todo?


def starts(module):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            function = f.__name__
            _.starts(module, function)
            return f(function, *args, **kwargs)
        return wrapper
    return decorator


def call(module):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            function = f.__name__
            _.call(module, function)
            return f(*args, **kwargs)
        return wrapper
    return decorator
