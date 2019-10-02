from os.path import dirname, abspath, join


project_path = dirname(dirname(dirname(abspath(__file__))))


def get_path(lang, file, out=False, root=False):
    if root:
        return join(project_path, 'modules', lang)

    out_str = '.out' if out else ''
    return join(project_path, 'modules', lang, f'ru{out_str}', f'{file}.{lang}')
