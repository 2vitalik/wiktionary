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


def get_module_title(file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else ''
    title = f'Module:{dev_prefix}inflection/ru/'
    if file == 'declension/declension':
        title += 'declension'
    elif file.startswith('declension/'):
        title += file.replace('/sub',  '')
    else:
        title += file
    return title
