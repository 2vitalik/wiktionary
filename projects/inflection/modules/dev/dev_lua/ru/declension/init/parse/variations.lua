local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process')  -- '..'  -- '_' /process
local angle = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/angle_brackets')  -- '..'
local init_stem = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/init_stem')  -- '..'
local noun_parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/noun')  -- '..'
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.parse.variations'


-- @starts
function export.process_animacy_variations(i)
	func = "process_animacy_variations"
	_.starts(module, func)

--	INFO: Клонируем две вариации на основании текущих данных
	local i_1 = mw.clone(i)
	local i_2 = mw.clone(i)

--	INFO: Устанавливаем для них соответствующую вариацию одушевлённости
	i_1.animacy = mw.ustring.sub(i.animacy, 1, 2)
	i_2.animacy = mw.ustring.sub(i.animacy, 5, 6)

--	INFO: Заполняем атрибут с вариациями
	i.variations = {p.process(i_1), p.process(i_2)}  -- list

	_.ends(module, func)
end


-- @starts
function export.process_plus(i, plus_words, plus_index)
	func = "process_plus"
	_.starts(module, func)

	i.plus = {}  -- list
	local n_plus = table.getn(plus_index)
	for j = 1, n_plus do
		local i_copy = mw.clone(i)
		i_copy.word.stressed = plus_words[j]

		init_stem.init_stem(i_copy)
		if e.has_error(i_copy) then
			e.add_error(i, i_copy.result.error)
			return _.ends(module, func)
		end

		i_copy.rest_index = plus_index[j]

		if i.noun then
			angle.angle_brackets(i_copy)
			if e.has_error(i_copy) then
				e.add_error(i, i_copy.result.error)
				return _.ends(module, func)
			end
		end

		table.insert(i.plus, p.process(i_copy))
	end

	_.ends(module, func)
end


-- @starts
function export.process_brackets_variations(i)
	func = "process_brackets_variations"
	_.starts(module, func)

--	INFO: Клонируем две вариации на основании текущих данных
	local i_1 = mw.clone(i)
	local i_2 = mw.clone(i)

--	INFO: Устанавливаем факультативность (первый случай):
	i_1.rest_index = _.replaced(i_1.rest_index, '%[(%([12]%))%]', '')
	i_1.rest_index = _.replaced(i_1.rest_index, '%[([①②])%]', '')

--	INFO: Устанавливаем факультативность (второй случай):
	i_2.rest_index = _.replaced(i_2.rest_index, '%[(%([12]%))%]', '%1')
	i_2.rest_index = _.replaced(i_2.rest_index, '%[([①②])%]', '%1')
	i_2.rest_index = _.replaced(i_2.rest_index, '%*', '')

--	INFO: Заполняем атрибут с вариациями
	i.variations = {p.process(i_1), p.process(i_2)}  -- list

	_.ends(module, func)
end


-- @starts
function export.process_full_variations(i, parts)
	func = "process_full_variations"
	_.starts(module, func)

--	INFO: Клонируем две вариации на основании текущих данных
	local i_1 = mw.clone(i)
	local i_2 = mw.clone(i)

--	INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
	i_1.rest_index = parts[1]
	i_2.rest_index = parts[2]

	if i.noun then
--		INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
		i_2.index = parts[2]  -- INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
		noun_parse.extract_gender_animacy(i_2)
	end

--	INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
	if not i_2.gender and not i_2.animacy then
--		INFO: Восстанавливаем прежние общие значения:
		i_2.gender = i.gender
		i_2.animacy = i.animacy
		i_2.common_gender = i.common_gender

--	INFO: Проверка на гипотетическую ошибку в алгоритме:
	elseif not i_2.gender and i_2.animacy or i_2.gender and not i_2.animacy then
		e.add_error(i, 'Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей')
		return _.ends(module, func)

--	INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
	elseif i.gender ~= i_2.gender or i.animacy ~= i_2.animacy or i.common_gender ~= i_2.common_gender then
		i.rest_index = nil  -- INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
	end
	i_2.index = i.index  -- INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

--	INFO: Заполняем атрибут с вариациями
	i.variations = {p.process(i_1), p.process(i_2)}  -- list

	_.ends(module, func)
end


return export
