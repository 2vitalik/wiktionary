from shutil import copy

from projects.inflection.scripts.lib.compare_dir import compare_dir
from projects.inflection.scripts.lib.modules import files
from projects.inflection.scripts.lib.paths import get_path


def clear_out_dir(lang):
    for file in files:
        # Копирование результата в `ru.out`:
        copy(get_path(lang, file, out=False),
             get_path(lang, file, out=True))

    if not compare_dir(lang):
        print(f'Ошибка: папки `{lang}` не синхронизированы.')
        return
