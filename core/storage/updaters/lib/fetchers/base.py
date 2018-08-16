
class BaseFetcher:
    slug = None  # should be set in inheritors

    def __init__(self, processor):
        self.processor = processor
        self.processor.slug = self.slug
