local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/common')  -- 'declension.'
local m = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify')  -- '_' /modify
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
local function main_algorithm(info)
	func = "main_algorithm"
	_.starts(module, func)

	local error, keys, out_args, orig_stem, for_category, old_value, cases

	-- todo: Инициализировать `forms` прямо здесь, чтобы не вызывать потом постоянно finalize...

	-- ... = extract_stress_type(...)
	-- if error then
	--     out_args = result.finalize(info, error)
	--     _.ends(module, func)
	--     return out_args
	-- end

--	INFO: Если ударение не указано:
	if not info.stress_type then

--		INFO: Может быть это просто несклоняемая схема:
		if _.contains(info.rest_index, '^0') then  -- todo: put this somewhere upper? before checking stress? or inside sub-algorithm?
			keys = {
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			}  -- list
			out_args = {}  -- dict
			out_args['зализняк'] = '0'
			out_args['скл'] = 'не'
			for i, key in pairs(keys) do  -- list
				out_args[key] = info.word.stressed
			end
			_.ends(module, func)
			return result.finalize(info, out_args)

--		INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
		elseif _.has_value(info.rest_index) then
			_.ends(module, func)
			return result.finalize(info, {error='Нераспознанная часть индекса: ' .. info.rest_index})  -- b-dict

--		INFO: Если индекса вообще нет, то и формы просто не известны:
		else  -- todo: put this somewhere upper?
			_.ends(module, func)
			return result.finalize(info, {})  -- b-dict
		end
	end

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem.stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(info.stem.stressed, '[́ ё]') then  -- and not info.absent_stress ??
		if _.equals(info.stress_type, {"f", "f'"}) then
			info.stem.stressed = _.replaced(info.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(info.rest_index, '%*') then
			-- pass  -- *** поставим ударение ниже, после чередования
		else
			info.stem.stressed = _.replaced(info.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(info.stem.stressed, 'info.stem.stressed')

	-- -------------------------------------------------------------------------

	-- fixme: Здесь раньше было определение типа основы

	if not info.stem.type then
		_.ends(module, func)
		return result.finalize(info, {error='Неизвестный тип основы'})  -- b-dict
	end

	-- -------------------------------------------------------------------------

	-- todo: `main_algo` will have only further lines?

	if info.noun then
		m.modify(info)
		form.generate_out_args(info)

	elseif info.adj then
		cases = {
			'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
			'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			'srt_sg', 'srt_pl',
		}  -- list

		genders = {'m', 'n', 'f', ''}  -- plural (without gender) should be last one?
		for i, gender in pairs(genders) do  -- list
			-- todo: copy info?
			info.gender = gender
			_.log_value(info.gender, 'info.gender')

			m.modify(info)

			if gender == '' then  -- todo: move all this logic inside `generate_out_args` ?
				form.generate_out_args(info)
			else
				form.generate_out_args(info)
				for i, case in pairs(cases) do  -- list
					key = case .. '_' .. gender
					info.out_args[key] = info.out_args[case]
				end
				if gender == 'f' then
					info.out_args['ins_sg2_f'] = info.out_args['ins_sg2']
				end
			end
		end

		info.out_args['acc_sg_m_a'] = info.out_args['gen_sg_m']
		info.out_args['acc_sg_m_n'] = info.out_args['nom_sg_m']
		info.out_args['acc_pl_a'] = info.out_args['gen_pl']
		info.out_args['acc_pl_n'] = info.out_args['nom_pl']

		info.gender = ''  -- redundant?
	end

	info.out_args['зализняк1'] = index.get_zaliznyak(info.stem.type, info.stress_type, info.rest_index)

	for_category = info.out_args['зализняк1']
	for_category = _.replaced(for_category, '①', '(1)')
	for_category = _.replaced(for_category, '②', '(2)')
	for_category = _.replaced(for_category, '③', '(3)')
	info.out_args['зализняк'] = for_category

	_.ends(module, func)
end


-- @starts
function export.forms(base, args, frame)  -- todo: rename to `out_args`
	func = "forms"
	_.starts(module, func)

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
	if info.variations then
		_.log_info("Случай с вариациями '//'")
		local info_1 = info.variations[1]
		local info_2 = info.variations[2]
		-- todo: ... = o.output(m.modify(info_1))
		main_algorithm(info_1)  -- local
		main_algorithm(info_2)  -- local
		info.out_args = form.join_forms(info_1.out_args, info_2.out_args)
	elseif info.plus then
		_.log_info("Случай с '+'")
		local out_args_plus = {}  -- list
		for i, sub_info in pairs(info.plus) do  -- list
			main_algorithm(sub_info)
			table.insert(out_args_plus, sub_info.out_args)
		end
		info.out_args = form.plus_forms(out_args_plus)
	else
		_.log_info('Стандартный случай без вариаций')
		main_algorithm(info)
	end

	if info.noun then
		noun_forms.special_cases(info.out_args, args, info.index, info.word.unstressed)
	end

	result.finalize(info, info.out_args)
	-- todo: put `forward_args` here instead of `finalize`

	_.log_table(info.out_args, "info.out_args")
	_.ends(module, func)
	return info.out_args
end


return export
