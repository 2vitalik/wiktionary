from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from .declension.init.parse import common as parse
from .declension.run.out import result as r
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

    info = parse.parse(base, args)  # local
    info.frame = frame  # todo: move to `parse`
    if r.has_error(info):
        _.ends(module, func)
        return info.out_args
    # end

    # INFO: Запуск основного алгоритма и получение результирующих словоформ:
    run.run(info)

    _.ends(module, func)
    return info.out_args
# end


# return export


# todo: rename `i.data` to `i.parts`
