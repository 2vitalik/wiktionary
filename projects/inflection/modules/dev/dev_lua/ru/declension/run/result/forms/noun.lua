local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.forms.noun'


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
		i.result['obelus'] = '1'
	end
	_.ends(module, func)
end


-- @starts
function export.apply_specific_3(i)
	func = "apply_specific_3"
	_.starts(module, func)

	local r = i.result

	-- Специфика по (3)
	if _.contains(i.rest_index, '%(3%)') or _.contains(i.rest_index, '③') then
		if _.endswith(r['prp-sg'], 'и') then
			r['prp-sg'] = r['prp-sg'] .. '&nbsp;//<br />' .. _.replaced(r['prp-sg'], 'и$', 'е')
		end
		if i.gender == 'f' and _.endswith(r['dat-sg'], 'и') then
			r['dat-sg'] = r['dat-sg'] .. '&nbsp;//<br />' .. _.replaced(r['dat-sg'], 'и$', 'е')
		end
	end

	_.ends(module, func)
end


--------------------------------------------------------------------------------


-- @starts
local function prt_case(i)  -- Разделительный падеж
	func = "prt_case"
	_.starts(module, func)

	local r = i.result

	if _.contains(i.index, 'Р2') or _.contains(i.index, 'Р₂') then
		r['prt-sg'] = r['dat-sg']
	end
	if _.has_value(i.args['Р']) then
		r['prt-sg'] = i.args['Р']
	end

	_.ends(module, func)
end


-- @starts
local function loc_case(i)  -- Местный падеж
	func = "loc_case"
	_.starts(module, func)

	local r = i.result

	if _.contains(i.index, 'П2') or _.contains(i.index, 'П₂') then
		local loc = r['dat-sg']
		loc = _.replaced(loc, '́ ', '')
		loc = _.replaced(loc, 'ё', 'е')
		loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
		loc = export.remove_stress_if_one_syllable(loc)
		r['loc-sg'] = loc
		local loc_prep = _.extract(i.index, 'П2%((.+)%)')
		if not loc_prep then
			loc_prep = _.extract(i.index, 'П₂%((.+)%)')
		end
		if not loc_prep then
			loc_prep = 'в, на'
		end
		r['loc-sg'] = '(' .. loc_prep .. ') ' .. r['loc-sg']
		if _.contains(i.index, '%[П') then
			r['loc-sg'] = r['loc-sg'] .. '&nbsp;//<br />' .. r['prp-sg']
		end
	end
	if _.has_value(i.args['М']) then
		r['loc-sg'] = i.args['М']
	end

	_.ends(module, func)
end


-- @starts
local function voc_case(i)  -- Звательный падеж
	func = "voc_case"
	_.starts(module, func)

	local r = i.result

	if _.has_value(i.args['З']) then
		r['voc-sg'] = i.args['З']
	elseif _.contains(i.index, 'З') then
		if _.endswith(i.word.unstressed, {'а', 'я'}) then
			r['voc-sg'] = r['gen-pl']
		else
			r['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
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
