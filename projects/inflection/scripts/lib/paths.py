from os.path import dirname, abspath, join


project_path = dirname(dirname(dirname(abspath(__file__))))


def get_path(lang, noun=True):
    if noun:
        return join(project_path, 'modules', lang, 'ru/noun')
    else:
        return join(project_path, 'modules', lang)
