from libs.parse.tests.classes.groupers.base_groupers import BaseSectionsGrouper


class LanguagesGrouper(BaseSectionsGrouper):
    ...


class HomonymsGrouper(BaseSectionsGrouper):
    ...


class EmptyBaseSectionsGrouper(BaseSectionsGrouper):
    ...


class BaseBlocksGrouper(BaseSectionsGrouper):
    ...


class BlocksGrouper(BaseBlocksGrouper):  # from base blocks
    ...


class SubBlocksGrouper(BaseBlocksGrouper):  # from base blocks
    ...


class AnyBlocksGrouper(BaseBlocksGrouper):  # from base blocks
    ...
