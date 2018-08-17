
class BaseFetcher:
    slug = None  # should be set in inheritors

    def __init__(self, processor_class):
        self.processor = processor_class(self.slug)
