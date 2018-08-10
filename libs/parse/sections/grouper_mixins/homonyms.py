from libs.parse.groupers.sections.homonyms import HomonymsGrouper
from libs.parse.sections.grouper_mixins.blocks import BlocksGroupersMixin
from libs.parse.utils.decorators import parsed


class HomonymsGroupersMixin(BlocksGroupersMixin):
    @property
    @parsed
    def homonyms(self):
        return HomonymsGrouper(self)
