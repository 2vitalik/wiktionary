local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local p = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts')  -- ''  -- '_' /parts
local res = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result')  -- ''  -- '_' /result
local forward = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forward')  -- ''
local v = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/variations')  -- ''
local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forms/noun')  -- ''


local module = 'run'


-- @starts
local function run_gender(i)
	func = "run_gender"
	_.starts(module, func)

	local r = i.result

	if _.startswith(i.rest_index, '0') then
		-- todo: move to special function
		local keys
		keys = {
			'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
			'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
		}  -- list
		for j, key in pairs(keys) do  -- list
			r[key] = i.word.stressed
		end
		return _.ends(module, func)
	end

	p.generate_parts(i)
	res.generate_result(i)

	_.ends(module, func)
end


-- @starts
local function run_info(i)
	func = "run_info"
	_.starts(module, func)

	if not i.has_index then
		return
	end

	if i.noun then
		run_gender(i)
	elseif i.adj then
		local r = i.result
		genders = {'m', 'n', 'f', ''}  -- plural (without gender) should be last one?
		for j, gender in pairs(genders) do  -- list
			local i_copy = mw.clone(i)
			i_copy.gender = gender
			_.log_value(i_copy.gender, 'i.gender')
			run_gender(i_copy)

			local r_copy = i_copy.result

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
				r[key] = r_copy[case]
			end
			if i_copy.gender == 'f' then
				r['ins-sg2-f'] = r_copy['ins-sg2']
			end

			if i_copy.gender == 'm' then
				r['acc-sg-m-a'] = r['gen-sg-m']
				r['acc-sg-m-n'] = r['nom-sg-m']
			elseif i_copy.gender == '' then
				r['acc-pl-a'] = r_copy['gen-pl']
				r['acc-pl-n'] = r_copy['nom-pl']
			end

		end
	end

	_.ends(module, func)
end


-- @starts
function export.run(i)
	func = "run"
	_.starts(module, func)

	-- todo: move this `if` block inside `run_info` and run it recursively? :)
	if i.variations then
		_.log_info("Случай с вариациями '//'")
		local i1 = i.variations[1]
		local i2 = i.variations[2]
		run_info(i1)
		run_info(i2)
		i.result = v.join_forms(i1.result, i2.result)
		-- todo: form.join_variations()
		-- todo: check for errors inside variations
	elseif i.plus then
		_.log_info("Случай с '+'")
		local plus = {}  -- list
		for j, sub_info in pairs(i.plus) do  -- list
			run_info(sub_info)
			table.insert(plus, sub_info.result)
		end
		i.result = v.plus_forms(plus)
		-- todo: form.plus_out_args()
	else
		_.log_info('Стандартный случай без вариаций')
		run_info(i)
	end

	if i.noun then
		noun_forms.special_cases(i)  -- todo: move to `run/result/generate_result`
	end

	forward.forward_args(i)

	_.log_table(i.result, "i.result")
	_.ends(module, func)
end


return export
