from lib.parse.groupers.sections.blocks.sub_blocks import SubBlocksGrouper
from lib.parse.utils.decorators import parsed


class SubBlocksGroupersMixin:
    @parsed
    def sub_blocks(self):
        return SubBlocksGrouper(self)
