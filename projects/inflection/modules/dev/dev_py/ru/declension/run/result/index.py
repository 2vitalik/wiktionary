from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


module = 'run.result.index'  # local


# Получение индекса Зализняка
@a.starts(module)
def get_zaliznyak(func, i):  # export
    # TODO: process <...> cases properly
    #  also e.g. "2*a + <п 1a>"
    r = i.result  # local

    if not i.has_index:
        r['зализняк1'] = '??'
        return _.ends(module, func)
    # end

    # local stem_types
    stem_types = {
        '1-hard': '1',
        '2-soft': '2',
        '3-velar': '3',
        '4-sibilant': '4',
        '5-letter-ц': '5',
        '6-vowel': '6',
        '7-letter-и': '7',
        '8-third': '8',
    }
    index = '?'  # local
    if _.contains(i.rest_index, '0'):
        index = '0'
    else:
        # index = i.stem.type[0]  -- TODO
        index = stem_types[i.stem.type]
    # end
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

    r['зализняк1'] = index
    value = r['зализняк1']  # local  # for category
    value = _.replaced(value, '①', '(1)')
    value = _.replaced(value, '②', '(2)')
    value = _.replaced(value, '③', '(3)')
    r['зализняк'] = value

    _.ends(module, func)
# end


# return export
