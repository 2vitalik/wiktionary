from lib.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from lib.parse.groupers.sections.blocks.blocks import BlocksGrouper
from lib.parse.sections.grouper_mixins.sub_blocks import SubBlocksGroupersMixin
from lib.parse.utils.decorators import parsed


class BlocksGroupersMixin(SubBlocksGroupersMixin):
    @property
    @parsed
    def blocks(self):
        return BlocksGrouper(self)

    @parsed
    def any_blocks(self):
        return AnyBlocksGrouper(self)
