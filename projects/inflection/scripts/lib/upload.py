from libs.utils.dt import dt
from libs.utils.io import append, read
from libs.utils.wikibot import save_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.files import declension_files, \
    get_module_title, testcases_files
from projects.inflection.scripts.lib.paths import get_path


def process_desc(dev, version, desc):
    if not desc:
        desc = input('Input description: ')
    replaces = {
        'b': 'bug-fix',
        'f': 'fix',
        'c': 'comments',
        'd': 'debug',
        'm': 'minor changes',
        'r': 'refactoring',
        't': 'testing',
        'v': 'increase version',
    }
    desc = replaces.get(desc, desc)
    if not desc:
        raise Exception('Description is required')
    d = 'D' if dev else 'P'
    new_desc = f'v{version}: {desc}'
    print(new_desc)
    append('../logs/changes.txt', f'[{dt()}] [{d}] {new_desc}')
    return desc


def read_file(dev, filename):
    result = read(filename).replace('\r', '')
    if not dev:
        result = result.replace("\ndev_prefix = 'User:Vitalik/'",
                                "\n-- dev_prefix = 'User:Vitalik/'")
    return result


def upload(version, desc, dev, testcases=False):
    if not compare_dir(dev, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    desc = process_desc(dev, version, desc)

    print(f'Загружаю lua-модули в ВС:')

    files = testcases_files if testcases else declension_files
    for file in files:
        title = get_module_title(file, dev)
        print(f'- {title} - ', end='')

        path = get_path(dev, 'lua', file, out=True)
        if save_page(title, read_file(dev, path), f'v{version}: {desc}'):
            print('OK')

    # todo: fixme, and move to separate function! with separate logs/changes
    # dev_prefix = 'User:Vitalik/' if dev else ''
    # title = f'Module:{dev_prefix}inflection/tools'
    # path = get_path('lua', root=True)  # todo: fixme
    # save_page(title, read_file(dev, f'{path}/tools.lua'),
    #           f'v{inflection_version}: {desc}')
