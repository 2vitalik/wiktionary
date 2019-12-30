local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'output.forms.noun'


function export.remove_stress_if_one_syllable(value)
	if _.contains_once(value, '{vowel+ё}') then
		return _.replaced(value, '́ ', '')
	end
	return value
end


-- @starts
function export.apply_obelus(i)
	func = "apply_obelus"
	_.starts(module, func)

	if _.contains(i.rest_index, '÷') then
		i.out_args['obelus'] = '1'
	end
	_.ends(module, func)
end


-- @starts
function export.apply_specific_3(i)
	func = "apply_specific_3"
	_.starts(module, func)

	local o = i.out_args

	-- Специфика по (3)
	if _.contains(i.rest_index, '%(3%)') or _.contains(i.rest_index, '③') then
		if _.endswith(o['prp-sg'], 'и') then
			o['prp-sg'] = o['prp-sg'] .. '&nbsp;//<br />' .. _.replaced(o['prp-sg'], 'и$', 'е')
		end
		if i.gender == 'f' and _.endswith(o['dat-sg'], 'и') then
			o['dat-sg'] = o['dat-sg'] .. '&nbsp;//<br />' .. _.replaced(o['dat-sg'], 'и$', 'е')
		end
	end

	_.ends(module, func)
end


--------------------------------------------------------------------------------


-- @starts
local function prt_case(i)  -- Разделительный падеж
	func = "prt_case"
	_.starts(module, func)

	local o = i.out_args

	if _.contains(i.index, 'Р2') or _.contains(i.index, 'Р₂') then
		o['prt-sg'] = o['dat-sg']
	end
	if _.has_value(i.args['Р']) then
		o['prt-sg'] = i.args['Р']
	end

	_.ends(module, func)
end


-- @starts
local function loc_case(i)  -- Местный падеж
	func = "loc_case"
	_.starts(module, func)

	local o = i.out_args

	if _.contains(i.index, 'П2') or _.contains(i.index, 'П₂') then
		local loc = o['dat-sg']
		loc = _.replaced(loc, '́ ', '')
		loc = _.replaced(loc, 'ё', 'е')
		loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
		loc = export.remove_stress_if_one_syllable(loc)
		o['loc-sg'] = loc
		local loc_prep = _.extract(i.index, 'П2%((.+)%)')
		if not loc_prep then
			loc_prep = _.extract(i.index, 'П₂%((.+)%)')
		end
		if not loc_prep then
			loc_prep = 'в, на'
		end
		o['loc-sg'] = '(' .. loc_prep .. ') ' .. o['loc-sg']
		if _.contains(i.index, '%[П') then
			o['loc-sg'] = o['loc-sg'] .. '&nbsp;//<br />' .. o['prp-sg']
		end
	end
	if _.has_value(i.args['М']) then
		o['loc-sg'] = i.args['М']
	end

	_.ends(module, func)
end


-- @starts
local function voc_case(i)  -- Звательный падеж
	func = "voc_case"
	_.starts(module, func)

	local o = i.out_args

	if _.has_value(i.args['З']) then
		o['voc-sg'] = i.args['З']
	elseif _.contains(i.index, 'З') then
		if _.endswith(i.word.unstressed, {'а', 'я'}) then
			o['voc-sg'] = o['gen-pl']
		else
			o['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
		end
	end

	_.ends(module, func)
end


-- @starts
function export.special_cases(i)
	func = "special_cases"
	_.starts(module, func)

	prt_case(i)
	loc_case(i)
	voc_case(i)
	_.ends(module, func)
end


return export
