local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local init_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forms/init')  -- '.'
local common_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forms/common')  -- '.'
local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forms/noun')  -- '.'
local adj_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forms/adj')  -- '.'


local module = 'run.result'


-- @starts
function export.generate_result(i)
	func = "generate_result"
	_.starts(module, func)

	local r = i.result

	init_forms.init_forms(i)
	if i.adj then
		init_forms.init_srt_forms(i)
	end
	_.log_table(r, 'i.result')

	common_forms.fix_stress(i)

	if i.adj and i.calc_pl then
		-- `calc_pl` -- чтобы считать их только один раз, а не для каждого рода
		adj_forms.add_comparative(i)
	end

	for key, value in pairs(r) do
		-- replace 'ё' with 'е' when unstressed
		-- if _.contains_once(i.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё') then  -- trying to bug-fix
		if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё') then
			if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt-sg' then
				r[key] = _.replaced(value, 'ё', 'е') .. ' // ' .. _.replaced(value, '́', '')
			else
				r[key] = _.replaced(value, 'ё', 'е')  -- обычный случай
			end
		end
	end

	if i.noun then
		noun_forms.apply_obelus(i)
	end

	common_forms.choose_accusative_forms(i)

	common_forms.second_ins_case(i)

	if i.noun then
		noun_forms.apply_specific_3(i)
	end

	for key, value in pairs(r) do
--		INFO Удаляем ударение, если только один слог:
		r[key] = noun_forms.remove_stress_if_one_syllable(value)
	end

	if i.adj then
		if i.postfix then
			local keys
			keys = {
				'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
				'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
			}  -- list
			for j, key in pairs(keys) do  -- list
				r[key] = r[key] .. 'ся'
			end
		end
	end

	_.ends(module, func)
end


return export
