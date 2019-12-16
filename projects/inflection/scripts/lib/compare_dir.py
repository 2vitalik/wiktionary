from libs.utils.io import compare
from projects.inflection.scripts.lib.files import declension_files
from projects.inflection.scripts.lib.paths import get_path


def compare_dir(dev, lang):
    for file in declension_files:
        if not compare(get_path(dev, lang, file, out=False),
                       get_path(dev, lang, file, out=True)):
            return False
    return True
