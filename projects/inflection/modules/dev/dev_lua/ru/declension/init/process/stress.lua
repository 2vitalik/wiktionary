local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- from shared_utils.io.json import json_load
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.process.stress'


-- @starts
function export.extract_stress_type(i)
	func = "extract_stress_type"
	_.starts(module, func)

	--    OLD: Старая версия кода:
--	local stress_regexp = "([abcdef][′']?[′']?)"
--	local stress_regexp2 = '(' .. stress_regexp .. '.*//.*' .. stress_regexp .. ')'
--	stress_regexp = '(' .. stress_regexp .. '(% ?.*))'
--	i.stress_type = _.extract(i.rest_index, stress_regexp2)
--	if not i.stress_type then
--		i.stress_type = _.extract(i.rest_index, stress_regexp)
--	end
	local stress_type, allowed_stress_types

--	INFO: Извлечение ударения из оставшейся части индекса:
	i.stress_type = _.extract(i.rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

--	INFO: Замена особых апострофов в ударении на обычные:
	if i.stress_type then
		i.stress_type = _.replaced(i.stress_type, '′', "'")
	end

--	INFO: Список допустимых схем ударений:
	allowed_stress_types = {  -- todo: special variables for that?
		'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
		'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
		'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
	}

--	INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
	if i.stress_type and not _.equals(i.stress_type, allowed_stress_types) then
		e.add_error(i, 'Ошибка: Неправильная схема ударения: ' .. i.stress_type)
	end

	_.ends(module, func)
end


-- @starts
function export.get_stress_schema(i)
	func = "get_stress_schema"
	_.starts(module, func)

	if _.contains(i.rest_index, '0') then
		_.log_info('Игнорируем схему ударения для случая "0"')
		i.stress_schema = {}  -- dict
		return _.ends(module, func)
	end

	unit = ''  -- todo: get from i.unit ?
	if i.adj then
		unit = 'adj'
	elseif i.pronoun then
		unit = 'pronoun'
	else
		unit = 'noun'
	end
	_.log_value(unit, 'unit')
	_.log_value(i.unit, 'i.unit')

	stress_schemas = mw.loadData('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/' .. unit)
	local stress_schema = stress_schemas[i.stress_type]

	-- ручное клонирование схемы ударения, т.к. потом через mw.clone не работает
	-- ошибка: "table from mw.loadData is read-only"
	i.stress_schema = {}  -- dict
	local types = {'stem', 'ending'}
	for j, type in pairs(types) do  -- list
		i.stress_schema[type] = {}  -- dict
		for case, value in pairs(stress_schema[type]) do
			i.stress_schema[type][case] = value
		end
	end

	_.log_table(i.stress_schema['stem'], "i.stress_schema['stem']")
	_.log_table(i.stress_schema['ending'], "i.stress_schema['ending']")

	_.ends(module, func)
end


return export
