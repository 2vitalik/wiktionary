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
function export.get_stress_schema(i)
	func = "get_stress_schema"
	_.starts(module, func)

	if i.adj then
		i.stress_schema = adj_stress.get_adj_stress_schema(i.stress_type)
	elseif i.pronoun then
		i.stress_schema = pronoun_stress.get_pronoun_stress_schema(i.stress_type)
	else
		i.stress_schema = noun_stress.get_noun_stress_schema(i.stress_type)
	end

	_.ends(module, func)
end


return export
