local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local adj_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/adj')  -- '..'
local pronoun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/pronoun')  -- '..'
local noun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/noun')  -- '..'
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/result')  -- '..'


local module = 'init.process.stress'


-- @starts
function export.extract_stress_type(i)
	func = "extract_stress_type"
	_.starts(module, func)

	--    OLD: Старая версия кода:
--	local stress_regexp = "([abcdef][′']?[′']?)"
--	local stress_regexp2 = '(' .. stress_regexp .. '.*//.*' .. stress_regexp .. ')'
--	stress_regexp = '(' .. stress_regexp .. '(% ?.*))'
--	info.stress_type = _.extract(rest_index, stress_regexp2)
--	if not info.stress_type then
--		info.stress_type = _.extract(rest_index, stress_regexp)
--	end
	local stress_type, allowed_stress_types

--	INFO: Извлечение ударения из оставшейся части индекса:
	i.stress_type = _.extract(i.rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

--	INFO: Замена особых апострофов в ударении на обычные:
	if i.stress_type then
		i.stress_type = _.replaced(i.stress_type, '′', "'")
	end

--	INFO: Список допустимых схем ударений:
	allowed_stress_types = {
		'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
		'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
		'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
	}

--	INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
	if i.stress_type and not _.equals(i.stress_type, allowed_stress_types) then
		r.add_error(i, 'Ошибка: Неправильная схема ударения: ' .. i.stress_type)
	end

	_.ends(module, func)
end


-- @starts
function export.get_stress_schema(stress_type, adj, pronoun)
	func = "get_stress_schema"
	_.starts(module, func)

	local result = ''
	if adj then
		result = adj_stress.get_adj_stress_schema(stress_type)
	elseif pronoun then
		result = pronoun_stress.get_pronoun_stress_schema(stress_type)
	else
		result = noun_stress.get_noun_stress_schema(stress_type)
	end

	_.ends(module, func)
	return result
end


return export
