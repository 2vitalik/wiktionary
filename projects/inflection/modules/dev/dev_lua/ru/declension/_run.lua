local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts')  -- ''  -- '_' /parts
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/result')  -- ''
local form = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/forms/common')  -- ''
local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/forms/noun')  -- ''


local module = 'run'


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
		local o = i.out_args
		genders = {'m', 'n', 'f', ''}  -- plural (without gender) should be last one?
		for j, gender in pairs(genders) do  -- list
			local i_copy = mw.clone(i)
			i_copy.gender = gender
			_.log_value(i_copy.gender, 'info.gender')
			run_gender(i_copy)

			local o_copy = i_copy.out_args

			local cases
			if i_copy.gender ~= '' then
				cases = {
					'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
					'srt-sg',
				}  -- list
			else
				cases = {
					'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
					'srt-pl',
					'comparative', 'comparative2'
				}  -- list
			end

			for c, case in pairs(cases) do  -- list
				if i_copy.gender ~= '' then
					key = case .. '-' .. i_copy.gender
				else
					key = case
				end
				o[key] = o_copy[case]
			end
			if i_copy.gender == 'f' then
				o['ins-sg2-f'] = o_copy['ins-sg2']
			end

			if i_copy.gender == 'm' then
				o['acc-sg-m-a'] = o['gen-sg-m']
				o['acc-sg-m-n'] = o['nom-sg-m']
			elseif i_copy.gender == '' then
				o['acc-pl-a'] = o_copy['gen-pl']
				o['acc-pl-n'] = o_copy['nom-pl']
			end

		end
	end

	_.ends(module, func)
end


-- @starts
function export.run(info)
	func = "run"
	_.starts(module, func)

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
end


return export
