def parsed(func):
    def wrapped(self, *args, **kwargs):
        if self.is_parsing:
            raise Exception("Can't access an entry which is being parsing "
                            "right now.")
        if not self.parsed:
            self._parse()
        return func(self, *args, **kwargs)
    return wrapped


def parsing(func):
    def wrapped(self, *args, **kwargs):
        self.is_parsing = True
        result = func(self, *args, **kwargs)
        self.parsed = True
        self.is_parsing = False
        return result
    return wrapped
