import re

import regex


class H:
    headers = {
        'morphology': 'Морфологические и синтаксические свойства',
        'pronunciation': 'Произношение',
        'semantic': 'Семантические свойства',
        'definition': 'Значение',
        'synonyms': 'Синонимы',
        'antonyms': 'Антонимы',
        'hyperonyms': 'Гиперонимы',
        'hyponyms': 'Гипонимы',
        'related_words': 'Родственные слова',
        'etymology': 'Этимология',
        'phrases': 'Фразеологизмы и устойчивые сочетания',
        'translation': 'Перевод',
        'bibliography': 'Библиография',
    }
    morphology = headers['morphology']
    pronunciation = headers['pronunciation']
    semantic = headers['semantic']
    definition = headers['definition']
    synonyms = headers['synonyms']
    antonyms = headers['antonyms']
    hyperonyms = headers['hyperonyms']
    hyponyms = headers['hyponyms']
    related_words = headers['related_words']
    etymology = headers['etymology']
    phrases = headers['phrases']
    translation = headers['translation']
    bibliography = headers['bibliography']

    @staticmethod
    def get_key(header):
        for key, value in H.headers.items():
            if header == value:
                return key


class TP:  # Template Pattern
    base = '{{\s*(__RE__)\s*(?:\}\}|\|)'

    lang_header = '{{-(?P<lang>[-\w]+)-(?:\|[^}]*)?\}\}'
    homonym_header = '{{з(?:аголовок)?\|(?P<args>[^}]+)\}\}'

    any_1 = \
        regex.compile('({{\s*([^{|}]+)\s*[^{}]*\}\})')
    any_2 = \
        regex.compile('({{\s*([^{|}]+)\s*(?:[^{}]*{{[^{}]*\}\}[^{}]*)+\}\})')
    any_3 = \
        regex.compile('({{\s*([^{|}]+)\s*(?:[^{}]*{{(?:[^{}]*{{[^{}]*\}\}[^{}]*|[^{}]*)+\}\}[^{}]*)+\}\})')


class TR:  # Template Regex
    lang_header = re.compile(TP.lang_header)
    homonym_header = re.compile(TP.homonym_header)


class P:
    """
    Special useful regexp patters for parsing wiktionary pages
    """
    header = '^(={__N__} *(?P<header>[^=].*?[^=]) *={__N__} *)$'


class R:
    first_header = re.compile(P.header.replace('__N__', '1'), re.MULTILINE)
    second_header = re.compile(P.header.replace('__N__', '2'), re.MULTILINE)
    third_header = re.compile(P.header.replace('__N__', '3'), re.MULTILINE)
    fourth_header = re.compile(P.header.replace('__N__', '4'), re.MULTILINE)

    lang_header = re.compile(f'^(= *{TP.lang_header} *= *)$', re.MULTILINE)


def find_templates(content, only_content=False):
    for p in [TP.any_3, TP.any_2, TP.any_1]:
        templates = p.findall(content)
        for tpl in templates:
            if only_content:
                yield tpl[0]
            else:
                yield tpl

            # to avoid searching the same templates on the next iteration
            #  of the first loop: [TP.any_3, TP.any_2, TP.any_1]
            content = content.replace(tpl[0], '')
