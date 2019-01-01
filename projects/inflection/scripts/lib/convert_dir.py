from os.path import join
from shutil import copy

from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.convert_file import convert_file
from projects.inflection.scripts.lib.modules import files
from projects.inflection.scripts.lib.paths import get_path


def convert_dir(_from, _to):
    if not compare_dir(_to):
        print(f'Ошибка: папки `{_to}` не синхронизированы.')
        return

    py_path = get_path(_to)

    for module in files:
        active = module.replace('[.out]', '')
        out = module.replace('[.out]', '.out')

        # Прямое преобразование:
        convert_file(active, _from, _to)

        # Копирование результата в `libs.out`:
        copy(join(py_path, f'{active}.{_to}'),
             join(py_path, f'{out}.{_to}'))

        # Обратное преобразование для .out:
        convert_file(out, _to, _from)

    if not compare_dir(_from):
        print(f'Ошибка: папки `{_from}` не синхронизированы.')
        return
