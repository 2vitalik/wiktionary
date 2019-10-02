files = [
    'adj/endings',
    'adj/stress',
    'adj/template',
    'declension/declension',
    'declension/sub/endings',
    'declension/sub/form',
    'declension/sub/index',
    'declension/sub/parse_args',
    'declension/sub/reducable',
    'declension/sub/result',
    'declension/sub/stem_type',
    'declension/sub/stress',
    'noun/endings',
    'noun/form',
    'noun/parse_args',
    'noun/stress',
    'noun/template',
    'pronoun/endings',
    'pronoun/stress',
    # 'pronoun/template',  # todo
    # '/testcases',  # todo
]


def get_module_title(unit, file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else ''
    file = file.replace('[unit]', unit)
    file = file.replace('[.out]', '')
    title = f'Module:{dev_prefix}inflection/ru/{unit}'
    if file == unit:
        return title
    if file.startswith('libs/'):
        title += file[len('libs'):]
        return title
    raise Exception('Unknown module title')
