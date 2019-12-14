local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'declension.index'


-- Получение индекса Зализняка
-- @starts
function export.get_zaliznyak(stem_type, stress_type, rest_index)
	func = "get_zaliznyak"
	_.starts(module, func)

	local stem_types, index

	-- TODO: process <...> cases properly

	stem_types = {
		['hard'] = '1',
		['soft'] = '2',
		['velar'] = '3',
		['sibilant'] = '4',
		['letter-ц'] = '5',
		['vowel'] = '6',
		['letter-и'] = '7',
		['m-3rd'] = '8',
		['f-3rd'] = '8',
		['f-3rd-sibilant'] = '8',
		['n-3rd'] = '8',
	}
	index = stem_types[stem_type]
	if _.contains(rest_index, '°') then
		index = index .. '°'
	elseif _.contains(rest_index, '%*') then
		index = index .. '*'
	end
	index = index .. _.replaced(stress_type, "'", "&#39;")
	if _.contains(rest_index, {'⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)'}) then
		index = index .. '⊠'
	elseif _.contains(rest_index, {'×', 'x', 'х', 'X', 'Х'}) then
		index = index .. '×'
	end
	if _.contains(rest_index, {'%(1%)', '①'}) then
		index = index .. '①'
	end
	if _.contains(rest_index, {'%(2%)', '②'}) then
		index = index .. '②'
	end
	if _.contains(rest_index, {'%(3%)', '③'}) then
		index = index .. '③'
	end
	if _.contains(rest_index, '÷') then
		index = index .. '÷'
	end
	if _.contains(rest_index, {'%-', '—', '−'}) then
		index = index .. '−'
	end
	if _.contains(rest_index, 'ё') then
		index = index .. ', ё'
	end

	_.ends(module, func)
	return index
end


return export
