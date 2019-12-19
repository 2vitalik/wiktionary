local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local adj_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/adj')  -- '..'
local pronoun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/pronoun')  -- '..'
local noun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/noun')  -- '..'


local module = 'init.stress'


-- @starts
function export.extract_stress_type(rest_index)
	func = "extract_stress_type"
	_.starts(module, func)

	--    OLD: Старая версия кода:
--	local stress_regexp = "([abcdef][′']?[′']?)"
--	local stress_regexp2 = '(' .. stress_regexp .. '.*//.*' .. stress_regexp .. ')'
--	stress_regexp = '(' .. stress_regexp .. '(% ?.*))'
--	data.stress_type = _.extract(rest_index, stress_regexp2)
--	if not data.stress_type then
--		data.stress_type = _.extract(rest_index, stress_regexp)
--	end
	local stress_type, allowed_stress_types

--	INFO: Извлечение ударения из оставшейся части индекса:
	stress_type = _.extract(rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

--	INFO: Замена особых апострофов в ударении на обычные:
	if stress_type then
		stress_type = _.replaced(stress_type, '′', "'")
	end

--	INFO: Список допустимых схем ударений:
	allowed_stress_types = {
		'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
		'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
		'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
	}

--	INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
	if stress_type and not _.equals(stress_type, allowed_stress_types) then
		_.ends(module, func)
		return stress_type, {error='Ошибка: Неправильная схема ударения: ' .. stress_type}  -- dict
	end

	_.ends(module, func)
	return stress_type, nil  -- INFO: `nil` здесь -- признак, что нет ошибок
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
