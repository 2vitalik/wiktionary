declension_files = [
    'ru/_declension',
    'ru/declension/data/endings/adj',
    'ru/declension/data/endings/noun',
    'ru/declension/data/endings/pronoun',
    'ru/declension/data/stress/adj',
    'ru/declension/data/stress/noun',
    'ru/declension/data/stress/pronoun',
    'ru/declension/data/template/adj',
    'ru/declension/data/template/noun',
    'ru/declension/init/parse/common',
    'ru/declension/init/parse/noun',
    'ru/declension/init/_process',
    'ru/declension/init/process/stem_type',
    'ru/declension/init/process/stress',
    'ru/declension/run/_parts',
    'ru/declension/run/parts/_prepare',
    'ru/declension/run/parts/prepare/endings',
    'ru/declension/run/parts/prepare/stress_apply',
    'ru/declension/run/parts/_transform',
    'ru/declension/run/parts/transform/circles/adj',
    'ru/declension/run/parts/transform/circles/noun',
    'ru/declension/run/parts/transform/degree',
    'ru/declension/run/parts/transform/reducable',
    'ru/declension/run/out/forms/common',
    'ru/declension/run/out/forms/noun',
    'ru/declension/run/out/forms/adj',
    'ru/declension/run/out/index',
    'ru/declension/run/out/init_out_args',
    'ru/declension/run/out/result',
]

testcases_files = [
    'ru/declension/_testcases',
    'ru/declension/testcases/_adj',
    'ru/declension/testcases/adj/data',
    'ru/declension/testcases/adj/other',
    'ru/declension/testcases/adj/simple',
    'ru/declension/testcases/_noun',
    'ru/declension/testcases/noun/all/angled',
    'ru/declension/testcases/noun/all/debug',
    'ru/declension/testcases/noun/all/other_cases',
    'ru/declension/testcases/noun/all/other_indexes',
    'ru/declension/testcases/noun/all/other_indexes2',
    'ru/declension/testcases/noun/all/reducable',
    'ru/declension/testcases/noun/all/simple',
    'ru/declension/testcases/noun/all/variations',
    'ru/declension/testcases/noun/data',
    'ru/declension/testcases/noun/new',
    'ru/declension/testcases/noun/other',
    'ru/declension/testcases/noun/reduceables',
    'ru/declension/testcases/noun/simple',
]

tpl_files = [
    'inflection/ru/adj',
    'inflection/ru/noun',
    'inflection/ru/noun/text',
    'inflection/ru/noun/cat',
]


def convert_path(file):
    path = file.replace('/_', '/')
    if path.startswith('_'):
        path = path[1:]
    return path


def get_module_title(file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else ''
    return f'Module:{dev_prefix}inflection/{convert_path(file)}'


def get_docs_title(file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else ''
    return f'Module:{dev_prefix}inflection/{convert_path(file)}/Документация'


def get_tpl_title(file, dev=True):
    dev_prefix = 'User:Vitalik/' if dev else 'Шаблон:'
    return f'{dev_prefix}{convert_path(file)}'
