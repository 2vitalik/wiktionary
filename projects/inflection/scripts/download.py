from libs.utils.io import write
from libs.utils.wikibot import load_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.modules import files, get_module_title
from projects.inflection.scripts.lib.paths import get_path

debug = False


def download_module(title, path):
    print(f'- {title}', end='')
    content = load_page(title) + '\n'
    content = content.replace("\n-- dev_prefix = 'User:Vitalik/'",
                              "\ndev_prefix = 'User:Vitalik/'")
    outs = ['', '.out'] if not debug else ['', ]
    for out in outs:
        write(path.replace('[.out]', out), content)
    print(' - OK')


def download(unit, dev=True):
    if not compare_dir(unit, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    path = get_path(unit, 'lua')
    print(f'Скачиваю lua-модули в папку:\n  {path}\nМодули:')

    for file in files:
        title = get_module_title(unit, file, dev)

        file = file.replace('[unit]', unit)
        download_module(title, f'{path}/{file}.lua')


if __name__ == '__main__':
    download('noun')
    # download('noun', dev=False)
