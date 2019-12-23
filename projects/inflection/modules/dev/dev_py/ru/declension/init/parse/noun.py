from projects.inflection.modules.dev.dev_py import a
from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


from ...output import result as r


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
def extract_gender_animacy(func, info):  # export
    # local convert_animacy, orig_index, rest_index

    # мо-жо - mf a
    # ж//жо - f ina//a
    # мо - m a
    # с  - n ina
    info.pt = False

    if _.startswith(info.index, 'п'):
        info.adj = True
    elif _.extract(info.index, '^м//ж') or _.extract(info.index, '^m//f'):  # todo: info: похоже все такие случаи либо 0, либо <...>
        info.gender = 'mf'
        info.animacy = 'in'
    elif _.extract(info.index, '^м//с') or _.extract(info.index, '^m//n'):
        info.gender = 'mn'
        info.animacy = 'in'
    elif _.extract(info.index, '^ж//м') or _.extract(info.index, '^f//m'):
        info.gender = 'fm'
        info.animacy = 'in'
    elif _.extract(info.index, '^ж//с') or _.extract(info.index, '^f//n'):
        info.gender = 'fn'
        info.animacy = 'in'
    elif _.extract(info.index, '^с//м') or _.extract(info.index, '^n//m'):
        info.gender = 'nm'
        info.animacy = 'in'
    elif _.extract(info.index, '^с//ж') or _.extract(info.index, '^n//m'):
        info.gender = 'nm'
        info.animacy = 'in'
    elif _.extract(info.index, '^мо%-жо') or _.extract(info.index, '^mf a'):
        info.gender = 'f'
        info.animacy = 'an'
        info.common_gender = True
    elif _.extract(info.index, '^мн'):
        info.gender = ''
        info.animacy = ''
        info.common_gender = False
        info.pt = True
        if _.extract(info.index, 'одуш'):
            info.animacy = 'an'
        elif _.extract(info.index, 'неод'):
            info.animacy = 'in'
        # end
        # TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
        info.rest_index = info.index
    elif _.extract(info.index, '^мс'):
        info.pronoun = True
    elif _.extract(info.index, '^м'):
        info.gender = 'm'
        info.animacy = get_cyrl_animacy(info.index, 'м')
        info.common_gender = False
    elif _.extract(info.index, '^ж'):
        info.gender = 'f'
        info.animacy = get_cyrl_animacy(info.index, 'ж')
        info.common_gender = False
    elif _.extract(info.index, '^с'):
        info.gender = 'n'
        info.animacy = get_cyrl_animacy(info.index, 'с')
        info.common_gender = False
    else:
        info.gender = _.extract(info.index, '^([mnf])')
        info.animacy = _.extract(info.index, '^[mnf] ([a-z/]+)')
        info.common_gender = False
        if info.animacy:
            convert_animacy = {}
            convert_animacy['in'] = 'in'
            convert_animacy['an'] = 'an'
            convert_animacy['ina'] = 'in'
            convert_animacy['a'] = 'an'
            convert_animacy['a//ina'] = 'an//in'
            convert_animacy['ina//a'] = 'in//an'
            convert_animacy['anin'] = 'an//in'
            convert_animacy['inan'] = 'in//an'
            info.animacy = convert_animacy[info.animacy]
        # end
    # end

    # Удаляем теперь соответствующий кусок индекса
    if (info.gender or info.gender == '') and info.animacy and not info.adj and not info.pronoun:
        _.log_value(info.index, 'info.index')
        orig_index = mw.text.trim(info.index)

#        # local test1 = _.replaced(info.index, '^mf a ?', '')
#        mw.log('test1 = ' + mw.text.trim(test1))
#
#        # local test2 = _.replaced(info.index, '^mf a ', '')
#        mw.log('test2 = ' + mw.text.trim(test2))
#
#        # local test3 = _.replaced(info.index, 'mf a ', '')
#        mw.log('test3 = ' + mw.text.trim(test3))
#
#        # local test4 = _.replaced(info.index, 'mf a', '')
#        mw.log('test4 = ' + mw.text.trim(test4))
#
#        # local test5 = mw.text.trim(_.replaced(info.index, '^mf a ?', ''))
#        mw.log('test5 = ' + test5)
#
#        # local test6 = _.replaced(info.index, '^mf a ?', '')
#        mw.log('test6 = ' + test6)
#        # local test7 = mw.text.trim(test6)
#        mw.log('test7 = ' + test7)

        # TODO: Simplify things a bit here (сделать циклом!):

        rest_index = _.replaced(info.index, '^mf a ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "mf a" из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(info.index, '^[mnf]+ [a-z/]+ ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "[mnf] [in/an]" из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(info.index, '^мн%.? неод%.? ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. неод." из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(info.index, '^мн%.? одуш%.? ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. одуш." из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(info.index, '^мн%.? ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн." из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        rest_index = _.replaced(info.index, '^[-мжсо/]+%,? ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "м/ж/с/мо/жо/со/..." из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
        r.add_error(info, 'TODO: process such errors')
        return _.ends(module, func)
    elif info.adj:
        _.log_value(info.index, 'info.index (п)')
        orig_index = mw.text.trim(info.index)

        rest_index = _.replaced(info.index, '^п ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "п" из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
    elif info.pronoun:
        _.log_value(info.index, 'info.index (мс)')
        orig_index = mw.text.trim(info.index)

        rest_index = _.replaced(info.index, '^мс ?', '')
        if rest_index != orig_index:
            info.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мс" из индекса')
            _.log_value(info.rest_index, 'info.rest_index')
            return _.ends(module, func)
        # end
    # end

    _.ends(module, func)
# end


# return export
