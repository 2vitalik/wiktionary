from shutil import copy

from libs.utils.io import ensure_parent_dir
from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.files import files
from projects.inflection.scripts.lib.paths import get_path


def clear_out_dir(dev, lang):
    for file in files:
        # Копирование результата в `ru.out`:
        out_file = get_path(dev, lang, file, out=True)
        ensure_parent_dir(out_file)
        copy(get_path(dev, lang, file, out=False), out_file)

    if not compare_dir(dev, lang):
        print(f'Ошибка: папки `{lang}` не синхронизированы.')
        return
