from libs.parse.groupers.sections.languages import LanguagesGrouper
from libs.parse.sections.grouper_mixins.homonyms import HomonymsGroupersMixin
from libs.parse.utils.decorators import parsed


class LanguagesGrouperMixin(HomonymsGroupersMixin):
    @property
    @parsed
    def languages(self):
        return LanguagesGrouper(self)
