from libs.parse.data.base import BaseData
from libs.parse.data.language import LanguageData
from libs.parse.utils.decorators import parsing


class PageData(BaseData):

    @parsing
    def _parse(self):
        self._sub_data = {}
        for lang, lang_section in self.base.sub_sections.items():
            self._sub_data[lang] = LanguageData(lang_section)
