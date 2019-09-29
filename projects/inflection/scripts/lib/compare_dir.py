from os import listdir

from libs.utils.io import compare
from projects.inflection.scripts.lib.paths import get_path


def compare_dir(unit, lang):
    path = get_path(unit, lang)
    if not compare(f'{path}/{unit}.{lang}', f'{path}/{unit}.out.{lang}'):
        return False
    for file in listdir(f'{path}/libs'):
        if file in ['__pycache__']:
            continue
        if not compare(f'{path}/libs/{file}', f'{path}/libs.out/{file}'):
            return False
    return True
