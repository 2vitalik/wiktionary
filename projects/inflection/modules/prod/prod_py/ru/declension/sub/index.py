from projects.inflection.modules.prod.prod_py import a
from projects.inflection.modules.prod.prod_py import mw
from projects.inflection.modules.prod.prod_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'declension.index'  # local


# Получение индекса Зализняка
@a.starts(module)
def get_zaliznyak(func, stem_type, stress_type, rest_index):  # export
    # local stem_types, index

    # TODO: process <...> cases properly

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
    index = stem_types[stem_type]
    if _.contains(rest_index, '°'):
        index = index + '°'
    elif _.contains(rest_index, '%*'):
        index = index + '*'
    # end
    index = index + _.replaced(stress_type, "'", "&#39;")
    if _.contains(rest_index, ['⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)']):
        index = index + '⊠'
    elif _.contains(rest_index, ['×', 'x', 'х', 'X', 'Х']):
        index = index + '×'
    # end
    if _.contains(rest_index, ['%(1%)', '①']):
        index = index + '①'
    # end
    if _.contains(rest_index, ['%(2%)', '②']):
        index = index + '②'
    # end
    if _.contains(rest_index, ['%(3%)', '③']):
        index = index + '③'
    # end
    if _.contains(rest_index, '÷'):
        index = index + '÷'
    # end
    if _.contains(rest_index, ['%-', '—', '−']):
        index = index + '−'
    # end
    if _.contains(rest_index, 'ё'):
        index = index + ', ё'
    # end

    _.ends(module, func)
    return index
# end


# return export
