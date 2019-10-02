import re
from os.path import join

from libs.utils.io import read, write
from projects.inflection.scripts.lib.paths import get_path


before = {
    'lua': """
local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')
""",
    'py': """
from projects.inflection.modules.py import additional
from projects.inflection.modules.py import mw
from projects.inflection.modules.py import tools as _

dev_prefix = 'User:Vitalik/'  # comment this on active version
"""}

string = '''('[^']*'|"[^"]*")'''

regexps_MULTILINE = {
    'py': [
        ('from projects.inflection.modules.py.additional import syllables', 'local syllables = require("Модуль:слоги")'),
        (r'from .libs import (\w+)', "local \\1 = require(parent_prefix .. '/\\1')"),
        (r'from \.\.declension.sub import (\w+)', "local \\1 = require('Module:' .. dev_prefix .. 'inflection/ru/declension/\\1')"),
        (r'from \.\.(\.)?(\w+) import (\w+) as (\w+)', "local \\4 = require('Module:' .. dev_prefix .. 'inflection/ru/\\2/\\3')  -- '\\1'"),
        # (r"\bmw\.text\.", 'mw.'),

        (r'^unstressed = 0', 'unstressed = 1'),
        (r'^stressed = 1', 'stressed = 2'),

        (r'^def (.*):  # export', 'function export.\\1'),
        (r'^def (.*):', 'local function \\1'),
        (r'# end\b', 'end'),
        (r'# return export\n', 'return export\n'),

        (r'\bpass\b', '-- pass'),
        (r'# local ', 'local '),
        (fr'''\[({string},\s*{string}(,\s*{string})*)\]''', '{\\1}'),

        (r'\bif (.*?):', 'if \\1 then'),
        (r'\belif (.*?):', 'elseif \\1 then'),
        (r'\belse:', 'else'),

        (r'\bstr\b', 'tostring'),
        (r'\bTrue\b', 'true'),
        (r'\bFalse\b', 'false'),
        (r'\bNone\b', 'nil'),

        (r'for (\w+) in range\((\w+), (\w+) \+ 1\):', 'for \\1 = \\2, \\3 do'),
        (r'for (\w+), (\w+) in enumerate\((\w+)\):', 'for \\1, \\2 in pairs(\\3) do  -- list'),
        (r'for (\w+), (\w+) in (.+).items\(\):', 'for \\1, \\2 in pairs(\\3) do'),

        (r'additional\.table_len\(', 'table.getn('),
        (r'(\s*)(.*)\.append\((.*)\)', '\\1table.insert(\\2, \\3)'),

        (r'_\.has_value\(([^)]+), ([^)]+)\)', '_.has_value(\\1[\\2])'),
        (r'_\.has_key\(([^)]+), ([^)]+)\)', '_.has_key(\\1[\\2])'),

        (r''' \+ (?!['"]$|\d)''', ' .. '),
        (r' != ', ' ~= '),

        (r"(\s)'(.*)': ", "\\1['\\2'] = "),

        (r"(?<![&'])#(.*)$", '--\\1'),
        (r"(?<![&'])#(.*)$", '--\\1'),  # Второй раз, чтобы обработать случаи `# .. # ..`

        (r'^( +)-- INFO:', '--\\1INFO:'),

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
        ('local syllables = require\("Модуль:слоги"\)', 'from projects.inflection.modules.py.additional import syllables'),
        (r"^local (\w+) = require\(parent_prefix \.\. '/(\w+)'\)", 'from .libs import \\1'),
        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/declension/(\w+)'\)", 'from ..declension.sub import \\1'),
        (r"local (\w+) = require\('Module:' \.\. dev_prefix \.\. 'inflection/ru/(\w+)/(\w+)'\)  -- '(\.)?'", 'from ..\\4\\2 import \\3 as \\1'),
        # (r"\bmw\.text\.", 'mw.'),
        # (r"\bmw\.ustring\.", 'mw.'),

        (r'^unstressed = 1', 'unstressed = 0'),
        (r'^stressed = 2', 'stressed = 1'),

        (r'^local function (.*?)(\s*--.*)?$', 'def \\1:\\2'),
        (r'^function export\.(.*?)(\s*--.*)?$', 'def \\1:  # export\\2'),
        (r'\bend\b', '# end'),
        (r'return export\n', '# return export\n'),

        (r'-- pass\b', 'pass'),
        (r'local ', '# local '),
        (r"\{('.*', '.*')\}", '[\\1]'),
        (r'\{(".*", ".*")\}', '[\\1]'),
        (r'\{(\'.*\', ".*")\}', '[\\1]'),

        (r'\bif (.*) then', 'if \\1:'),
        (r'\belseif (.*) then', 'elif \\1:'),
        (r'\belse\b', 'else:'),

        (r'\btostring\b', 'str'),
        (r'\btrue\b', 'True'),
        (r'\bfalse\b', 'False'),
        (r'\bnil\b', 'None'),

        (r'for (\w+) = (\w+), (\w+) do', 'for \\1 in range(\\2, \\3 + 1):'),
        (r'for (\w+), (\w+) in pairs\((.*)\) do  -- list', 'for \\1, \\2 in enumerate(\\3):'),
        (r'for (\w+), (\w+) in pairs\((.*)\) do', 'for \\1, \\2 in \\3.items():'),

        (r'table\.getn\(', 'additional.table_len('),
        (r'table\.insert\((.*), (.*)\)', '\\1.append(\\2)'),

        (r'_\.has_value\((\w+)\[([^]]+)\]\)', '_.has_value(\\1, \\2)'),
        (r'_\.has_key\((\w+)\[([^]]+)\]\)', '_.has_key(\\1, \\2)'),

        (r' \.\. ', ' + '),
        (r' ~= ', ' != '),

        (r"(\s)\['(.*)'\] = ", "\\1'\\2': "),

        (r'^--(\t+)INFO:', '\\1-- INFO:'),

        (r'^--(.*)$', '#\\1'),
        (r'(\s)--(.*)$', '\\1#\\2'),

        ('\t', r'    '),
    ],
}
regexps_DOTALL = {
    'py': [
        (r'\[([^][]*)\]([,)]?)  (--|#) list',     '{\\1}\\2  -- list'),
        (r'dict\(([^()]*)\)\)  (--|#) b-dict', '{\\1})  -- b-dict'),
        (r'dict\(([^()]*)\)([,)]?)  (--|#) dict', '{\\1}\\2  -- dict'),
        (r'additional\.AttrDict\(([^()]*)\)([,)]?)  (--|#) AttrDict', '{\\1}\\2  -- AttrDict'),
    ],
    'lua': [
        (r'\{([^{}]*)\}([,)]?)  (--|#) list', '[\\1]\\2  # list'),
        (r'\{([^{}]*)\}\)  (--|#) b-dict', 'dict(\\1))  # b-dict'),
        (r'\{([^{}]*)\}([,)]?)  (--|#) dict', 'dict(\\1)\\2  # dict'),
        (r'\{([^{}]*)\}([,)]?)  (--|#) AttrDict', 'additional.AttrDict(\\1)\\2  # AttrDict'),
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


def convert_file(file, _from, _to, out):
    py_file = get_path('py', file, out=out)
    lua_file = get_path('lua', file, out=out)
    in_file = py_file if _from == 'py' else lua_file
    out_file = py_file if _to == 'py' else lua_file

    content = read(in_file)
    content = content.replace(before[_from].strip(), '')

    for pattern, replace in regexps_before[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_DOTALL[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_MULTILINE[_from]:
        content = re.sub(pattern, replace, content, flags=re.MULTILINE)

    for i in range(5):
        for pattern, replace in regexps_DOTALL[_from]:
            content = re.sub(pattern, replace, content, flags=re.DOTALL)

    for pattern, replace in regexps_after[_from]:
        content = re.sub(pattern, replace, content, flags=re.DOTALL)

    content = f"{before[_to]}\n\n{content.strip()}\n".lstrip()
    write(out_file, content)


# todo: автоматически отслеживать `local` случаи
# todo: автоматически определять тип константы `{...}` в LUA
# todo: автоматически определять тип цикла `for` в LUA
# todo: автоматически определять позиции для `end` в Python
