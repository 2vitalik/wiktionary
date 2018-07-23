from lib.parse.groupers.sections.homonyms import HomonymsGrouper
from lib.parse.sections.grouper_mixins.blocks import BlocksGroupersMixin
from lib.parse.utils.decorators import parsed


class HomonymsGroupersMixin(BlocksGroupersMixin):
    @property
    @parsed
    def homonyms(self):
        return HomonymsGrouper(self)
