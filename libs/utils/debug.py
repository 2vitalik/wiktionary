from core.conf import conf


def debug(func):
    def wrapped(self, *args, **kwargs):
        if conf.DEBUGGING:
            return func(self, *args, **kwargs)
    return wrapped
