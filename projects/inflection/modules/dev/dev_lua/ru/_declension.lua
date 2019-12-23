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
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/result')  -- 'declension.'

local module = 'declension'


local function prepare_stash()  -- todo rename to `prepare_regexp_templates` or patterns
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


-- @starts
local function main_algorithm(i)
	func = "main_algorithm"
	_.starts(module, func)

	local o = i.out_args

--	INFO: Если ударение не указано:
	if not i.stress_type then

--		INFO: Может быть это просто несклоняемая схема:
		if _.contains(i.rest_index, '^0') then  -- todo: put this somewhere upper? before checking stress? or inside sub-algorithm?
			local keys
			keys = {
				'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
				'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
			}  -- list
			o['зализняк'] = '0'
			o['скл'] = 'не'
			for j, key in pairs(keys) do  -- list
				o[key] = i.word.stressed
			end
			return _.ends(module, func)

--		INFO: Если это не несклоняемая схема, но есть какой-то индекс -- это ОШИБКА:
		elseif _.has_value(i.rest_index) then
			r.add_error(i, 'Нераспознанная часть индекса: ' .. i.rest_index)
			return _.ends(module, func)

--		INFO: Если индекса вообще нет, то и формы просто не известны:
		else  -- todo: put this somewhere upper?
			return _.ends(module, func)
		end
	end

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem.stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(i.stem.stressed, '[́ ё]') then  -- and not info.absent_stress ??
		if _.equals(i.stress_type, {"f", "f'"}) then
			i.stem.stressed = _.replaced(i.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(i.rest_index, '%*') then
			-- pass  -- *** поставим ударение ниже, после чередования
		else
			i.stem.stressed = _.replaced(i.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(i.stem.stressed, 'info.stem.stressed')

	-- -------------------------------------------------------------------------

	-- fixme: Здесь раньше было определение типа основы

	if not i.stem.type then
		r.add_error(i, 'Неизвестный тип основы')
		return _.ends(module, func)
	end

	-- -------------------------------------------------------------------------

	-- todo: `main_algo` will have only further lines?

	if i.noun then
		m.modify(i)
		form.generate_out_args(i)

	elseif i.adj then
		local cases
		cases = {
			'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
			'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
			'srt-sg', 'srt-pl',
		}  -- list

		genders = {'m', 'n', 'f', ''}  -- plural (without gender) should be last one?
		for j, gender in pairs(genders) do  -- list
			-- todo: copy info?
			i.gender = gender
			_.log_value(i.gender, 'info.gender')

			m.modify(i)

			if gender == '' then  -- todo: move all this logic inside `generate_out_args` ?
				form.generate_out_args(i)
			else
				form.generate_out_args(i)
				for c, case in pairs(cases) do  -- list
					key = case .. '-' .. gender
					o[key] = o[case]
				end
				if gender == 'f' then
					o['ins-sg2-f'] = o['ins-sg2']
				end
			end
		end

		o['acc-sg-m-a'] = o['gen-sg-m']
		o['acc-sg-m-n'] = o['nom-sg-m']
		o['acc-pl-a'] = o['gen-pl']
		o['acc-pl-n'] = o['nom-pl']

		i.gender = ''  -- redundant?
	end

	o['зализняк1'] = index.get_zaliznyak(i)

	value = o['зализняк1']  local  -- for category
	value = _.replaced(value, '①', '(1)')
	value = _.replaced(value, '②', '(2)')
	value = _.replaced(value, '③', '(3)')
	o['зализняк'] = value

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
	local info = parse.parse(base, args)
	if r.has_error(info) then
		_.ends(module, func)
		return info.out_args
	end

	info.frame = frame

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	if info.variations then
		_.log_info("Случай с вариациями '//'")
		local info_1 = info.variations[1]
		local info_2 = info.variations[2]
		-- todo: ... = o.output(m.modify(info_1))
		main_algorithm(info_1)
		main_algorithm(info_2)
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
		noun_forms.special_cases(info)
	end

	result.forward_args(info)

	_.log_table(info.out_args, "info.out_args")
	_.ends(module, func)
	return info.out_args
end


return export
