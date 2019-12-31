local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local noun_parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/noun')  -- '..'
local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process')  -- '..'  -- '_' /process
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.parse.common'


-- @starts
local function init_info(i)  -- todo rename to `init_stem`
	func = "init_info"
	_.starts(module, func)

	local several_vowels, has_stress

--	INFO: Исходное слово без ударения:
	i.word.unstressed = _.replaced(i.word.stressed, '́ ', '')  -- todo: move outside this function

--	INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
	i.word.cleared = _.replaced(_.replaced(_.replaced(i.word.unstressed, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

	if i.adj then
		if _.endswith(i.word.stressed, 'ся') then
			i.postfix = true
			i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]ся$', '')
			i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]ся$', '')
		else
			i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]$', '')
			i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]$', '')
		end
	else
--		INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
		i.stem.unstressed = _.replaced(i.word.unstressed, '[аеёийоьыя]$', '')
		i.stem.stressed = _.replaced(i.word.stressed, '[аеёийоьыя]́ ?$', '')
	end

	_.log_value(i.word.unstressed, 'i.word.unstressed')
	_.log_value(i.stem.unstressed, 'i.stem.unstressed')
	_.log_value(i.stem.stressed, 'i.stem.stressed')

--  INFO: Случай, когда не указано ударение у слова:
	several_vowels = _.contains_several(i.word.stressed, '{vowel+ё}')
	has_stress = _.contains(i.word.stressed, '[́ ё]')
	if several_vowels and not has_stress then
		_.log_info('Ошибка: Не указано ударение в слове')
		e.add_error(i, 'Ошибка: Не указано ударение в слове')
		i.result.error_category = 'Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)'
	end

	_.ends(module, func)
end


-- @starts
local function angle_brackets(i)
	func = "angle_brackets"
	_.starts(module, func)

	local another_index = _.extract(i.rest_index, '%<([^>]+)%>')
	if another_index then
		local pt = i.pt
		if not pt then
			i.output_gender = i.gender
			i.output_animacy = i.animacy
		end
		i.orig_index = i.index
		i.index = another_index
		noun_parse.extract_gender_animacy(i)
		i.pt = pt
		if e.has_error(i) then
			return _.ends(module, func)
		end

		_.log_value(i.adj, 'i.adj')
		if i.adj then  -- fixme: Для прилагательных надо по-особенному?
			init_info(i)
			if e.has_error(i) then
				return _.ends(module, func)
			end
		end
	end

	_.ends(module, func)
end


-- @starts
function export.parse(base, args)
	func = "parse"
	_.starts(module, func)

	local i = {}  -- AttrDict
	i.word = {}  -- AttrDict                                      --
	i.stem = {}  -- AttrDict                                      --

--	INFO: Достаём значения из параметров:
	i.base = base
	i.args = args
	i.lang = mw.text.trim(args['lang'])
	i.unit = mw.text.trim(args['unit'])
	i.index = mw.text.trim(args['индекс'])
	i.word.stressed = mw.text.trim(args['слово'])
	i.noun = (i.unit == 'noun')

	i.parts = {}  -- AttrDict
	i.result = {}  -- AttrDict
	i.result.error = ''

	i.has_index = true  -- изначально предполагаем, что индекс есть

	_.log_value(i.index, 'i.index')
	_.log_value(i.word.stressed, 'i.word.stressed')

	-- mw.log('')
	-- mw.log('==================================================')
	-- mw.log('args: ' .. tostring(i.index) .. ' | ' .. tostring(i.word.stressed))
	-- mw.log('--------------------------------------------------')

	_.log_info('Получение информации о роде и одушевлённости')

	if i.noun then  -- fxime
		noun_parse.extract_gender_animacy(i)
		if e.has_error(i) then
			_.ends(module, func)
			return i
		end

		_.log_value(i.gender, 'i.gender')
		_.log_value(i.animacy, 'i.animacy')
		_.log_value(i.common_gender, 'i.common_gender')
		_.log_value(i.adj, 'i.adj')
		_.log_value(i.pronoun, 'i.pronoun')
	else
		i.gender = ''  -- fixme
		i.animacy = ''  -- fixme
		i.adj = true  -- fixme
		i.rest_index = i.index  -- fixme
	end

	_.log_value(i.pt, 'i.pt')
	_.log_value(i.rest_index, 'i.rest_index')

--	INFO: stem, stem.stressed, etc.
	init_info(i)  -- todo: rename to `init_stem`
	if e.has_error(i) then
		_.ends(module, func)
		return i
	end

	if i.noun then
--		INFO: Случай, если род или одушевлённость не указаны:
		if (not i.gender or not i.animacy) and not i.pt then
--			INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
			_.ends(module, func)
			return i
		end
	end

