def parsed(func):
    """This decorator makes sure, that before this func is called, the class is parsed.
    If it is not parsed, parsing is lazily executed for this BaseSection"""
    def wrapped(self, *args, **kwargs):
        if self.is_parsing:
            raise Exception("Can't access an entry which is being parsing "
                            "right now.")
        if not self.parsed:
            self._parse()
        return func(self, *args, **kwargs)
    return wrapped


def parsing(func):
    """Decorator that marks parser code for this class. The func parses the class and its children (not recursively)"""
    def wrapped(self, *args, **kwargs):
        self.is_parsing = True
        result = func(self, *args, **kwargs)
        self.parsed = True
        self.is_parsing = False
        return result
    return wrapped
