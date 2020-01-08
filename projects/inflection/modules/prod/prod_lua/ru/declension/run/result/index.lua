local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.index'


-- Получение индекса Зализняка
-- @starts
function export.get_zaliznyak(i)
	func = "get_zaliznyak"
	_.starts(module, func)

	-- TODO: process <...> cases properly
	--  also e.g. "2*a .. <п 1a>"
	local r = i.result

	if not i.has_index then
		r['зализняк1'] = '??'
		return _.ends(module, func)
	end

	local stem_types
	stem_types = {
		['1-hard'] = '1',
		['2-soft'] = '2',
		['3-velar'] = '3',
		['4-sibilant'] = '4',
		['5-letter-ц'] = '5',
		['6-vowel'] = '6',
		['7-letter-и'] = '7',
		['8-third'] = '8',
	}
	local index = '?'
	if _.contains(i.rest_index, '0') then
		index = '0'
	else
		-- index = i.stem.type[1]  -- TODO
		index = stem_types[i.stem.type]
	end
	if _.contains(i.rest_index, '°') then
		index = index .. '°'
	elseif _.contains(i.rest_index, '%*') then
		index = index .. '*'
	end
	index = index .. _.replaced(i.stress_type, "'", "&#39;")
	if _.contains(i.rest_index, {'⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)'}) then
		index = index .. '⊠'
	elseif _.contains(i.rest_index, {'✕', '×', 'x', 'х', 'X', 'Х'}) then
		index = index .. '✕'
	end
	if _.contains(i.rest_index, {'%(1%)', '①'}) then
		index = index .. '①'
	end
	if _.contains(i.rest_index, {'%(2%)', '②'}) then
		index = index .. '②'
	end
	if _.contains(i.rest_index, {'%(3%)', '③'}) then
		index = index .. '③'
	end
	if _.contains(i.rest_index, '÷') then
		index = index .. '÷'
	end
	if _.contains(i.rest_index, {'%-', '—', '−'}) then
		index = index .. '−'
	end
	if _.contains(i.rest_index, 'ё') then
		index = index .. ', ё'
	end

	r['зализняк1'] = index
	value = r['зализняк1']  local  -- for category
	value = _.replaced(value, '①', '(1)')
	value = _.replaced(value, '②', '(2)')
	value = _.replaced(value, '③', '(3)')
	r['зализняк'] = value

	_.ends(module, func)
end


return export
