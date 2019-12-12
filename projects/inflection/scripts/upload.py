from libs.utils.dt import dt
from libs.utils.io import read, append
from libs.utils.wikibot import save_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.files import files, get_module_title
from projects.inflection.scripts.lib.paths import get_path


def process_desc(dev, desc):
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
    append('logs/changes.txt', f'[{dt()}] [{d}] {new_desc}')
    return desc


def read_file(dev, filename):
    result = read(filename).replace('\r', '')
    if not dev:
        result = result.replace("\ndev_prefix = 'User:Vitalik/'",
                                "\n-- dev_prefix = 'User:Vitalik/'")
    return result


def upload(dev, version, desc):
    if not compare_dir(dev, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    desc = process_desc(dev, desc)

    print(f'Загружаю lua-модули в ВС:')

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


if __name__ == '__main__':
    # inflection_version = '2.4'

    # dev = False
    dev = True

    version = '3.9.10'
    desc = 'Исправление для "умён" (звёздочка для кратких b)'

    print(f'v{version}: {desc}')
    upload(dev, version, desc)


# todo: почистить старые неиспользуемые модули на ВС (старые имена)
