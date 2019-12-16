from os.path import exists

from pywikibot import NoPage

from libs.utils.io import write, read
from libs.utils.wikibot import load_page
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.files import declension_files, \
    get_module_title, testcases_files, get_docs_title, tpl_files, get_tpl_title
from projects.inflection.scripts.lib.paths import get_path


def download_page(title, path):
    print(f'- {title}', end='')
    try:
        content = load_page(title) + '\n'
    except NoPage:
        print(' - No page')
        return
    content = content.replace("\n-- dev_prefix = 'User:Vitalik/'",
                              "\ndev_prefix = 'User:Vitalik/'")
    if exists(path):
        old_content = read(path)
        if old_content != content:
            print(' - OK')
        else:
            write(path, content)
            print(' - Not changed')
    else:
        write(path, content)
        print(' - NEW')


def download_lua(dev, testcases=False):
    if not compare_dir(dev, 'lua'):
        print('Ошибка: папки `lua` не синхронизированы.')
        return

    path = get_path(dev, 'lua', '', root=True)
    print(f'Скачиваю lua-модули в папку:\n  {path}\nМодули:')

    files = testcases_files if testcases else declension_files
    for file in files:
        title = get_module_title(file, dev)
        filename = get_path(dev, 'lua', file, '')
        download_page(title, filename)


def download_docs(dev):
    path = get_path(dev, 'docs', '', root=True)
    print(f'Скачиваю документацию в папку:\n  {path}\nШаблоны:')

    files = declension_files + testcases_files
    for file in files:
        title = get_docs_title(file, dev)
        filename = get_path(dev, 'docs', file, '')
        download_page(title, filename)


def download_tpls(dev):
    path = get_path(dev, 'tpl', '', root=True)
    print(f'Скачиваю шаблоны в папку:\n  {path}\nШаблоны:')

    for file in tpl_files:
        title = get_tpl_title(file, dev)
        filename = get_path(dev, 'tpl', file, '')
        download_page(title, filename)
