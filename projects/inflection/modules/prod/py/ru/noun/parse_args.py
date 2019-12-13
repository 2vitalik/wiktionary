from projects.inflection.modules.prod.py import additional
from projects.inflection.modules.prod.py import mw
from projects.inflection.modules.prod.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version


def get_cyrl_animacy(index, gender):
    _.log_func('parse_args', 'get_cyrl_animacy')

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


def extract_gender_animacy(data):  # export
    _.log_func('parse_args', 'extract_gender_animacy')

    # local convert_animacy, orig_index, rest_index

    # мо-жо - mf a
    # ж//жо - f ina//a
    # мо - m a
    # с  - n ina
    data.pt = False

    if _.startswith(data.index, 'п'):
        data.adj = True
    elif _.extract(data.index, '^м//ж') or _.extract(data.index, '^m//f'):
        data.gender = 'mf'
        data.animacy = 'in'
    elif _.extract(data.index, '^м//с') or _.extract(data.index, '^m//n'):
        data.gender = 'mn'
        data.animacy = 'in'
    elif _.extract(data.index, '^ж//м') or _.extract(data.index, '^f//m'):
        data.gender = 'fm'
        data.animacy = 'in'
    elif _.extract(data.index, '^ж//с') or _.extract(data.index, '^f//n'):
        data.gender = 'fn'
        data.animacy = 'in'
    elif _.extract(data.index, '^с//м') or _.extract(data.index, '^n//m'):
        data.gender = 'nm'
        data.animacy = 'in'
    elif _.extract(data.index, '^с//ж') or _.extract(data.index, '^n//m'):
        data.gender = 'nm'
        data.animacy = 'in'
    elif _.extract(data.index, '^мо%-жо') or _.extract(data.index, '^mf a'):
        data.gender = 'f'
        data.animacy = 'an'
        data.common_gender = True
    elif _.extract(data.index, '^мн'):
        data.gender = ''
        data.animacy = ''
        data.common_gender = False
        data.pt = True
        if _.extract(data.index, 'одуш'):
            data.animacy = 'an'
        elif _.extract(data.index, 'неод'):
            data.animacy = 'in'
        # end
        # TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
        data.rest_index = data.index
    elif _.extract(data.index, '^мс'):
        data.pronoun = True
    elif _.extract(data.index, '^м'):
        data.gender = 'm'
        data.animacy = get_cyrl_animacy(data.index, 'м')
        data.common_gender = False
    elif _.extract(data.index, '^ж'):
        data.gender = 'f'
        data.animacy = get_cyrl_animacy(data.index, 'ж')
        data.common_gender = False
    elif _.extract(data.index, '^с'):
        data.gender = 'n'
        data.animacy = get_cyrl_animacy(data.index, 'с')
        data.common_gender = False
    else:
        data.gender = _.extract(data.index, '^([mnf])')
        data.animacy = _.extract(data.index, '^[mnf] ([a-z/]+)')
        data.common_gender = False
        if data.animacy:
            convert_animacy = {}
            convert_animacy['in'] = 'in'
            convert_animacy['an'] = 'an'
            convert_animacy['ina'] = 'in'
            convert_animacy['a'] = 'an'
            convert_animacy['a//ina'] = 'an//in'
            convert_animacy['ina//a'] = 'in//an'
            convert_animacy['anin'] = 'an//in'
            convert_animacy['inan'] = 'in//an'
            data.animacy = convert_animacy[data.animacy]
        # end
    # end

    # Удаляем теперь соответствующий кусок индекса
    if (data.gender or data.gender == '') and data.animacy and not data.adj and not data.pronoun:
        _.log_value(data.index, 'data.index')
        orig_index = mw.text.trim(data.index)

#        # local test1 = _.replaced(data.index, '^mf a ?', '')
#        mw.log('test1 = ' + mw.text.trim(test1))
#
#        # local test2 = _.replaced(data.index, '^mf a ', '')
#        mw.log('test2 = ' + mw.text.trim(test2))
#
#        # local test3 = _.replaced(data.index, 'mf a ', '')
#        mw.log('test3 = ' + mw.text.trim(test3))
#
#        # local test4 = _.replaced(data.index, 'mf a', '')
#        mw.log('test4 = ' + mw.text.trim(test4))
#
#        # local test5 = mw.text.trim(_.replaced(data.index, '^mf a ?', ''))
#        mw.log('test5 = ' + test5)
#
#        # local test6 = _.replaced(data.index, '^mf a ?', '')
#        mw.log('test6 = ' + test6)
#        # local test7 = mw.text.trim(test6)
#        mw.log('test7 = ' + test7)

        # TODO: Simplify things a bit here (сделать циклом!):

        rest_index = _.replaced(data.index, '^mf a ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "mf a" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^[mnf]+ [a-z/]+ ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "[mnf] [in/an]" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^мн%.? неод%.? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. неод." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^мн%.? одуш%.? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн. одуш." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^мн%.? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мн." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        rest_index = _.replaced(data.index, '^[-мжсо/]+%,? ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "м/ж/с/мо/жо/со/..." из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
        return dict(error = 'TODO')  # dict # TODO: process such errors
    elif data.adj:
        _.log_value(data.index, 'data.index (п)')
        orig_index = mw.text.trim(data.index)

        rest_index = _.replaced(data.index, '^п ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "п" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
    elif data.pronoun:
        _.log_value(data.index, 'data.index (мс)')
        orig_index = mw.text.trim(data.index)

        rest_index = _.replaced(data.index, '^мс ?', '')
        if rest_index != orig_index:
            data.rest_index = mw.text.trim(rest_index)
            mw.log('  # Удаление "мс" из индекса')
            _.log_value(data.rest_index, 'data.rest_index')
            return
        # end
    # end
# end


# return export
