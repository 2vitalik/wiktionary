local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local noun_parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/noun')  -- '..'
local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process')  -- '..'  -- '_' /process


local module = 'init.parse.common'


-- @starts
local function init(info)
	func = "init"
	_.starts(module, func)

	local several_vovwels, has_stress

--	INFO: Исходное слово без ударения:
	info.word.unstressed = _.replaced(info.word.stressed, '́ ', '')

--	INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
	info.word.cleared = _.replaced(_.replaced(_.replaced(info.word.unstressed, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

	if info.adj then
		if _.endswith(info.word.stressed, 'ся') then
			info.postfix = true
			info.stem.unstressed = _.replaced(info.word.unstressed, '{vowel}[йяе]ся$', '')
			info.stem.stressed = _.replaced(info.word.stressed, '{vowel}́ ?[йяе]ся$', '')
		else
			info.stem.unstressed = _.replaced(info.word.unstressed, '{vowel}[йяе]$', '')
			info.stem.stressed = _.replaced(info.word.stressed, '{vowel}́ ?[йяе]$', '')
		end
	else
--		INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
		info.stem.unstressed = _.replaced(info.word.unstressed, '[аеёийоьыя]$', '')
		info.stem.stressed = _.replaced(info.word.stressed, '[аеёийоьыя]́ ?$', '')
	end

	_.log_value(info.word.unstressed, 'info.word.unstressed')
	_.log_value(info.stem.unstressed, 'info.stem.unstressed')
	_.log_value(info.stem.stressed, 'info.stem.stressed')

--  INFO: Случай, когда не указано ударение у слова:
	several_vovwels = _.contains_several(info.word.stressed, '{vowel+ё}')
	has_stress = _.contains(info.word.stressed, '[́ ё]')
	if several_vovwels and not has_stress then
		_.log_info('Ошибка: Не указано ударение в слове')
		_.ends(module, func)
		return {
			error='Ошибка: Не указано ударение в слове',
			error_category='Ошибка в шаблоне "сущ-ru": не указано ударение в слове',
		}  -- dict
	end

	_.ends(module, func)
end


-- @starts
local function angle_brackets(info)
	func = "angle_brackets"
	_.starts(module, func)

	local another_index, pt, error

	another_index = _.extract(info.rest_index, '%<([^>]+)%>')
	if another_index then
		pt = info.pt
		if not pt then
			info.output_gender = info.gender
			info.output_animacy = info.animacy
		end
		info.orig_index = info.index
		info.index = another_index
		error = noun_parse.extract_gender_animacy(info)
		info.pt = pt
		if error then
			_.ends(module, func)
			return error
		end

		_.log_value(info.adj, 'info.adj')
		if info.adj then  -- Для прилагательных надо по-особенному?
			error = init(info)
			if error then
				_.ends(module, func)
				return error
			end
		end
	end

	_.ends(module, func)
end


-- @starts
function export.parse(base, args)
	func = "parse"
	_.starts(module, func)

	local info = {}  -- AttrDict
	info.word = {}  -- AttrDict                                      --
	info.stem = {}  -- AttrDict                                      --

--	INFO: Достаём значения из параметров:
	info.base = base
	info.args = args
	info.lang = mw.text.trim(args['lang'])
	info.unit = mw.text.trim(args['unit'])
	info.index = mw.text.trim(args['индекс'])
	info.word.stressed = mw.text.trim(args['слово'])
	info.noun = (info.unit == 'noun')

	_.log_value(info.index, 'info.index')
	_.log_value(info.word.stressed, 'info.word.stressed')

	-- mw.log('')
	-- mw.log('==================================================')
	-- mw.log('args: ' .. tostring(info.index) .. ' | ' .. tostring(info.word.stressed))
	-- mw.log('--------------------------------------------------')

	_.log_info('Получение информации о роде и одушевлённости')

	if info.noun then  -- fxime
		local error = noun_parse.extract_gender_animacy(info)
		if error then
			_.ends(module, func)
			return info, error
		end

		_.log_value(info.gender, 'info.gender')
		_.log_value(info.animacy, 'info.animacy')
		_.log_value(info.common_gender, 'info.common_gender')
		_.log_value(info.adj, 'info.adj')
		_.log_value(info.pronoun, 'info.pronoun')
	else
		info.gender = ''  -- fixme
		info.animacy = ''  -- fixme
		info.adj = true  -- fixme
		info.rest_index = info.index  -- fixme
	end

	_.log_value(info.pt, 'info.pt')
	_.log_value(info.rest_index, 'info.rest_index')

--	INFO: stem, stem.stressed, etc.
	-- todo: rename to `create_info`:
	local error = init(info)
	if error then
		_.ends(module, func)
		return info, error
	end

	if info.noun then
--		INFO: Случай, если род или одушевлённость не указаны:
		if (not info.gender or not info.animacy) and not info.pt then
			_.ends(module, func)
			return info, {}  -- dict -- INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
		end
	end

--	INFO: Проверяем случай с вариациями:
	local parts = mw.text.split(info.rest_index, '//')
	local n_parts = table.getn(parts)

	if n_parts == 1 then  -- INFO: Дополнительных вариаций нет
		if _.contains(info.animacy, '//') then  -- INFO: Случаи 'in//an' и 'an//in'
--			INFO: Клонируем две вариации на основании текущих данных
			local info_1 = mw.clone(info)
			local info_2 = mw.clone(info)

--			INFO: Устанавливаем для них соответствующую вариацию одушевлённости
			info_1.animacy = mw.ustring.sub(info.animacy, 1, 2)
			info_2.animacy = mw.ustring.sub(info.animacy, 5, 6)

--			INFO: Заполняем атрибут с вариациями
			info.variations = {p.process(info_1), p.process(info_2)}  -- list

			_.ends(module, func)
			return p.process(info), nil
			-- TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
		end

		-- _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

		local index_parts = mw.text.split(info.rest_index, '%+')
		local words_parts = mw.text.split(info.word.stressed, '-')
		local n_sub_parts = table.getn(index_parts)
		if n_sub_parts > 1 then
			info.plus = {}  -- list
			for i = 1, n_sub_parts do
				local info_copy = mw.clone(info)
				info_copy.word.stressed = words_parts[i]

				error = init(info_copy)
				if error then
					_.ends(module, func)
					return info, error
				end

				info_copy.rest_index = index_parts[i]

				if info.noun then
					error = angle_brackets(info_copy)
					if error then
						_.ends(module, func)
						return info, error
					end
				end

				table.insert(info.plus, info_copy)
			end
			_.ends(module, func)
			return p.process(info), nil
		end

		if info.noun then
			error = angle_brackets(info)
			if error then
				_.ends(module, func)
				return info, error
			end
		end

		if _.contains(info.rest_index, '%[%([12]%)%]') or _.contains(info.rest_index, '%[[①②]%]') then
--			INFO: Клонируем две вариации на основании текущих данных
			local info_1 = mw.clone(info)
			local info_2 = mw.clone(info)

--			INFO: Устанавливаем факультативность (первый случай):
			info_1.rest_index = _.replaced(info_1.rest_index, '%[(%([12]%))%]', '')
			info_1.rest_index = _.replaced(info_1.rest_index, '%[([①②])%]', '')

--			INFO: Устанавливаем факультативность (второй случай):
			info_2.rest_index = _.replaced(info_2.rest_index, '%[(%([12]%))%]', '%1')
			info_2.rest_index = _.replaced(info_2.rest_index, '%[([①②])%]', '%1')
			info_2.rest_index = _.replaced(info_2.rest_index, '%*', '')

--			INFO: Заполняем атрибут с вариациями
			info.variations = {p.process(info_1), p.process(info_2)}  -- list

			_.ends(module, func)
			return p.process(info), nil
		end

	elseif n_parts == 2 then  -- INFO: Вариации "//" для ударения (и прочего индекса)
		_.log_info('> Случай с вариациями //')

		if _.contains(info.animacy, '//') then
--			INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
			_.ends(module, func)
			return info, {error='Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?'}  -- dict
		end

--		INFO: Клонируем две вариации на основании текущих данных
		local info_1 = mw.clone(info)
		local info_2 = mw.clone(info)

--		INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
		info_1.rest_index = parts[1]
		info_2.rest_index = parts[2]

		if info.noun then
--			INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
			info_2.index = parts[2]  -- INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
			noun_parse.extract_gender_animacy(info_2)
		end

--		INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
		if not info_2.gender and not info_2.animacy then
--			INFO: Восстанавливаем прежние общие значения:
			info_2.gender = info.gender
			info_2.animacy = info.animacy
			info_2.common_gender = info.common_gender

--		INFO: Проверка на гипотетическую ошибку в алгоритме:
		elseif not info_2.gender and info_2.animacy or info_2.gender and not info_2.animacy then
			_.ends(module, func)
			return info, {error='Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей' }  -- dict

--		INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
		elseif info.gender ~= info_2.gender or info.animacy ~= info_2.animacy or info.common_gender ~= info_2.common_gender then
			info.rest_index = nil  -- INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
		end
		info_2.index = info.index  -- INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

--		INFO: Заполняем атрибут с вариациями
		info.variations = {p.process(info_1), p.process(info_2)}  -- list

	else  -- INFO: Какая-то ошибка, слишком много "//" в индексе
		_.ends(module, func)
		return info, {error='Ошибка: Слишком много частей для "//"'}  -- dict
	end

	_.ends(module, func)
	return p.process(info), nil  -- INFO: `nil` здесь -- признак, что нет ошибок
end


return export
