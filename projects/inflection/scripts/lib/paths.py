from os.path import dirname, abspath, join


project_path = dirname(dirname(dirname(abspath(__file__))))


def get_path(lang):
    return join(project_path, 'modules', lang, 'ru/noun')
