from lib.parse.groupers.sections.languages import LanguagesGrouper
from lib.parse.sections.grouper_mixins.homonyms import HomonymsGroupersMixin
from lib.parse.utils.decorators import parsed


class LanguagesGrouperMixin(HomonymsGroupersMixin):
    @property
    @parsed
    def languages(self):
        return LanguagesGrouper(self)
