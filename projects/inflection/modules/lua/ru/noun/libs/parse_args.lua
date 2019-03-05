local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local function get_cyrl_animacy(index, gender)
	_.log_func('parse_args', 'get_cyrl_animacy')

	if _.extract(index, '^' .. gender .. 'о//' .. gender) then
		return 'an//in'
	elseif _.extract(index, '^' .. gender .. '//' .. gender .. 'о') then
		return 'in//an'
	elseif _.extract(index, '^' .. gender .. 'о') then
		return 'an'
	else
		return 'in'
	end
end


local function extract_gender_animacy(data)
	_.log_func('parse_args', 'extract_gender_animacy')

	local convert_animacy, orig_index, rest_index

	-- мо-жо - mf a
	-- ж//жо - f ina//a
	-- мо - m a
	-- с  - n ina
	data.pt = false

	if _.startswith(data.index, 'п') then
		data.adj = true
	elseif _.extract(data.index, '^м//ж') or _.extract(data.index, '^m//f') then
		data.gender = 'mf'
		data.animacy = 'in'
	elseif _.extract(data.index, '^м//с') or _.extract(data.index, '^m//n') then
		data.gender = 'mn'
		data.animacy = 'in'
	elseif _.extract(data.index, '^ж//м') or _.extract(data.index, '^f//m') then
		data.gender = 'fm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^ж//с') or _.extract(data.index, '^f//n') then
		data.gender = 'fn'
		data.animacy = 'in'
	elseif _.extract(data.index, '^с//м') or _.extract(data.index, '^n//m') then
		data.gender = 'nm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^с//ж') or _.extract(data.index, '^n//m') then
		data.gender = 'nm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^мо%-жо') or _.extract(data.index, '^mf a') then
		data.gender = 'f'
		data.animacy = 'an'
		data.common_gender = true
	elseif _.extract(data.index, '^мн') then
		data.gender = ''
		data.animacy = ''
		data.common_gender = false
		data.pt = true
		if _.extract(data.index, 'одуш') then
			data.animacy = 'an'
		elseif _.extract(data.index, 'неод') then
			data.animacy = 'in'
		end
		-- TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
		data.rest_index = data.index
	elseif _.extract(data.index, '^мс') then
		data.pronoun = true
	elseif _.extract(data.index, '^м') then
		data.gender = 'm'
		data.animacy = get_cyrl_animacy(data.index, 'м')
		data.common_gender = false
	elseif _.extract(data.index, '^ж') then
		data.gender = 'f'
		data.animacy = get_cyrl_animacy(data.index, 'ж')
		data.common_gender = false
	elseif _.extract(data.index, '^с') then
		data.gender = 'n'
		data.animacy = get_cyrl_animacy(data.index, 'с')
		data.common_gender = false
	else
		data.gender = _.extract(data.index, '^([mnf])')
		data.animacy = _.extract(data.index, '^[mnf] ([a-z/]+)')
		data.common_gender = false
		if data.animacy then
			convert_animacy = {}
			convert_animacy['in'] = 'in'
			convert_animacy['an'] = 'an'
			convert_animacy['ina'] = 'in'
			convert_animacy['a'] = 'an'
			convert_animacy['a//ina'] = 'an//in'
			convert_animacy['ina//a'] = 'in//an'
			convert_animacy['anin'] = 'an//in'
			convert_animacy['inan'] = 'in//an'
			data.animacy = convert_animacy[data.animacy]
		end
	end

	-- Удаляем теперь соответствующий кусок индекса
	if (data.gender or data.gender == '') and data.animacy and not data.adj and not data.pronoun then
		_.log_value(data.index, 'data.index')
		orig_index = mw.text.trim(data.index)

