from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .init import _parse as parse


module = 'init'  # local


def prepare_regexp_patterns():
    _.clear_stash()
    _.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
    _.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
    _.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
# end


@a.starts(module)
def init_info(func, base, args, frame):  # export
    prepare_regexp_patterns()  # INFO: Заполняем шаблоны для регулярок

    i = parse.parse(base, args, frame)

    return _.returns(module, func, i)
# end


# return export
