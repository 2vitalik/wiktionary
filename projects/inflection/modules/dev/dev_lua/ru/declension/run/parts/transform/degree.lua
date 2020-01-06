local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local reducable = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/reducable')  -- '...'


local module = 'run.parts.transform.degree'


-- @starts
function export.apply_specific_degree(i)
	func = "apply_specific_degree"
	_.starts(module, func)

	-- If degree sign °
	local p = i.parts
	local word = i.word.unstressed

	if _.contains(i.rest_index, '°') and _.endswith(word, '[ая]нин') then
		_.replace(p.stems, 'all-pl', '([ая])ни́ н$', '%1́ н')
		_.replace(p.stems, 'all-pl', '([ая]́ ?н)ин$', '%1')
		p.endings['nom-pl'] = 'е'
		p.endings['gen-pl'] = ''
		return _.returns(module, func, i.rest_index)
	end

	if _.contains(i.rest_index, '°') and _.endswith(word, 'ин') then
		_.replace(p.stems, 'all-pl', 'и́ ?н$', '')
		if not _.contains(i.rest_index, {'%(1%)', '①'}) then
			p.endings['nom-pl'] = 'е'
		end
		p.endings['gen-pl'] = ''
	end

	if _.contains(i.rest_index, '°') and _.endswith(word, {'ёнок', 'онок'}) then
		_.replace(p.stems, 'all-pl', 'ёнок$', 'я́т')
		_.replace(p.stems, 'all-pl', 'о́нок$', 'а́т')

--		INFO: Эмуляция среднего рода `1a` для форм мн. числа
		p.endings['nom-pl'] = 'а'
		p.endings['gen-pl'] = ''

		reducable.apply_specific_reducable(i, i.gender, i.rest_index .. '*', true)
		return _.returns(module, func, i.rest_index)
	end

	if _.contains(i.rest_index, '°') and _.endswith(word, {'ёночек', 'оночек'}) then

		_.replace(p.stems, 'all-pl', 'ёночек$', 'я́тк')
		_.replace(p.stems, 'all-pl', 'о́ночек$', 'а́тк')

--		INFO: Черездование для единичной формы (возможно применится также и для множественной, но это не страшно, потом заменится по идее)
		reducable.apply_specific_reducable(i, i.gender, i.rest_index .. '*', false)

--		INFO: По сути должно примениться только к мн. формам (случай `B`)
		reducable.apply_specific_reducable(i, 'f', i.rest_index .. '*', false)

		p.endings['gen-pl'] = ''  -- INFO: Странный фикс, но он нужен.. <_<

		return _.returns(module, func, i.rest_index)
	end

	if _.contains(i.rest_index, '°') and i.gender == 'n' and _.endswith(word, 'мя') then
		_.replace(p.stems, 'all-sg', 'м$', 'мен')
		_.replace(p.stems, 'ins-sg', 'м$', 'мен')
		_.replace(p.stems, 'all-pl', 'м$', 'мен')

		p.endings['nom-sg'] = 'я'
		p.endings['gen-sg'] = 'и'
		p.endings['dat-sg'] = 'и'
		p.endings['ins-sg'] = 'ем'
		p.endings['prp-sg'] = 'и'
	end

	return _.returns(module, func, i.rest_index)
end


return export