--		local test1 = _.replaced(data.index, '^mf a ?', '')
--		mw.log('test1 = ' .. mw.text.trim(test1))
--
--		local test2 = _.replaced(data.index, '^mf a ', '')
--		mw.log('test2 = ' .. mw.text.trim(test2))
--
--		local test3 = _.replaced(data.index, 'mf a ', '')
--		mw.log('test3 = ' .. mw.text.trim(test3))
--
--		local test4 = _.replaced(data.index, 'mf a', '')
--		mw.log('test4 = ' .. mw.text.trim(test4))
--
--		local test5 = mw.text.trim(_.replaced(data.index, '^mf a ?', ''))
--		mw.log('test5 = ' .. test5)
--
--		local test6 = _.replaced(data.index, '^mf a ?', '')
--		mw.log('test6 = ' .. test6)
--		local test7 = mw.text.trim(test6)
--		mw.log('test7 = ' .. test7)

		-- TODO: Simplify things a bit here (сделать циклом!):

		rest_index = _.replaced(data.index, '^mf a ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "mf a" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^[mnf]+ [a-z/]+ ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "[mnf] [in/an]" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^мн%.? неод%.? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн. неод." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^мн%.? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^[-мжсо/]+%,? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "м/ж/с/мо/жо/со/..." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		return {error = 'TODO'}  -- dict -- TODO: process such errors
	elseif data.adj then
		_.log_value(data.index, 'data.index (п)')
		orig_index = mw.text.trim(data.index)

		rest_index = _.replaced(data.index, '^п ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "п" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
	elseif data.pronoun then
		_.log_value(data.index, 'data.index (мс)')
		orig_index = mw.text.trim(data.index)

		rest_index = _.replaced(data.index, '^мс ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мс" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
	end
end


local function init(data)
	_.log_func('parse_args', 'init')

	local several_vovwels, has_stress

--	INFO: Исходное слово без ударения:
	data.word = _.replaced(data.word_stressed, '́ ', '')

--	INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
	data.word_cleared = _.replaced(_.replaced(_.replaced(data.word, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

	if data.adj then
		if _.endswith(data.word_stressed, 'ся') then
			data.postfix = true
			data.stem = _.replaced(data.word, '{vowel}[йяе]ся$', '')
			data.stem_stressed = _.replaced(data.word_stressed, '{vowel}́ ?[йяе]ся$', '')
		else
			data.stem = _.replaced(data.word, '{vowel}[йяе]$', '')
			data.stem_stressed = _.replaced(data.word_stressed, '{vowel}́ ?[йяе]$', '')
		end
	else
--		INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
		data.stem = _.replaced(data.word, '[аеёийоьыя]$', '')
		data.stem_stressed = _.replaced(data.word_stressed, '[аеёийоьыя]́ ?$', '')
	end

	_.log_value(data.word, 'data.word')
	_.log_value(data.stem, 'data.stem')
	_.log_value(data.stem_stressed, 'data.stem_stressed')

--  INFO: Случай, когда не указано ударение у слова:
	several_vovwels = _.contains_several(data.word_stressed, '{vowel+ё}')
	has_stress = _.contains(data.word_stressed, '[́ ё]')
	if several_vovwels and not has_stress then
		return {
			error='Ошибка: Не указано ударение в слове',
			error_category='Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)',
		}  -- dict
	end
end


local function angle_brackets(data)
	_.log_func('parse_args', 'angle_brackets')

	local another_index, pt, error

	another_index = _.extract(data.rest_index, '%<([^>]+)%>')
	if another_index then
		pt = data.pt
		if not pt then
			data.output_gender = data.gender
			data.output_animacy = data.animacy
		end
		data.orig_index = data.index
		data.index = another_index
		error = extract_gender_animacy(data)
		data.pt = pt
		if error then return error end

		_.log_value(data.adj, 'data.adj')
		if data.adj then  -- Для прилагательных надо по-особенному
			error = init(data)
			if error then return data, error end
		end
	end
end


function export.parse(base, args)
	_.log_func('parse_args', 'parse')

	local data, error, parts, n_parts, data1, data2
	local index_parts, words_parts, n_sub_parts, data_copy

--	INFO: Достаём значения из параметров:
	data = {}  -- AttrDict
	data.base = base
	data.args = args
	data.index = mw.text.trim(args['индекс'])
	data.word_stressed = mw.text.trim(args['слово'])

	_.log_value(data.index, 'data.index')
	_.log_value(data.word_stressed, 'data.word_stressed')

	-- mw.log('')
	-- mw.log('==================================================')
	-- mw.log('args: ' .. tostring(data.index) .. ' | ' .. tostring(data.word_stressed))
	-- mw.log('--------------------------------------------------')

	-- -------------------------------------------------------------------------

	_.log_info('Получение информации о роде и одушевлённости')

	error = extract_gender_animacy(data)

	if error then return data, error end

	_.log_value(data.gender, 'data.gender')
	_.log_value(data.animacy, 'data.animacy')
	_.log_value(data.common_gender, 'data.common_gender')
	_.log_value(data.adj, 'data.adj')
	_.log_value(data.pronoun, 'data.pronoun')
	_.log_value(data.pt, 'data.pt')
	_.log_value(data.rest_index, 'data.rest_index')

--	INFO: stem, stem_stressed, etc.
	error = init(data)
	if error then return data, error end

--	INFO: Случай, если род или одушевлённость не указаны:
	if (not data.gender or not data.animacy) and not data.pt then
		return data, {}  -- dict -- INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
	end

--	INFO: Проверяем случай с вариациями:
	parts = mw.text.split(data.rest_index, '//')
	n_parts = table.getn(parts)

	if n_parts == 1 then  -- INFO: Дополнительных вариаций нет
		if _.contains(data.animacy, '//') then  -- INFO: Случаи 'in//an' и 'an//in'
--			INFO: Клонируем две вариации на основании текущих данных
			data1 = mw.clone(data)
			data2 = mw.clone(data)

--			INFO: Устанавливаем для них соответствующую вариацию одушевлённости
			data1.animacy = mw.ustring.sub(data.animacy, 1, 2)
			data2.animacy = mw.ustring.sub(data.animacy, 5, 6)

--			INFO: Заполняем атрибут с вариациями
			data.sub_cases = {data1, data2}  -- list

			return data, nil
			-- TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
		end

		-- _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

		index_parts = mw.text.split(data.rest_index, '%+')
		words_parts = mw.text.split(data.word_stressed, '-')
		n_sub_parts = table.getn(index_parts)
		if n_sub_parts > 1 then
			data.sub_parts = {}  -- list
			for i = 1, n_sub_parts do
				data_copy = mw.clone(data)
				data_copy.word_stressed = words_parts[i]

				error = init(data_copy)
				if error then return data, error end

				data_copy.rest_index = index_parts[i]

				error = angle_brackets(data_copy)
				if error then return data, error end

				table.insert(data.sub_parts, data_copy)
			end
			return data, nil
		end

		error = angle_brackets(data)
		if error then return data, error end

		if _.contains(data.rest_index, '%[%([12]%)%]') or _.contains(data.rest_index, '%[[①②]%]') then
--			INFO: Клонируем две вариации на основании текущих данных
			data1 = mw.clone(data)
			data2 = mw.clone(data)

--			INFO: Устанавливаем факультативность (первый случай):
			data1.rest_index = _.replaced(data1.rest_index, '%[(%([12]%))%]', '')
			data1.rest_index = _.replaced(data1.rest_index, '%[([①②])%]', '')

--			INFO: Устанавливаем факультативность (второй случай):
			data2.rest_index = _.replaced(data2.rest_index, '%[(%([12]%))%]', '%1')
			data2.rest_index = _.replaced(data2.rest_index, '%[([①②])%]', '%1')
			data2.rest_index = _.replaced(data2.rest_index, '%*', '')

--			INFO: Заполняем атрибут с вариациями
			data.sub_cases = {data1, data2}  -- list

			return data, nil
		end

	elseif n_parts == 2 then  -- INFO: Вариации "//" для ударения (и прочего индекса)
		_.log_info('> Случай с вариациями //')

		if _.contains(data.animacy, '//') then
--			INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
			return data, {error='Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?'}  -- dict
		end

--		INFO: Клонируем две вариации на основании текущих данных
		data1 = mw.clone(data)
		data2 = mw.clone(data)

--		INFO: Предпогалаем, что у нас пока не "полная" вариация (не затрагивающая род)
		data1.rest_index = parts[1]
		data2.rest_index = parts[2]

--		INFO: Проверяем, не находится ли род+одушевлённость во второй вариации
		data2.index = parts[2]  -- INFO: Для этого инициируем `.index`, чтобы его обработала функция `extract_gender_animacy`
		extract_gender_animacy(data2)

--		INFO: Если рода и одушевлённости во второй вариации нет (простой случай):
		if not data2.gender and not data2.animacy then
--			INFO: Восстанавливаем прежние общие значения:
			data2.gender = data.gender
			data2.animacy = data.animacy
			data2.common_gender = data.common_gender

--		INFO: Проверка на гипотетическую ошибку в алгоритме:
		elseif not data2.gender and data2.animacy or data2.gender and not data2.animacy then
			return data, {error='Странная ошибка: После `extract_gender_animacy` не может быть частичной заполненности полей' }  -- dict

--		INFO: Если что-то изменилось, значит, прошёл один из случаев, и значит у нас "полная" вариация (затрагивающая род)
		elseif data.gender ~= data2.gender or data.animacy ~= data2.animacy or data.common_gender ~= data2.common_gender then
			data.rest_index = nil  -- INFO: Для случая "полной" вариации понятие `rest_index`, наверное, не определено
		end
		data2.index = data.index  -- INFO: Возвращаем исходное значение `index`; инвариант: оно всегда будет равно исходному индексу

--		INFO: Заполняем атрибут с вариациями
		data.sub_cases = {data1, data2}  -- list

	else  -- INFO: Какая-то ошибка, слишком много "//" в индексе
		return data, {error='Ошибка: Слишком много частей для "//"'}  -- dict
	end

	return data, nil  -- INFO: `nil` здесь -- признак, что нет ошибок
end


return export
