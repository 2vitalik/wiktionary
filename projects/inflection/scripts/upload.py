from libs.utils.io import read, append
from libs.utils.wikibot import save_page
from projects.inflection.scripts.lib.modules import files, get_module_title
from projects.inflection.scripts.lib.paths import get_path


def process_desc(desc):
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
    append('logs/changes.txt',
           f'v{ru_noun_version}/{inflection_version}: {desc}')
    return desc


def read_file(dev, filename):
    result = read(filename).replace('\r', '')
    if not dev:
        result = result.replace("\ndev_prefix = 'User:Vitalik/'",
                                "\n-- dev_prefix = 'User:Vitalik/'")
    return result


def upload(dev, ru_noun_version, inflection_version, desc):
    desc = process_desc(desc)

    path = get_path('lua')
    print(f'Загружаю lua-модули в ВС:')

    for file in files:
        title = get_module_title(file, dev)
        print(f'- {title} - ', end='')

        file = file.replace('[.out]', '.out')
        if save_page(title, read_file(dev, f'{path}/{file}.lua'),
                     f'v{ru_noun_version}: {desc}'):
            print('OK')


if __name__ == '__main__':
    # dev = False
    dev = True
    ru_noun_version = '3.4.5'
    inflection_version = '2.2.3'
    desc = 'b'

    upload(dev, ru_noun_version, inflection_version, desc)
