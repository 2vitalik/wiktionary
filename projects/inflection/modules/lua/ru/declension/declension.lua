local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse_args = require('Module:' .. dev_prefix .. 'inflection/ru/declension/parse_args')
local stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/stress')
local stem_type = require('Module:' .. dev_prefix .. 'inflection/ru/declension/stem_type')
local endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/endings')
local reducable = require('Module:' .. dev_prefix .. 'inflection/ru/declension/reducable')
local form = require('Module:' .. dev_prefix .. 'inflection/ru/declension/form')
local index = require('Module:' .. dev_prefix .. 'inflection/ru/declension/index')
local result = require('Module:' .. dev_prefix .. 'inflection/ru/declension/result')

local noun_form = require('Module:' .. dev_prefix .. 'inflection/ru/noun/form')  -- ''


local function prepare_stash()
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


local function main_sub_algorithm(data)
	_.log_info('Вычисление схемы ударения')

	data.stress_schema = stress.get_stress_schema(data.stress_type, data.adj, data.pronoun)

	_.log_table(data.stress_schema['stem'], "data.stress_schema['stem']")
	_.log_table(data.stress_schema['ending'], "data.stress_schema['ending']")

	data.endings = endings.get_endings(data)

	data.stems = {}  -- dict
	stress.apply_stress_type(data)
	_.log_table(data.stems, 'data.stems')
	_.log_table(data.endings, 'data.endings')


