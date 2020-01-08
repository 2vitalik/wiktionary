import re

print(re.sub('json_load\\(\'\\.\\./modules/dev/dev_py/ru/declension/data/(\\w+)/\' + unit + \'\\.json\'\\)',
             '',
             "stress_schemas = json_load('../modules/dev/dev_py/ru/declension/data/stress/' + unit + '.json')"))
