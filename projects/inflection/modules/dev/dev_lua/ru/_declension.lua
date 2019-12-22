local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/common')  -- 'declension.'
local m = require('Module:' .. dev_prefix .. 'inflection/ru/declension/declension/_modify')  -- ''
local result = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/result')  -- 'declension.' =
local form = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/forms/common')  -- 'declension.'
local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/forms/noun')  -- 'declension.'
local index = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/index')  -- 'declension.' =

local module = 'declension'


local function prepare_stash()
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


-- @starts
local function main_algorithm(data)
	func = "main_algorithm"
	_.starts(module, func)

	local error, keys, out_args, orig_stem, for_category, old_value, cases

	-- todo: Инициализировать `forms` прямо здесь, чтобы не вызывать потом постоянно finalize...

	-- ... = extract_stress_type(...)
	-- if error then
	--     out_args = result.finalize(data, error)
	--     _.ends(module, func)
	--     return out_args
	-- end

--	INFO: Если ударение не указано:
	if not data.stress_type then

--		INFO: Может быть это просто несклоняемая схема:
		if _.contains(data.rest_index, '^0') then  -- todo: put this somewhere upper? before checking stress? or inside sub-algorithm?
			keys = {
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			}  -- list
			out_args = {}  -- dict
			out_args['зализняк'] = '0'
			out_args['скл'] = 'не'
			for i, key in pairs(keys) do  -- list
				out_args[key] = data.word.stressed
			end
			_.ends(module, func)
			return result.finalize(data, out_args)

--		INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
		elseif _.has_value(data.rest_index) then
			_.ends(module, func)
			return result.finalize(data, {error='Нераспознанная часть индекса: ' .. data.rest_index})  -- b-dict

--		INFO: Если индекса вообще нет, то и формы просто не известны:
		else  -- todo: put this somewhere upper?
			_.ends(module, func)
			return result.finalize(data, {})  -- b-dict
		end
	end

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem.stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(data.stem.stressed, '[́ ё]') then  -- and not data.absent_stress ??
		if _.equals(data.stress_type, {"f", "f'"}) then
			data.stem.stressed = _.replaced(data.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(data.rest_index, '%*') then
			-- pass  -- *** поставим ударение ниже, после чередования
		else
			data.stem.stressed = _.replaced(data.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(data.stem.stressed, 'data.stem.stressed')

	-- -------------------------------------------------------------------------

	-- fixme: Здесь раньше было определение типа основы

	if not data.stem.type then
		_.ends(module, func)
		return result.finalize(data, {error='Неизвестный тип основы'})  -- b-dict
	end

	-- -------------------------------------------------------------------------

	-- todo: `main_algo` will have only further lines?

	if data.noun then
		m.modify(data)
		out_args = form.generate_forms(data)  -- TODO: Rename to `out_args` ?

	elseif data.adj then
		out_args = {}
		cases = {
			'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
			'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			'srt_sg', 'srt_pl',
		}  -- list

		genders = {'', 'm', 'n', 'f'}
		for i, gender in pairs(genders) do  -- list
			-- todo: copy data?
			data.gender = gender
			_.log_value(data.gender, 'data.gender')

			m.modify(data)

			if gender == '' then  -- todo: move all this logic inside `generate_forms` ?
				out_args = form.generate_forms(data)  -- TODO: Rename to `out_args` ?
			else
				sub_forms = form.generate_forms(data)
				for i, case in pairs(cases) do  -- list
					key = case .. '_' .. gender
					out_args[key] = sub_forms[case]  -- todo: rename to `out_args`
				end
				if gender == 'f' then
					out_args['ins_sg2_f'] = sub_forms['ins_sg2']
				end
			end
		end
		out_args['acc_sg_m_a'] = out_args['gen_sg_m']
		out_args['acc_sg_m_n'] = out_args['nom_sg_m']
		out_args['acc_pl_a'] = out_args['gen_pl']
		out_args['acc_pl_n'] = out_args['nom_pl']

		data.gender = ''  -- redundant?
	end

	out_args['зализняк1'] = index.get_zaliznyak(data.stem.type, data.stress_type, data.rest_index)

	for_category = out_args['зализняк1']
	for_category = _.replaced(for_category, '①', '(1)')
	for_category = _.replaced(for_category, '②', '(2)')
	for_category = _.replaced(for_category, '③', '(3)')
	out_args['зализняк'] = for_category

	_.ends(module, func)
	return out_args
end


-- @starts
function export.forms(base, args, frame)  -- todo: rename to `out_args`
	func = "forms"
	_.starts(module, func)

--	INFO: `base` здесь нигде не используется,
	--  но теоретически может понадобиться для других языков

	-- todo: move this to another place?
	mw.log('=================================================================')

	prepare_stash()  -- INFO: Заполняем шаблоны для регулярок

--	INFO: Достаём всю информацию из аргументов (args):
	--   основа, род, одушевлённость и т.п.
	local info, error
	info, error = parse.parse(base, args)
	if error then
		out_args = result.finalize(info, error)
		_.ends(module, func)
		return out_args
	end

	info.frame = frame

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	local out_args = {}  -- dict
	if info.variations then
		_.log_info("Случай с вариациями '//'")
		local info_1 = info.variations[1]
		local info_2 = info.variations[2]
		-- todo: ... = o.output(m.modify(info_1))
		local out_args_1 = main_algorithm(info_1)
		local out_args_2 = main_algorithm(info_2)
		out_args = form.join_forms(out_args_1, out_args_2)
	elseif info.plus then
		_.log_info("Случай с '+'")
		local out_args_plus = {}  -- list
		for i, sub_info in pairs(info.plus) do
			table.insert(out_args_plus, main_algorithm(sub_info))
		end
		out_args = form.plus_forms(out_args_plus)
	else
		_.log_info('Стандартный случай без вариаций')
		out_args = main_algorithm(info)
	end

	if info.noun then
		noun_forms.special_cases(out_args, args, info.index, info.word.unstressed)
	end

	result.finalize(info, out_args)

	_.log_table(out_args, "out_args")
	_.ends(module, func)
	return out_args
end


return export
