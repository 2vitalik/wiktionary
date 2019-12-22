import re

from libs.utils.io import read, write
from projects.inflection.scripts.lib.paths import get_path


before = {
    'lua': """
local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')
""",
    'py': """
from projects.inflection.modules.{dev}.{dev}_py import a
from projects.inflection.modules.{dev}.{dev}_py import mw
from projects.inflection.modules.{dev}.{dev}_py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on `prod` version
"""}  # todo: use `from ....py import ` here (relative path)

string = '''('[^']*?'|"[^"]*?")'''

regexps_MULTILINE = {
    'py': [
        ('from projects.inflection.modules.{dev}.{dev}_py.a import syllables',
         'local syllables = require("Модуль:слоги")'),

        (r'from \.declension import (\w+) as (\w+)',
         "local \\2 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\1')"),

        (r'from \.((?:declension\.)?\.*)(\w+) import (\w+) as (\w+)',
         "local \\4 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\2/\\3')  -- '\\1'"),

        (r'from \.((?:declension\.)?\.*)(\w+) import (\w+)',
         "local \\3 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\2/\\3')  -- '\\1' ="),

        (r'from \.((?:declension\.)?\.*)(\w+)\.(\w+) import (\w+) as (\w+)',
         "local \\5 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\2/\\3/\\4')  -- '\\1'"),

        (r'from \.((?:declension\.)?\.*)(\w+)\.(\w+)\.(\w+) import (\w+) as (\w+)',
         "local \\6 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\2/\\3/\\4/\\5')  -- '\\1'"),

        (r"local ([^=]+) = require\('Module:' .. dev_prefix .. 'inflection/ru/([^']*)/_(\w+)'\)([^\n]*)\n",
         "local \\1 = require('Module:' .. dev_prefix .. 'inflection/ru/\\2/\\3')\\4  -- '_' /\\3\n"),

        # (r"\bmw\.text\.", 'mw.'),

        (r'stressed = 1',
         r'stressed = 2'),

        (r'unstressed = 0',
         r'unstressed = 1'),

        (r'^def (.*):  # export',
         'function export.\\1'),

        (r'^def (.*):',
         'local function \\1'),

        (r'# end\b',
         'end'),

        (r'# return export\n',
         'return export\n'),

        (r'^(\s+)([^=\n]+?) = (.*?)  # = export.\n',
         '\\1\\2 = export.\\3\n'),

        (r'^(\s+)([^=\n]*?)  # export.\n',
         '\\1export.\\2\n'),

        (r'^(\s*)([^=\n]+?) = (.*?)  # local\n',
         '\\1local \\2 = \\3\n'),

        (r'\bpass\b',
         '-- pass'),

        (r'# local ',
         'local '),

        (r'global ',
         '# global '),

        (fr'''\[({string},\s*{string}(,\s*{string})*)\]''',
         '{\\1}'),

        (r'\bif (.*?):',
         'if \\1 then'),

        (r'\belif (.*?):',
         'elseif \\1 then'),

        (r'\belse:',
         'else'),

        (r'\bstr\b',
         'tostring'),

        (r'\bTrue\b',
         'true'),

        (r'\bFalse\b',
         'false'),

        (r'\bNone\b',
         'nil'),

        (r'for (\w+) in range\((\w+)\):',
         'for \\1 = 1, \\2 do'),

        (r'for (\w+), (\w+) in enumerate\(([\w\.]+)\):',
         'for \\1, \\2 in pairs(\\3) do  -- list'),

        (r'for (\w+), (\w+) in (.+).items\(\):',
         'for \\1, \\2 in pairs(\\3) do'),

        (r'a\.table_len\(',
         'table.getn('),

        (r'(\s*)(.*)\.append\((.*)\)',
         '\\1table.insert(\\2, \\3)'),

        (r'_\.has_value\(([^)]+), ([^)]+)\)',
         '_.has_value(\\1[\\2])'),

        (r'_\.has_key\(([^)]+), ([^)]+)\)',
         '_.has_key(\\1[\\2])'),

        (r''' \+ (?!['"]$|\d)''',
         ' .. '),

        (r' != ',
         ' ~= '),

        (r"(\s)'(.*)': ",
         "\\1['\\2'] = "),

        (r'\[(1)\]',
         '[2]'),

        (r'\[(0)\]',
         '[1]'),

        (r"(?<![&'])#(.*)$",
         '--\\1'),

        (r"(?<![&'])#(.*)$",
         '--\\1'),  # Второй раз, чтобы обработать случаи `# .. # ..`

        (r'^( +)-- INFO:',
         '--\\1INFO:'),

        (r'^(--)?' + '    ' * 9, '\\1' + '\t' * 9),
        (r'^(--)?' + '    ' * 8, '\\1' + '\t' * 8),
        (r'^(--)?' + '    ' * 7, '\\1' + '\t' * 7),
        (r'^(--)?' + '    ' * 6, '\\1' + '\t' * 6),
        (r'^(--)?' + '    ' * 5, '\\1' + '\t' * 5),
        (r'^(--)?' + '    ' * 4, '\\1' + '\t' * 4),
        (r'^(--)?' + '    ' * 3, '\\1' + '\t' * 3),
        (r'^(--)?' + '    ' * 2, '\\1' + '\t' * 2),
        (r'^(--)?' + '    ' * 1, '\\1' + '\t' * 1),
    ],
    'lua': [
        ('local syllables = require\("Модуль:слоги"\)',
         'from projects.inflection.modules.{dev}.{dev}_py.a import syllables'),

        (r"local ([^=]+) = require\('Module:' .. dev_prefix .. 'inflection/ru/([^'\n]*)/(\w+)'\)([^\n]*)  -- '_' /(\w+)\n",
         "local \\1 = require('Module:' .. dev_prefix .. 'inflection/ru/\\2/_\\3')\\4\n"),

        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)'\)",
         'from .declension import \\2 as \\1'),

        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)/(\w+)'\)  -- '((?:declension\.)?\.*)' =",
         'from .\\4\\2 import \\1'),

        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)/(\w+)'\)  -- '((?:declension\.)?\.*)'",
         'from .\\4\\2 import \\3 as \\1'),

        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)/(\w+)/(\w+)'\)  -- '((?:declension\.)?\.*)'",
         'from .\\5\\2.\\3 import \\4 as \\1'),

        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)/(\w+)/(\w+)/(\w+)'\)  -- '((?:declension\.)?\.*)'",
         'from .\\6\\2.\\3.\\4 import \\5 as \\1'),

        # (r"\bmw\.text\.", 'mw.'),
        # (r"\bmw\.ustring\.", 'mw.'),

        (r'stressed = 2',
         'stressed = 1'),

        (r'unstressed = 1',
         'unstressed = 0'),

        (r'^local function (.*?)(\s*--.*)?$',
         'def \\1:\\2'),

        (r'^function export\.(.*?)(\s*--.*)?$',
         'def \\1:  # export\\2'),

        (r'\bend\b',
         '# end'),

        (r'return export\n',
         '# return export\n'),

        (r'^(\s+)([^=\n]+?) = export\.(.*?)\n',
         '\\1\\2 = \\3  # = export.\n'),

        (r'^(\s+)export\.(.*?)\n',
         '\\1\\2  # export.\n'),

        (r'^(\s*)local ([^=\n]+?) = (.*?)\n',
         '\\1\\2 = \\3  # local\n'),

        (r'-- pass\b',
         'pass'),

        (r'local ',
         '# local '),

        (r'# global ',
         'global '),

        (r"\{('.*?', '.*?')\}",
         '[\\1]'),

        (r'\{(".*?", ".*?")\}',
         '[\\1]'),

        (r'\{(\'.*?\', ".*?")\}',
         '[\\1]'),

        (r'\bif (.*) then',
         'if \\1:'),

        (r'\belseif (.*) then',
         'elif \\1:'),

        (r'\belse\b',
         'else:'),

        (r'\btostring\b',
         'str'),

        (r'\btrue\b',
         'True'),

        (r'\bfalse\b',
         'False'),

        (r'\bnil\b',
         'None'),

        (r'for (\w+) = 1, (\w+) do',
         'for \\1 in range(\\2):'),

        (r'for (\w+), (\w+) in pairs\((.*)\) do  -- list',
         'for \\1, \\2 in enumerate(\\3):'),

        (r'for (\w+), (\w+) in pairs\((.*)\) do',
         'for \\1, \\2 in \\3.items():'),

        (r'table\.getn\(',
         'a.table_len('),

        (r'table\.insert\((.*), (.*)\)',
         '\\1.append(\\2)'),

        (r'_\.has_value\(([\w\.]+)\[([^]]+)\]\)',
         '_.has_value(\\1, \\2)'),

        (r'_\.has_key\(([\w\.]+)\[([^]]+)\]\)',
         '_.has_key(\\1, \\2)'),

        (r' \.\. ',
         ' + '),

        (r' ~= ',
         ' != '),

        (r'\[(1)\]',
         '[0]'),

        (r'\[(2)\]',
         '[1]'),

        (r"(\s)\['(.*)'\] = ",
         "\\1'\\2': "),

        (r'^--(\t+)INFO:',
         '\\1-- INFO:'),

        (r'^--(.*)$',
         '#\\1'),

        (r'(\s)--(.*)$',
         '\\1#\\2'),

        ('\t', r'    '),
    ],
}
regexps_DOTALL = {
    'py': [
        (r'\[([^][]*)\]([,)]?)  (--|#) list',
         '{\\1}\\2  -- list'),

        (r'dict\(([^()]*)\)\)  (--|#) b-dict',
         '{\\1})  -- b-dict'),

        (r'dict\(([^()]*)\)([,)]?)  (--|#) dict',
         '{\\1}\\2  -- dict'),

        (r'a\.AttrDict\(([^()]*)\)([,)]?)  (--|#) AttrDict',
         '{\\1}\\2  -- AttrDict'),

        (r'@a\.starts\(module\)\ndef ([\w]+)\(func(, )?([^\n]*?)\n',
         '# @starts\ndef \\1(\\3\n    func = "\\1"\n    _.starts(module, func)\n\n'),

        (r'@a\.call\(module\)\ndef ([\w]+)\(([^\n]*?)\n',
         '# @call\ndef \\1(\\2\n    func = "\\1"\n    _.call(module, func)\n\n'),
    ],
    'lua': [
        (r'\{([^{}]*)\}([,)]?)  (--|#) list',
         '[\\1]\\2  # list'),

        (r'\{([^{}]*)\}\)  (--|#) b-dict',
         'dict(\\1))  # b-dict'),

        (r'\{([^{}]*)\}([,)]?)  (--|#) dict',
         'dict(\\1)\\2  # dict'),

        (r'\{([^{}]*)\}([,)]?)  (--|#) AttrDict',
         'a.AttrDict(\\1)\\2  # AttrDict'),

        (r'(--|#) @starts\n(local )?function ([\w.]+)\(\)([^\n]*?)\n\tfunc = "[^"]+"\n\t_\.starts\(module, func\)\n\n',
         '@a.starts(module)\n\\2function \\3(func)\\4\n'),

        (r'(--|#) @starts\n(local )?function ([\w.]+)\(([^\n]*?)\n\tfunc = "[^"]+"\n\t_\.starts\(module, func\)\n\n',
         '@a.starts(module)\n\\2function \\3(func, \\4\n'),

        (r'(--|#) @call\n(local )?function ([\w.]+)\(([^\n]*?)\n\tfunc = "[^"]+"\n\t_\.call\(module, func\)\n\n',
         '@a.call(module)\n\\2function \\3(\\4\n'),
    ],
}
regexps_before = {
    'py': [

    ],
    'lua': [
        (r'\{  (--|#) dict', 'dict(  # dict'),
    ],
}
regexps_after = {
    'py': [
        (r'dict\(  (--|#) dict', '{  -- dict'),
        (r'\)([,)]?)  (--|#) dict', '}\\1  -- dict'),
    ],
    'lua': [
        (r'\}([,)]?)  (--|#) dict', ')\\1  # dict'),
    ],
}


def convert_file(dev, file, _from, _to, out):
    dev_str = 'dev' if dev else 'prod'

    py_file = get_path(dev, 'py', file, out=out)
    lua_file = get_path(dev, 'lua', file, out=out)
    in_file = py_file if _from == 'py' else lua_file
    out_file = py_file if _to == 'py' else lua_file

    content = read(in_file)
    content = \
        content.replace(before[_from].replace('{dev}', dev_str).strip(), '')

    for pattern, replace in regexps_before[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_DOTALL[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_MULTILINE[_from]:
        pattern = pattern.replace('{dev}', dev_str)
        replace = replace.replace('{dev}', dev_str)
        content = re.sub(pattern, replace, content, flags=re.MULTILINE)

    for i in range(5):
        for pattern, replace in regexps_DOTALL[_from]:
            content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_after[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    content = \
        f"{before[_to].replace('{dev}', dev_str)}\n\n" \
        f"{content.strip()}\n".lstrip()
    write(out_file, content)


# todo: автоматически отслеживать `local` случаи
# todo: автоматически определять тип константы `{...}` в LUA
# todo: автоматически определять тип цикла `for` в LUA
# todo: автоматически определять позиции для `end` в Python