--	INFO: Проверяем случай с вариациями:
	local parts = mw.text.split(i.rest_index, '//')
	local n_parts = table.getn(parts)

	if n_parts == 1 then  -- INFO: Дополнительных вариаций нет
		if _.contains(i.animacy, '//') then  -- INFO: Случаи 'in//an' и 'an//in'
--			INFO: Клонируем две вариации на основании текущих данных
			local i_1 = mw.clone(i)
			local i_2 = mw.clone(i)

--			INFO: Устанавливаем для них соответствующую вариацию одушевлённости
			i_1.animacy = mw.ustring.sub(i.animacy, 1, 2)
			i_2.animacy = mw.ustring.sub(i.animacy, 5, 6)

--			INFO: Заполняем атрибут с вариациями
			i.variations = {p.process(i_1), p.process(i_2)}  -- list

			_.ends(module, func)
			return i
			-- TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
		end

		-- _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

		local index_parts = mw.text.split(i.rest_index, '%+')
		local words_parts = mw.text.split(i.word.stressed, '-')
		local n_sub_parts = table.getn(index_parts)
		if n_sub_parts > 1 then
			i.plus = {}  -- list
			for j = 1, n_sub_parts do
				local i_copy = mw.clone(i)
				i_copy.word.stressed = words_parts[i]

				init_info(i_copy)
				if e.has_error(i_copy) then
					e.add_error(i, i_copy.result.error)
					_.ends(module, func)
					return i
				end

				i_copy.rest_index = index_parts[i]

				if i.noun then
					angle_brackets(i_copy)
					if e.has_error(i_copy) then
						e.add_error(i, i_copy.result.error)
						_.ends(module, func)
						return i
					end
				end

				table.insert(i.plus, p.process(i_copy))
			end
			_.ends(module, func)
			return i
		end

		if i.noun then
			angle_brackets(i)
			if e.has_error(i) then
				_.ends(module, func)
				return i
			end
		end

		if _.contains(i.rest_index, '%[%([12]%)%]') or _.contains(i.rest_index, '%[[①②]%]') then
--			INFO: Клонируем две вариации на основании текущих данных
			local i_1 = mw.clone(i)
			local i_2 = mw.clone(i)

--			INFO: Устанавливаем факультативность (первый случай):
			i_1.rest_index = _.replaced(i_1.rest_index, '%[(%([12]%))%]', '')
			i_1.rest_index = _.replaced(i_1.rest_index, '%[([①②])%]', '')

--			INFO: Устанавливаем факультативность (второй случай):
			i_2.rest_index = _.replaced(i_2.rest_index, '%[(%([12]%))%]', '%1')
			i_2.rest_index = _.replaced(i_2.rest_index, '%[([①②])%]', '%1')
			i_2.rest_index = _.replaced(i_2.rest_index, '%*', '')

--			INFO: Заполняем атрибут с вариациями
			i.variations = {p.process(i_1), p.process(i_2)}  -- list

			_.ends(module, func)
			return i
		end

	elseif n_parts == 2 then  -- INFO: Вариации "//" для ударения (и прочего индекса)
		_.log_info('> Случай с вариациями //')

		if _.contains(i.animacy, '//') then
--			INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
			e.add_error(i, 'Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')
			_.ends(module, func)
			return i
		end

--		INFO: Клонируем две вариации на основании текущих данных
		local i_1 = mw.clone(i)
		local i_2 = mw.clone(i)

--		INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
		i_1.rest_index = parts[1]
		i_2.rest_index = parts[2]

		if i.noun then
--			INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
			i_2.index = parts[2]  -- INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
			noun_parse.extract_gender_animacy(i_2)
		end

--		INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
		if not i_2.gender and not i_2.animacy then
--			INFO: Восстанавливаем прежние общие значения:
			i_2.gender = i.gender
			i_2.animacy = i.animacy
			i_2.common_gender = i.common_gender

--		INFO: Проверка на гипотетическую ошибку в алгоритме:
		elseif not i_2.gender and i_2.animacy or i_2.gender and not i_2.animacy then
			e.add_error(i, 'Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей')
			_.ends(module, func)
			return i

--		INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
		elseif i.gender ~= i_2.gender or i.animacy ~= i_2.animacy or i.common_gender ~= i_2.common_gender then
			i.rest_index = nil  -- INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
		end
		i_2.index = i.index  -- INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

--		INFO: Заполняем атрибут с вариациями
		i.variations = {p.process(i_1), p.process(i_2)}  -- list

		_.ends(module, func)
		return i

	else  -- INFO: Какая-то ошибка, слишком много "//" в индексе
		e.add_error(i, 'Ошибка: Слишком много частей для "//"')
		_.ends(module, func)
		return i
	end

	_.ends(module, func)
	return p.process(i)
end


return export
