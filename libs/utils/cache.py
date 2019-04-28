

class Cache:
    def __init__(self, cache_size):
        self.keys = []
        self.cache = {}
        self.size = cache_size

    def get(self, key):
        if key in self.cache:
            return self.cache[key]

    def update(self, key, value):
        if len(self.cache) > self.size:
            remove_key = self.keys.pop(0)
            del self.cache[remove_key]
        self.cache[key] = value
        self.keys.append(key)

    def remove(self, key):
        del self.cache[key]
