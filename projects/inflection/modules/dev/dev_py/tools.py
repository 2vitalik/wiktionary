import colorama
from colorama import Fore, Style

from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import utils as u


def trim_stress(str):
    # remove space after stress (we put it in the code just to make visually readable sources)
    return mw.ustring.gsub(str, '́ ', '́')


stash = {}
level = 0
colorama.init()


def clear_stash():
    global stash
    stash = {}


def add_stash(name, value):
    stash[name] = value


def apply_stash(str):
    for name, value in stash.items():
        str = mw.ustring.gsub(str, u.escape(name), value)

    return str


def replaced(str, pattern, replace_to):
    pattern = apply_stash(pattern)
    return mw.ustring.gsub(str, trim_stress(pattern), trim_stress(replace_to))


def replace(dict, key, pattern, replace_to):
    if key == 'all-sg':
        keys = ['gen-sg', 'dat-sg', 'prp-sg']  # without 'nom-sg', 'acc-sg' and 'ins-sg'
        for key in keys:
            dict[key] = replaced(dict[key], pattern, replace_to)

    elif key == 'all-pl':
        keys = ['nom-pl', 'gen-pl', 'dat-pl', 'ins-pl', 'prp-pl']  # without 'acc-pl'
        for key in keys:
            dict[key] = replaced(dict[key], pattern, replace_to)

    else:
        dict[key] = replaced(dict[key], pattern, replace_to)


def extract(str, pattern):
    pattern = apply_stash(pattern)
    return mw.ustring.match(str, trim_stress(pattern))


def check(string, values, checker):
    if type(values) == str:
        values = [values]

    for value in values:
        value = trim_stress(apply_stash(value))
        ok = checker == 'equals' and value == string \
             or checker == 'startswith' and mw.ustring.match(string, "^" + value) != None \
             or checker == 'endswith' and mw.ustring.match(string, value + "$") != None \
             or checker == 'penultimate' and mw.ustring.match(string, value + ".$") != None \
             or checker == 'contains' and mw.ustring.match(string, value) != None \
             or checker == 'contains_once' and len(mw.text.split(string, value)) == 2 \
             or checker == 'contains_several' and len(mw.text.split(string, value)) > 2
        if ok:
            return True

    return False


def equals(str, values):
    return check(str, values, 'equals')


def In(str, values):
    return equals(str, values)


def startswith(str, values):
    return check(str, values, 'startswith')


def endswith(str, values):
    return check(str, values, 'endswith')


def penultimate(str, values):
    return check(str, values, 'penultimate')


def contains(str, values):
    return check(str, values, 'contains')


def contains_once(str, values):
    return check(str, values, 'contains_once')


def contains_several(str, values):
    return check(str, values, 'contains_several')


def log(value):
    global level
    prefix = ' ' * level
    mw.log(prefix + value)


def green(value):
    return f'{Fore.GREEN}{value}{Style.RESET_ALL}'


def blue(value):
    return f'{Fore.BLUE}{value}{Style.RESET_ALL}'


def red(value):
    return f'{Fore.RED}{value}{Style.RESET_ALL}'


def green_line(func):
    def wrapped(*args, **kwargs):
        print(Fore.GREEN, end='')
        res = func(*args, **kwargs)
        print(Style.RESET_ALL, end='')
        return res
    return wrapped


def blue_line(func):
    def wrapped(*args, **kwargs):
        print(Fore.BLUE, end='')
        res = func(*args, **kwargs)
        print(Style.RESET_ALL, end='')
        return res
    return wrapped


def red_line(func):
    def wrapped(*args, **kwargs):
        print(Fore.RED, end='')
        res = func(*args, **kwargs)
        print(Style.RESET_ALL, end='')
        return res
    return wrapped


@green_line
def log_info(info):
    log('# ' + info)


# @blue_line
def call(module, name):
    log('@ ' + module + '.' + blue(name) + '()')
    global level


# @blue_line
def starts(module, name):
    log('↘ @ ' + module + '.' + blue(name) + '():')
    global level
    level += 4


def ends(module, name):
    global level
    level -= 4
    # log('↙ . ' + module + '.' + name + '()')
    log('↙ . ')


def returns(module, name, result):
    global level
    level -= 4
    # log('↙ . ' + module + '.' + name + '()')
    log('↙ . ')
    return result


# @red_line
def log_value(value, name):
    log('= ' + name + ': ' + red('"' + str(value) + '"'))


def log_table(t, name):
    log('- ' + name + ':')
    for key, value in t.items():
        log('  ["' + str(key) + '"] = ' + red('"' + str(value) + '"'))


def has_key(value, key=None):
    if key:
        return key in value
    return value


def has_value(value, key=None):
    if key:
        return key in value
    return value


def empty(value):
    return not value


# todo: log with colors (only for python)
# todo: log to files also (only for python)
# todo: create special short commands (like `u` and `pl`)
#  and use them from command line instead of running them via PyCharm
# todo: locally on python run all tests from lua tests data
# todo: try to get more tetsts from udarenieru html dumps... or from some zaliznyak file `All_Forms.txt`?