--	-- *** для случая с расстановкой ударения  (см. ниже)
--	local orig_stem = data.stem
--	if _.contains(data.rest_index, {'%(2%)', '②'}) then
--		orig_stem = _.replaced(data.stems['gen_pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
--		mw.log('> Another `orig_stem`: ' .. tostring(orig_stem))
--	end

	-- reducable
	data.rest_index = reducable.apply_specific_degree(data.stems, data.endings, data.word, data. stem, data. stem_type, data.gender, data.animacy, data. stress_type, data.rest_index, data)
	reducable.apply_specific_reducable(data.stems, data.endings, data.word, data.stem, data.stem_type, data.gender, data.stress_type, data.rest_index, data, false)

	if not _.equals(data.stress_type, {"f", "f'"}) and _.contains(data.rest_index, '%*') then
		mw.log('# Обработка случая на препоследний слог основы при чередовании')
		orig_stem = data.stem
		if data.forced_stem then
			orig_stem = data.forced_stem
		end
		for key, stem in pairs(data.stems) do
--			mw.log(' - ' .. key .. ' -> ' .. stem)
--			mw.log('Ударение на основу?')
--			mw.log(data.stress_schema['stem'][key])
			if not _.contains(stem, '[́ ё]') and data.stress_schema['stem'][key] then
				-- *** случай с расстановкой ударения  (см. выше)
				-- "Дополнительные правила об ударении", стр. 34
				old_value = data.stems[key]
				-- mw.log('> ' .. key .. ' (old): ' .. tostring(old_value))
				if data.stems[key] ~= orig_stem then  -- попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
					data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
					if not _.contains(data.stems[key], '[́ ё]') then -- если предпоследнего слога попросту нет
						-- сделаем хоть последний ударным
						data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
					end
				else
					data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
				end
				-- mw.log('> ' .. key .. ' (new): ' .. tostring(data.stems[key]))
				mw.log('  - [' .. key .. '] = "' .. tostring(old_value) .. '" -> "' .. tostring(data.stems[key]) .. '"')
			end
		end
	end

	-- Специфика по "ё"
	if _.contains(data.rest_index, 'ё') and not _.contains(data.endings['gen_pl'], '{vowel+ё}') and not _.contains(data.stems['gen_pl'], 'ё') then
		data.stems['gen_pl'] = _.replaced(data.stems['gen_pl'], 'е́?([^е]*)$', 'ё%1')
		data.rest_index = data.rest_index .. 'ё'  -- ???
	end
end


local function main_algorithm(data)
	_.log_func('declension', 'main_algorithm')

	local error, keys, forms, orig_stem, for_category, old_value, cases

	_.log_value(data.rest_index, 'data.rest_index')

	-- -------------------------------------------------------------------------

	_.log_info('Извлечение информации об ударении')

	data.stress_type, error = stress.extract_stress_type(data.rest_index)

	if error then return result.finalize(data, error) end

	_.log_value(data.stress_type, 'data.stress_type')

--	INFO: Если ударение не указано:
	if not data.stress_type then

--		INFO: Может быть это просто несклоняемая схема:
		if _.contains(data.rest_index, '^0') then
			keys = {
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			}  -- list
			forms = {}  -- dict
			forms['зализняк'] = '0'
			forms['скл'] = 'не'
			for i, key in pairs(keys) do  -- list
				forms[key] = data.word_stressed
			end
			return result.finalize(data, forms)

--		INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
		elseif _.has_value(data.rest_index) then
			return result.finalize(data, {error='Нераспознанная часть индекса: ' .. data.rest_index})  -- b-dict

--		INFO: Если индекса вообще нет, то и формы просто не известны:
		else
			return result.finalize(data, {})  -- b-dict
		end
	end

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem_stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(data.stem_stressed, '[́ ё]') then  -- and not data.absent_stress ??
		if _.equals(data.stress_type, {"f", "f'"}) then
			data.stem_stressed = _.replaced(data.stem_stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(data.rest_index, '%*') then
			-- pass  -- *** поставим ударение ниже, после чередования
		else
			data.stem_stressed = _.replaced(data.stem_stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(data.stem_stressed, 'data.stem_stressed')

	-- -------------------------------------------------------------------------

	_.log_info('Определение типа основы')

	data.stem_type, data.base_stem_type = stem_type.get_stem_type(data.stem, data.word, data.gender, data.adj, data.rest_index)

	_.log_value(data.stem_type, 'data.stem_type')
	_.log_value(data.base_stem_type, 'data.base_stem_type')

	if not data.stem_type then
		return result.finalize(data, {error='Неизвестный тип основы'})  -- b-dict
	end

	-- -------------------------------------------------------------------------

	if data.noun then
		main_sub_algorithm(data)
		forms = form.generate_forms(data)  -- TODO: Rename to `out_args` ?

	elseif data.adj then
		forms = {}
		cases = {
			'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
			'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			'srt_sg', 'srt_pl',
		}  -- list

		genders = {'', 'm', 'n', 'f'}
		for i, gender in pairs(genders) do  -- list
			data.gender = gender

			main_sub_algorithm(data)

			if gender == '' then
				forms = form.generate_forms(data)  -- TODO: Rename to `out_args` ?
			else
				sub_forms = form.generate_forms(data)
				for i, case in pairs(cases) do  -- list
					key = case .. '_' .. gender
					forms[key] = sub_forms[case]
				end
			end
		end
		forms['acc_sg_m_a'] = forms['gen_sg_m']
		forms['acc_sg_m_n'] = forms['nom_sg_m']
		forms['acc_pl_a'] = forms['gen_pl']
		forms['acc_pl_n'] = forms['nom_pl']

		data.gender = ''  -- redundant?
	end

	forms['зализняк1'] = index.get_zaliznyak(data.stem_type, data.stress_type, data.rest_index)

	for_category = forms['зализняк1']
	for_category = _.replaced(for_category, '①', '(1)')
	for_category = _.replaced(for_category, '②', '(2)')
	for_category = _.replaced(for_category, '③', '(3)')
	forms['зализняк'] = for_category

	return forms
end


function export.forms(base, args, frame)
	mw.log('==================================================')
	_.log_func('declension', 'forms')

	local data, error, forms
	local data1, data2, forms1, forms2, sub_forms

--	INFO: `base` здесь нигде не используется, но теоретически может понадобиться для других языков

--	INFO: Для отладки:
--	if true then return '`forms` executed' end

--	INFO: Заполняем шаблоны для регулярок
	prepare_stash()

--	INFO: Достаём всю информацию из аргументов (args): основа, род, одушевлённость и т.п.
	data, error = parse_args.parse(base, args)
	if error then
		forms = result.finalize(data, error)
		_.log_table(forms, "forms")
		return forms
	end

	data.frame = frame

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	forms = {}  -- dict
	if data.sub_cases then
		_.log_info("Случай с вариациями '//'")
		data1 = data.sub_cases[1]
		data2 = data.sub_cases[2]
		forms1 = main_algorithm(data1)
		forms2 = main_algorithm(data2)
		forms = form.join_forms(forms1, forms2)
	elseif data.sub_parts then
		_.log_info("Случай с '+'")
		sub_forms = {}  -- list
		for i, sub_part in pairs(data.sub_parts) do
			table.insert(sub_forms, main_algorithm(sub_part))
		end
		forms = form.plus_forms(sub_forms)
	else
		_.log_info('Стандартный случай без вариаций')
		forms = main_algorithm(data)
	end

	if data.noun then
		noun_form.special_cases(forms, args, data.index, data.word)
	end

	result.finalize(data, forms)

	_.log_table(forms, "forms")
	return forms
end


return export
