local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/common')  -- 'declension.'
local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/parts')  -- '_' /parts
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/result')  -- 'declension.'
local form = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/forms/common')  -- 'declension.'
local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/forms/noun')  -- 'declension.'


local module = 'declension'


local function prepare_stash()  -- todo rename to `prepare_regexp_templates` or patterns
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


-- @starts
local function run_gender(i)
	func = "run_gender"
	_.starts(module, func)

	local o = i.out_args

	if _.startswith(i.rest_index, '0') then
		-- todo: move to special function
		local keys
		keys = {
			'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
			'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
		}  -- list
		for j, key in pairs(keys) do  -- list
			o[key] = i.word.stressed
		end
		return _.ends(module, func)
	end

	p.generate_parts(i)
	form.generate_out_args(i)

	if i.adj then
		-- todo: move to special function
		if i.gender ~= '' then
			local cases
			cases = {
				'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
				'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
				'srt-sg', 'srt-pl',
			}  -- list

			for c, case in pairs(cases) do  -- list
				key = case .. '-' .. i.gender
				o[key] = o[case]
			end
			if i.gender == 'f' then
				o['ins-sg2-f'] = o['ins-sg2']
			end
		end

		if i.gender == 'm' then
			o['acc-sg-m-a'] = o['gen-sg-m']
			o['acc-sg-m-n'] = o['nom-sg-m']
		elseif i.gender == '' then
			o['acc-pl-a'] = o['gen-pl']
			o['acc-pl-n'] = o['nom-pl']
		end
	end

	_.ends(module, func)
end


-- @starts
local function run_info(i)  -- todo rename to `run_info`
	func = "run_info"
	_.starts(module, func)

	if not i.has_index then
		return
	end

	if i.noun then
		run_gender(i)
	elseif i.adj then
		genders = {'m', 'n', 'f', ''}  -- plural (without gender) should be last one?
		for j, gender in pairs(genders) do  -- list
			-- todo: copy info?
			i.gender = gender
			_.log_value(i.gender, 'info.gender')
			run_gender(i)
		end
	end

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

	info.frame = frame  -- todo: move to `parse`

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	-- todo: move this `if` block inside `run_info` and run it recursively :)
	if info.variations then
		_.log_info("Случай с вариациями '//'")
		local info_1 = info.variations[1]
		local info_2 = info.variations[2]
		-- todo: ... = o.output(m.modify(info_1))
		run_info(info_1)
		run_info(info_2)
		info.out_args = form.join_forms(info_1.out_args, info_2.out_args)
		-- todo: form.join_variations()
		-- todo: check for errors inside variations
	elseif info.plus then
		_.log_info("Случай с '+'")
		local out_args_plus = {}  -- list
		for i, sub_info in pairs(info.plus) do  -- list
			run_info(sub_info)
			table.insert(out_args_plus, sub_info.out_args)
		end
		info.out_args = form.plus_forms(out_args_plus)
		-- todo: form.plus_out_args()
	else
		_.log_info('Стандартный случай без вариаций')
		run_info(info)
	end

	if info.noun then
		noun_forms.special_cases(info)
	end

	r.forward_args(info)

	_.log_table(info.out_args, "info.out_args")
	_.ends(module, func)
	return info.out_args
end


return export


-- todo: rename `i.data` to `i.parts`
