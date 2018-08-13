def required(*fields):
    def decorator(func):
        def wrapped(self, *args, **kwargs):
            for field in fields:
                if getattr(self, field) is None:
                    class_name = self.__class__.__name__
                    msg = f'{class_name}: Absent value for `{field}`'
                    raise NotImplementedError(msg)
            return func(self, *args, **kwargs)
        return wrapped
    return decorator


def derive(*classes):
    return type('', classes, {})
