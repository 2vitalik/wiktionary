import unicodedata


def char_info(char):
    category = unicodedata.category(char)
    try:
        name = unicodedata.name(char).split(' ')[0]
    except ValueError:
        name = 'UNKNOWN'
    return category, name
