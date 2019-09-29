from os.path import dirname, abspath, join


project_path = dirname(dirname(dirname(abspath(__file__))))


def get_path(unit, lang):
    if unit == 'root':
        return join(project_path, 'modules', lang)

    return join(project_path, 'modules', lang, f'ru/{unit}')
