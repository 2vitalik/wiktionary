files = [
    'data/endings/adj',
    'data/endings/noun',
    'data/endings/pronoun',
    'data/stress/adj',
    'data/stress/noun',
    'data/stress/pronoun',
    'data/template/adj',
    'data/template/noun',
    'init/input/common',
    'init/input/noun',
    'init/endings',
    'init/stem_type',
    'init/stress',
    'modify/circles/adj',
    'modify/circles/noun',
    'modify/degree',
    'modify/reducable',
    'output/form',
    'output/noun',
    'output/index',
    'output/result',
    'declension',
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
