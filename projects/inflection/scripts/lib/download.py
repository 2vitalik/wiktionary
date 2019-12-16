from pywikibot import NoPage

from libs.utils.io import write
from libs.utils.wikibot import load_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.files import declension_files, \
    get_module_title, testcases_files, get_docs_title
from projects.inflection.scripts.lib.paths import get_path

debug = False


def download_module(title, path):
    print(f'- {title}', end='')
    try:
        content = load_page(title) + '\n'
    except NoPage:
        print(' - No page')
        return
    content = content.replace("\n-- dev_prefix = 'User:Vitalik/'",
                              "\ndev_prefix = 'User:Vitalik/'")
    outs = ['', '.out'] if not debug else ['', ]
    for out in outs:
        write(path.replace('[.out]', out), content)
    print(' - OK')


def download(dev, testcases=False):
    if not compare_dir(dev, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    path = get_path(dev, 'lua', '', root=True)
    print(f'Скачиваю lua-модули в папку:\n  {path}\nМодули:')

    files = testcases_files if testcases else declension_files
    for file in files:
        title = get_module_title(file, dev)
        filename = get_path(dev, 'lua', file, '')
        download_module(title, filename)


def download_docs(dev):
    path = get_path(dev, 'docs', '', root=True)
    print(f'Скачиваю документацию в папку:\n  {path}\nМодули:')

    files = declension_files + testcases_files
    for file in files:
        title = get_docs_title(file, dev)
        filename = get_path(dev, 'docs', file, '')
        download_module(title, filename)
