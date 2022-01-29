from libs.parse.tests.classes.groupers.section_groupers import HomonymsGrouper, \
    LanguagesGrouper, BlocksGrouper, SubBlocksGrouper, AnyBlocksGrouper


class SubBlocksGroupersMixin:
    def sub_blocks(self):
        return SubBlocksGrouper(self)  # передаётся section


class BlocksGroupersMixin(SubBlocksGroupersMixin):
    @property
    def blocks(self):
        return BlocksGrouper(self)  # передаётся section

    def any_blocks(self):
        return AnyBlocksGrouper(self)  # передаётся section


class HomonymsGroupersMixin(BlocksGroupersMixin):
    @property
    def homonyms(self):
        return HomonymsGrouper(self)  # передаётся section


class LanguagesGrouperMixin(HomonymsGroupersMixin):
    @property
    def languages(self):
        return LanguagesGrouper(self)  # передаётся section
