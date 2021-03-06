local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process')  -- '.'  -- '_' /process
local angle = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/angle_brackets')  -- '.'
local init_stem = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/init_stem')  -- '.'
local noun_parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/noun')  -- '.'
local v = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/variations')  -- '.'
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '.'


local module = 'init.parse'


-- @starts
function export.parse(base, args, frame)
	func = "parse"
	_.starts(module, func)

	local i = {}  -- AttrDict
	i.word = {}  -- AttrDict
	i.stem = {}  -- AttrDict
	i.parts = {}  -- AttrDict
	i.result = {}  -- AttrDict
	i.result.error = ''
	i.has_index = true  -- изначально предполагаем, что индекс есть

--	INFO: Достаём значения из параметров:
	i.base = base
	i.args = args
	i.frame = frame
	i.lang = mw.text.trim(args['lang'])
	i.unit = mw.text.trim(args['unit'])
	i.index = mw.text.trim(args['индекс'])
	i.word.stressed = mw.text.trim(args['слово'])
	i.noun = (i.unit == 'noun')

	_.log_value(i.index, 'i.index')
	_.log_value(i.word.stressed, 'i.word.stressed')

	-- mw.log('')
	-- mw.log('==================================================')
	-- mw.log('args: ' .. tostring(i.index) .. ' | ' .. tostring(i.word.stressed))
	-- mw.log('--------------------------------------------------')

	_.log_info('Получение информации о роде и одушевлённости')

	if i.noun then  -- fixme
		noun_parse.extract_gender_animacy(i)
		if e.has_error(i) then
			return _.returns(module, func, i)
		end

		-- Будем расчитывать оба числа сразу вместе
		i.calc_sg = true
		i.calc_pl = true

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

		-- Будем расчитывать позже по отдельности
		i.calc_sg = false
		i.calc_pl = false
	end

	_.log_value(i.pt, 'i.pt')
	_.log_value(i.rest_index, 'i.rest_index')

--	INFO: stem, stem.stressed, etc.
	init_stem.init_stem(i)
	if e.has_error(i) then
		return _.returns(module, func, i)
	end

	if i.noun then
--		INFO: Случай, если род или одушевлённость не указаны:
		if (not i.gender or not i.animacy) and not i.pt then
--			INFO: Не показываем ошибку, просто считаем, что род или одушевлённость *ещё* не указаны
			return _.returns(module, func, i)
		end
	end

--	INFO: Проверяем случай с вариациями:
	local variations = mw.text.split(i.rest_index, '//')
	local n_variations = table.getn(variations)

	if n_variations == 1 then  -- INFO: Дополнительных вариаций нет
		if _.contains(i.animacy, '//') then  -- INFO: Случаи 'in//an' и 'an//in'
			v.process_animacy_variations(i)
			return _.returns(module, func, i)
			-- TODO: А что если in//an одновременно со следующими случаями "[]" или "+"
		end

		-- _.log_info('Случай с "+" (несколько составных частей слова через дефис)')

		local plus_index = mw.text.split(i.rest_index, '%+')
		local plus_words = mw.text.split(i.word.stressed, '-')
		local n_plus = table.getn(plus_index)
		if n_plus > 1 then
			v.process_plus(i, plus_words, plus_index)
			return _.returns(module, func, i)
		end

		if i.noun then
			angle.angle_brackets(i)
			if e.has_error(i) then
				return _.returns(module, func, i)
			end
		end

		if _.contains(i.rest_index, '%[%([12]%)%]') or _.contains(i.rest_index, '%[[①②]%]') then
			v.process_brackets_variations(i)
			return _.returns(module, func, i)
		end

	elseif n_variations == 2 then  -- INFO: Вариации "//" для ударения (и прочего индекса)
		_.log_info('> Случай с вариациями //')

		if _.contains(i.animacy, '//') then
--			INFO: Если используются вариации одновременно и отдельно для одушевлённости и ударения
			e.add_error(i, 'Ошибка: Случай с несколькими "//" пока не реализован. Нужно реализовать?')
			return _.returns(module, func, i)
		end

		v.process_full_variations(i, variations)

		return _.returns(module, func, i)

	else  -- INFO: Какая-то ошибка, слишком много "//" в индексе
		e.add_error(i, 'Ошибка: Слишком много частей для "//"')
		return _.returns(module, func, i)
	end

	_.ends(module, func)
	return p.process(i)
end


return export
