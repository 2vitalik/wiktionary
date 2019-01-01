from os.path import join
from shutil import copy

from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.modules import files
from projects.inflection.scripts.lib.paths import get_path


def clear_out_dir(lang):
    py_path = get_path(lang)

    for module in files:
        active = module.replace('[.out]', '')
        out = module.replace('[.out]', '.out')

        # Копирование результата в `libs.out`:
        copy(join(py_path, f'{active}.{lang}'),
             join(py_path, f'{out}.{lang}'))

    if not compare_dir(lang):
        print(f'Ошибка: папки `{lang}` не синхронизированы.')
        return
