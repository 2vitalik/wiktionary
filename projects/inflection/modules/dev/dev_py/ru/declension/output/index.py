from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'output.index'  # local


# Получение индекса Зализняка
@a.starts(module)
def get_zaliznyak(func, i):  # export
    # TODO: process <...> cases properly

    # local stem_types
    stem_types = {
        'hard': '1',
        'soft': '2',
        'velar': '3',
        'sibilant': '4',
        'letter-ц': '5',
        'vowel': '6',
        'letter-и': '7',
        'm-3rd': '8',
        'f-3rd': '8',
        'f-3rd-sibilant': '8',
        'n-3rd': '8',
    }
    index = stem_types[i.stem.type]  # local
    if _.contains(i.rest_index, '°'):
        index = index + '°'
    elif _.contains(i.rest_index, '%*'):
        index = index + '*'
    # end
    index = index + _.replaced(i.stress_type, "'", "&#39;")
    if _.contains(i.rest_index, ['⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)']):
        index = index + '⊠'
    elif _.contains(i.rest_index, ['✕', '×', 'x', 'х', 'X', 'Х']):
        index = index + '✕'
    # end
    if _.contains(i.rest_index, ['%(1%)', '①']):
        index = index + '①'
    # end
    if _.contains(i.rest_index, ['%(2%)', '②']):
        index = index + '②'
    # end
    if _.contains(i.rest_index, ['%(3%)', '③']):
        index = index + '③'
    # end
    if _.contains(i.rest_index, '÷'):
        index = index + '÷'
    # end
    if _.contains(i.rest_index, ['%-', '—', '−']):
        index = index + '−'
    # end
    if _.contains(i.rest_index, 'ё'):
        index = index + ', ё'
    # end

    _.ends(module, func)
    return index
# end


# return export
