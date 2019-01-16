from libs.utils.parse import remove_stress
from projects.inflection.modules.py.ru.noun.noun import forms


def replace_stress(value):
    return value.replace('́', "'")


def run(word, index):
    result = forms(remove_stress(word), {'индекс': index, 'слово': word}, None)

    keys = [
        ('Им.', 'nom-sg', 'nom-pl'),
        ('Р. ', 'gen-sg', 'gen-pl'),
        ('Д. ', 'dat-sg', 'dat-pl'),
        ('В. ', 'acc-sg', 'acc-pl'),
        ('Тв.', 'ins-sg', 'ins-pl'),
        ('Пр.', 'prp-sg', 'prp-pl'),
    ]

    len1 = 0
    len2 = 0
    for _, key1, key2 in keys:
        len1 = max(len1, len(result[key1]))
        len2 = max(len2, len(result[key2]))

    width = len1 + len2 + 11

    print()
    print(f'╔{"═" * width}╗')
    print(f'║ Слово:  {replace_stress(word)}{" " * (width-9-len(word))}║')
    print(f'║ Индекс: {index}{" " * (width-9-len(index))}║')
    print(f'╠═════╤═{"═" * len1}═╤═{"═" * len2}═╣')
    for key, key1, key2 in keys:
        print(f'║ {key} '
              f'│ {replace_stress(result[key1]).ljust(len1)} '
              f'│ {replace_stress(result[key2]).ljust(len2)} '
              f'║')
    print(f'╚═════╧═{"═" * len1}═╧═{"═" * len2}═╝')
    print()
