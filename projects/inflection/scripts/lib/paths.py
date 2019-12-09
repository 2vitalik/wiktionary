from os.path import dirname, abspath, join


project_path = dirname(dirname(dirname(abspath(__file__))))


def get_path(dev, lang, file, out=False, root=False):
    dev_str = 'dev' if dev else 'prod'
    if root:
        return join(project_path, 'modules', dev_str, lang)

    out_str = '.out' if out else ''
    return join(project_path, 'modules', dev_str, lang, f'ru{out_str}',
                f'{file}.{lang}')
