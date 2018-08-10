from libs.parse.groupers.sections.blocks.sub_blocks import SubBlocksGrouper
from libs.parse.utils.decorators import parsed


class SubBlocksGroupersMixin:
    @parsed
    def sub_blocks(self):
        return SubBlocksGrouper(self)
