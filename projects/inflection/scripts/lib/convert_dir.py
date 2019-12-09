from shutil import copy

from libs.utils.io import write
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.convert_file import convert_file
from projects.inflection.scripts.lib.files import files
from projects.inflection.scripts.lib.paths import get_path


def convert_dir(dev, _from, _to):
    if not compare_dir(dev, _to):
        print(f'Ошибка: папки `{_to}` не синхронизированы.')
        return

    for file in files:
        # Прямое преобразование:
        convert_file(dev, file, _from, _to, out=False)

        # Копирование результата в `ru.out`:
        in_file = get_path(dev, _to, file, out=False)
        out_file = get_path(dev, _to, file, out=True)
        write(out_file, '')  # чтобы создать папки, если их нет
        copy(in_file, out_file)

        # Обратное преобразование для .out:
        convert_file(dev, file, _to, _from, out=True)

    if not compare_dir(dev, _from):
        print(f'Ошибка: папки `{_from}` не синхронизированы.')
        return
