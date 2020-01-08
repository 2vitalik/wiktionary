from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.result import error as e


module = 'init.parse.init_stem'  # local


@a.starts(module)
def init_stem(func, i):  # export  # todo rename to `init_stem`

    # INFO: Исходное слово без ударения:
    i.word.unstressed = _.replaced(i.word.stressed, '́ ', '')  # todo: move outside this function

    # INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
    i.word.cleared = _.replaced(_.replaced(_.replaced(i.word.unstressed, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

    if i.adj:
        if _.endswith(i.word.stressed, 'ся'):
            i.postfix = True
            i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]ся$', '')
            i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]ся$', '')
        else:
            i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]$', '')
            i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]$', '')
        # end
    else:
        # INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
        i.stem.unstressed = _.replaced(i.word.unstressed, '[аеёийоьыя]$', '')
        i.stem.stressed = _.replaced(i.word.stressed, '[аеёийоьыя]́ ?$', '')
    # end

    _.log_value(i.word.unstressed, 'i.word.unstressed')
    _.log_value(i.stem.unstressed, 'i.stem.unstressed')
    _.log_value(i.stem.stressed, 'i.stem.stressed')

    #  INFO: Случай, когда не указано ударение у слова:
    several_vowels = _.contains_several(i.word.stressed, '{vowel+ё}')  # local
    has_stress = _.contains(i.word.stressed, '[́ ё]')  # local
    if several_vowels and not has_stress:
        _.log_info('Ошибка: Не указано ударение в слове')
        e.add_error(i, 'Ошибка: Не указано ударение в слове')
        i.result.error_category = 'Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)'
    # end

    _.ends(module, func)
# end


# return export
