from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension.init import _parse as parse
from .declension.run.result import error as e
from .declension import _run as run


module = 'declension'  # local


def prepare_stash():  # todo rename to `prepare_regexp_templates` or patterns
    _.clear_stash()
    _.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
    _.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
    _.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
# end


@a.starts(module)
def forms(func, base, args, frame):  # export  # todo: rename to `out_args`
    prepare_stash()  # INFO: Заполняем шаблоны для регулярок

    # `i` -- main `info` object
    i = parse.parse(base, args, frame)  # local
    if e.has_error(i):
        _.ends(module, func)
        return i.result
    # end

    # INFO: Запуск основного алгоритма и получение результирующих словоформ:
    run.run(i)

    _.ends(module, func)
    return i.result
# end


# return export
