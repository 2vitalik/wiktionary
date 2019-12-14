from projects.inflection.modules.dev.dev_py import mw
from projects.inflection.modules.dev.dev_py import utils as u


def trim_stress(str):
    # remove space after stress (we put it in the code just to make visually readable sources)
    return mw.ustring.gsub(str, '́ ', '́')


stash = {}
level = 0


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
    if key == 'all_sg':
        keys = ['gen_sg', 'dat_sg', 'prp_sg']  # without 'nom_sg', 'acc_sg' and 'ins_sg'
        for key in keys:
            dict[key] = replaced(dict[key], pattern, replace_to)

    elif key == 'all_pl':
        keys = ['nom_pl', 'gen_pl', 'dat_pl', 'ins_pl', 'prp_pl']  # without 'acc_pl'
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


def log_info(info):
    log('# ' + info)


def call(module, name):
    log('@ ' + module + '.' + name + '()')


def starts(module, name):
    log('↘ @ ' + module + '.' + name + '():')
    global level
    level += 4


def ends(module, name):
    global level
    level -= 4
    # log('↙ . ' + module + '.' + name + '()')
    log('↙ . ')


def log_value(value, name):
    log('= ' + name + ': "' + str(value) + '"')


def log_table(t, name):
    log('- ' + name + ':')
    for key, value in t.items():
        log('  ["' + str(key) + '"] = "' + str(value) + '"')


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
