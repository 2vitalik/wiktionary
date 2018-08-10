from libs.parse.groupers.sections.blocks.any_blocks import AnyBlocksGrouper
from libs.parse.groupers.sections.blocks.blocks import BlocksGrouper
from libs.parse.sections.grouper_mixins.sub_blocks import SubBlocksGroupersMixin
from libs.parse.utils.decorators import parsed


class BlocksGroupersMixin(SubBlocksGroupersMixin):
    @property
    @parsed
    def blocks(self):
        return BlocksGrouper(self)

    @parsed
    def any_blocks(self):
        return AnyBlocksGrouper(self)
