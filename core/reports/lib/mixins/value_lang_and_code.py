from libs.utils.wikicode import nowiki_code, bold


class ValueLangAndCode:
    @classmethod
    def convert_value(cls, lang_and_value):
        lang, value = lang_and_value
        return f'{bold(lang)}:{nowiki_code(value)}'
