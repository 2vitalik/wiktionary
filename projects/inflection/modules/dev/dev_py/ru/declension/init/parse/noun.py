from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...run.result import error as e


module = 'init.parse.noun'  # local


@a.call(module)
def get_cyrl_animacy(index, gender):
    if _.extract(index, '^' + gender + 'о//' + gender):
        return 'an//in'
    elif _.extract(index, '^' + gender + '//' + gender + 'о'):
        return 'in//an'
    elif _.extract(index, '^' + gender + 'о'):
        return 'an'
    else:
        return 'in'
    # end
# end


@a.starts(module)
def extract_gender_animacy(func, i):  # export
    # local convert_animacy, orig_index, rest_index

    # мо-жо - mf a
    # ж//жо - f ina//a
    # мо - m a
    # с  - n ina
    i.pt = False

    if _.startswith(i.index, 'п'):
        i.adj = True
    elif _.extract(i.index, '^м//ж') or _.extract(i.index, '^m//f'):  # todo: INFO: похоже все такие случаи либо 0, либо <...>
        i.gender = 'mf'
        i.animacy = 'in'
    elif _.extract(i.index, '^м//с') or _.extract(i.index, '^m//n'):
        i.gender = 'mn'
        i.animacy = 'in'
    elif _.extract(i.index, '^ж//м') or _.extract(i.index, '^f//m'):
        i.gender = 'fm'
        i.animacy = 'in'
    elif _.extract(i.index, '^ж//с') or _.extract(i.index, '^f//n'):
        i.gender = 'fn'
        i.animacy = 'in'
    elif _.extract(i.index, '^с//м') or _.extract(i.index, '^n//m'):
        i.gender = 'nm'
        i.animacy = 'in'
    elif _.extract(i.index, '^с//ж') or _.extract(i.index, '^n//m'):
        i.gender = 'nm'
        i.animacy = 'in'
    elif _.extract(i.index, '^мо%-жо') or _.extract(i.index, '^mf a'):
        i.gender = 'f'
        i.animacy = 'an'
        i.common_gender = True
    elif _.extract(i.index, '^мн'):
        i.gender = ''
        i.animacy = ''
        i.common_gender = False
        i.pt = True
        if _.extract(i.index, 'одуш'):
            i.animacy = 'an'
        elif _.extract(i.index, 'неод'):
            i.animacy = 'in'
        # end
        # TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
        i.rest_index = i.index
    elif _.extract(i.index, '^мс'):
        i.pronoun = True
    elif _.extract(i.index, '^м'):
        i.gender = 'm'
        i.animacy = get_cyrl_animacy(i.index, 'м')
        i.common_gender = False
    elif _.extract(i.index, '^ж'):
        i.gender = 'f'
        i.animacy = get_cyrl_animacy(i.index, 'ж')
        i.common_gender = False
    elif _.extract(i.index, '^с'):
        i.gender = 'n'
        i.animacy = get_cyrl_animacy(i.index, 'с')
        i.common_gender = False
    else:
        i.gender = _.extract(i.index, '^([mnf])')
        i.animacy = _.extract(i.index, '^[mnf] ([a-z/]+)')
        i.common_gender = False
        if i.animacy:
            convert_animacy = {}
            convert_animacy['in'] = 'in'
            convert_animacy['an'] = 'an'
            convert_animacy['ina'] = 'in'
            convert_animacy['a'] = 'an'
            convert_animacy['a//ina'] = 'an//in'
            convert_animacy['ina//a'] = 'in//an'
            convert_animacy['anin'] = 'an//in'
            convert_animacy['inan'] = 'in//an'
            i.animacy = convert_animacy[i.animacy]
        # end
    # end

    # Удаляем теперь соответствующий кусок индекса
    if (i.gender or i.gender == '') and i.animacy and not i.adj and not i.pronoun:
        _.log_value(i.index, 'i.index')
        orig_index = mw.text.trim(i.index)

#        # local test1 = _.replaced(i.index, '^mf a ?', '')
#        mw.log('test1 = ' + mw.text.trim(test1))
#
#        # local test2 = _.replaced(i.index, '^mf a ', '')
#        mw.log('test2 = ' + mw.text.trim(test2))
#
#        # local test3 = _.replaced(i.index, 'mf a ', '')
#        mw.log('test3 = ' + mw.text.trim(test3))
#
#        # local test4 = _.replaced(i.index, 'mf a', '')
#        mw.log('test4 = ' + mw.text.trim(test4))
#
#        # local test5 = mw.text.trim(_.replaced(i.index, '^mf a ?', ''))
#        mw.log('test5 = ' + test5)
#
#        # local test6 = _.replaced(i.index, '^mf a ?', '')
#        mw.log('test6 = ' + test6)
#        # local test7 = mw.text.trim(test6)
#        mw.log('test7 = ' + test7)

        # TODO: Simplify things a bit here (сделать циклом!):

        rest_index = _.replaced(i.index, '^mf a ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "mf a" из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(i.index, '^[mnf]+ [a-z/]+ ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "[mnf] [in/an]" из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(i.index, '^мн%.? неод%.? ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. неод." из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(i.index, '^мн%.? одуш%.? ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. одуш." из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(i.index, '^мн%.? ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн." из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(i.index, '^[-мжсо/]+%,? ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "м/ж/с/мо/жо/со/..." из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
        e.add_error(i, 'TODO: process such errors')
        return _.ends(module, func)
    elif i.adj:
        _.log_value(i.index, 'i.index (п)')
        orig_index = mw.text.trim(i.index)

        rest_index = _.replaced(i.index, '^п ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "п" из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
    elif i.pronoun:
        _.log_value(i.index, 'i.index (мс)')
        orig_index = mw.text.trim(i.index)

        rest_index = _.replaced(i.index, '^мс ?', '')
        if rest_index != orig_index:
            i.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мс" из индекса')
            _.log_value(i.rest_index, 'i.rest_index')
            return _.ends(module, func)
        # end
    # end

    _.ends(module, func)
# end


# return export
