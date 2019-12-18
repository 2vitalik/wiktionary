local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'output.forms.noun'


function export.remove_stress_if_one_syllable(value)
	-- _.call('noun.forms', 'remove_stress_if_one_syllable')

	if _.contains_once(value, '{vowel+ё}') then
		return _.replaced(value, '́ ', '')
	end
	return value
end


-- @starts
function export.apply_obelus(out_args, rest_index)
	func = "apply_obelus"
	_.starts(module, func)

	if _.contains(rest_index, '÷') then
		out_args['obelus'] = '1'
	end

	_.ends(module, func)
end


-- @starts
function export.apply_specific_3(out_args, gender, rest_index)
	func = "apply_specific_3"
	_.starts(module, func)

	-- Специфика по (3)
	if _.contains(rest_index, '%(3%)') or _.contains(rest_index, '③') then
		if _.endswith(out_args['prp_sg'], 'и') then
			out_args['prp_sg'] = out_args['prp_sg'] .. '&nbsp;//<br />' .. _.replaced(out_args['prp_sg'], 'и$', 'е')
		end
		if gender == 'f' and _.endswith(out_args['dat_sg'], 'и') then
			out_args['dat_sg'] = out_args['dat_sg'] .. '&nbsp;//<br />' .. _.replaced(out_args['dat_sg'], 'и$', 'е')
		end
	end

	_.ends(module, func)
end



--------------------------------------------------------------------------------


-- @starts
local function prt_case(out_args, args, index)  -- Разделительный падеж
	func = "prt_case"
	_.starts(module, func)

	if _.contains(index, 'Р2') or _.contains(index, 'Р₂') then
		out_args['prt_sg'] = out_args['dat_sg']
	end
	if _.has_value(args['Р']) then
		out_args['prt_sg'] = args['Р']
	end

	_.ends(module, func)
end


-- @starts
local function loc_case(out_args, args, index)  -- Местный падеж
	func = "loc_case"
	_.starts(module, func)

	local loc, loc_prep

	if _.contains(index, 'П2') or _.contains(index, 'П₂') then
		loc = out_args['dat_sg']
		loc = _.replaced(loc, '́ ', '')
		loc = _.replaced(loc, 'ё', 'е')
		loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
		loc = export.remove_stress_if_one_syllable(loc)
		out_args['loc_sg'] = loc
		loc_prep = '?'
		loc_prep = _.extract(index, 'П2%((.+)%)')
		if not loc_prep then
			loc_prep = _.extract(index, 'П₂%((.+)%)')
		end
		if not loc_prep then
			loc_prep = 'в, на'
		end
		out_args['loc_sg'] = '(' .. loc_prep .. ') ' .. out_args['loc_sg']
		if _.contains(index, '%[П') then
			out_args['loc_sg'] = out_args['loc_sg'] .. '&nbsp;//<br />' .. out_args['prp_sg']
		end
	end
	if _.has_value(args['М']) then
		out_args['loc_sg'] = args['М']
	end

	_.ends(module, func)
end


-- @starts
local function voc_case(out_args, args, index, word)  -- Звательный падеж
	func = "voc_case"
	_.starts(module, func)

	if _.has_value(args['З']) then
		out_args['voc_sg'] = args['З']
	elseif _.contains(index, 'З') then
		if _.endswith(word, {'а', 'я'}) then
			out_args['voc_sg'] = out_args['gen_pl']
		else
			out_args['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
		end
	end

	_.ends(module, func)
end


-- @starts
function export.special_cases(out_args, args, index, word)
	func = "special_cases"
	_.starts(module, func)

	prt_case(out_args, args, index)
	loc_case(out_args, args, index)
	voc_case(out_args, args, index, word)

	_.ends(module, func)
end


return export
