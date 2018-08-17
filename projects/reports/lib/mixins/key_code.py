from libs.utils.wikicode import nowiki_code


class KeyCode:
    @classmethod
    def convert_key(cls, key):
        return nowiki_code(key)
