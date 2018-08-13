from libs.utils.wikicode import nowiki_code


class ValueCode:
    @classmethod
    def convert_value(cls, value):
        return nowiki_code(value)
