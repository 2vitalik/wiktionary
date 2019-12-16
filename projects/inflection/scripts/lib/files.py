files = [
    'declension/data/endings/adj',
    'declension/data/endings/noun',
    'declension/data/endings/pronoun',
    'declension/data/stress/adj',
    'declension/data/stress/noun',
    'declension/data/stress/pronoun',
    'declension/data/template/adj',
    'declension/data/template/noun',
    'declension/init/input/common',
    'declension/init/input/noun',
    'declension/init/endings',
    'declension/init/stem_type',
    'declension/init/stress',
    'declension/modify/circles/adj',
    'declension/modify/circles/noun',
    'declension/modify/degree',
    'declension/modify/reducable',
    'declension/output/form',
    'declension/output/noun',
    'declension/output/index',
    'declension/output/result',
    'declension/declension',
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
