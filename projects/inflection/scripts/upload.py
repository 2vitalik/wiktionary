from libs.utils.dt import dt
from libs.utils.io import read, append
from libs.utils.wikibot import save_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.modules import files, get_module_title
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
    append('logs/changes.txt',
           f'[{dt()}] [{d}] v{version}/{inflection_version}: {desc}')
    return desc


def read_file(dev, filename):
    result = read(filename).replace('\r', '')
    if not dev:
        result = result.replace("\ndev_prefix = 'User:Vitalik/'",
                                "\n-- dev_prefix = 'User:Vitalik/'")
    return result


def upload(dev, unit, version, inflection_version, desc):
    if not compare_dir(unit, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    desc = process_desc(dev, desc)

    path = get_path(unit, 'lua')
    print(f'Загружаю lua-модули в ВС:')

    for file in files:
        title = get_module_title(unit, file, dev)
        print(f'- {title} - ', end='')

        file = file.replace('[unit]', unit)
        file = file.replace('[.out]', '.out')
        if save_page(title, read_file(dev, f'{path}/{file}.lua'),
                     f'v{version}: {desc}'):
            print('OK')

    dev_prefix = 'User:Vitalik/' if dev else ''
    title = f'Module:{dev_prefix}inflection/tools'
    path = get_path('root', 'lua')
    save_page(title, read_file(dev, f'{path}/tools.lua'),
              f'v{inflection_version}: {desc}')


if __name__ == '__main__':
    # dev = False
    dev = True

    inflection_version = '2.3'

    # unit = 'noun'
    # version = '3.5.16'

    unit = 'adj'
    version = '0.1.4'

    desc = 'b'

    upload(dev, unit, version, inflection_version, desc)
