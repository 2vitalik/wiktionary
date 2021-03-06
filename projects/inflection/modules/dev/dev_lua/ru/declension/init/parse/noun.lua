local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.parse.noun'


-- @call
local function get_cyrl_animacy(index, gender)
	func = "get_cyrl_animacy"
	_.call(module, func)

	if _.extract(index, '^' .. gender .. 'о//' .. gender) then
		return 'an//in'
	elseif _.extract(index, '^' .. gender .. '//' .. gender .. 'о') then
		return 'in//an'
	elseif _.extract(index, '^' .. gender .. 'о') then
		return 'an'
	else
		return 'in'
	end
end


-- @starts
function export.extract_gender_animacy(i)
	func = "extract_gender_animacy"
	_.starts(module, func)

	local convert_animacy, orig_index, rest_index

	-- мо-жо - mf a
	-- ж//жо - f ina//a
	-- мо - m a
	-- с  - n ina
	i.pt = false

	if _.startswith(i.index, 'п') then
		i.adj = true
	elseif _.extract(i.index, '^м//ж') or _.extract(i.index, '^m//f') then  -- todo: INFO: похоже все такие случаи либо 0, либо <...>
		i.gender = 'mf'
		i.animacy = 'in'
	elseif _.extract(i.index, '^м//с') or _.extract(i.index, '^m//n') then
		i.gender = 'mn'
		i.animacy = 'in'
	elseif _.extract(i.index, '^ж//м') or _.extract(i.index, '^f//m') then
		i.gender = 'fm'
		i.animacy = 'in'
	elseif _.extract(i.index, '^ж//с') or _.extract(i.index, '^f//n') then
		i.gender = 'fn'
		i.animacy = 'in'
	elseif _.extract(i.index, '^с//м') or _.extract(i.index, '^n//m') then
		i.gender = 'nm'
		i.animacy = 'in'
	elseif _.extract(i.index, '^с//ж') or _.extract(i.index, '^n//m') then
		i.gender = 'nm'
		i.animacy = 'in'
	elseif _.extract(i.index, '^мо%-жо') or _.extract(i.index, '^mf a') then
		i.gender = 'f'
		i.animacy = 'an'
		i.common_gender = true
	elseif _.extract(i.index, '^мн') then
		i.gender = ''
		i.animacy = ''
		i.common_gender = false
		i.pt = true
		if _.extract(i.index, 'одуш') then
			i.animacy = 'an'
		elseif _.extract(i.index, 'неод') then
			i.animacy = 'in'
		end
		-- TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
		i.rest_index = i.index
	elseif _.extract(i.index, '^мс') then
		i.pronoun = true
	elseif _.extract(i.index, '^м') then  -- fixme: сюда частично попадает необрабатываемый пока "м//мн."
		i.gender = 'm'
		i.animacy = get_cyrl_animacy(i.index, 'м')
		i.common_gender = false
	elseif _.extract(i.index, '^ж') then
		i.gender = 'f'
		i.animacy = get_cyrl_animacy(i.index, 'ж')
		i.common_gender = false
	elseif _.extract(i.index, '^с') then
		i.gender = 'n'
		i.animacy = get_cyrl_animacy(i.index, 'с')
		i.common_gender = false
	else
		i.gender = _.extract(i.index, '^([mnf])')
		i.animacy = _.extract(i.index, '^[mnf] ([a-z/]+)')
		i.common_gender = false
		if i.animacy then
			convert_animacy = {}
			convert_animacy['in'] = 'in'
			convert_animacy['an'] = 'an'
			convert_animacy['ina'] = 'in'
			convert_animacy['a'] = 'an'
			convert_animacy['a//ina'] = 'an//in'
			convert_animacy['ina//a'] = 'in//an'
			convert_animacy['anin'] = 'an//in'
			convert_animacy['inan'] = 'in//an'
			i.animacy = convert_animacy[i.animacy]
		end
	end

	-- Удаляем теперь соответствующий кусок индекса
	if (i.gender or i.gender == '') and i.animacy and not i.adj and not i.pronoun then
		_.log_value(i.index, 'i.index')
		orig_index = mw.text.trim(i.index)

--		local test1 = _.replaced(i.index, '^mf a ?', '')
--		mw.log('test1 = ' .. mw.text.trim(test1))
--
--		local test2 = _.replaced(i.index, '^mf a ', '')
--		mw.log('test2 = ' .. mw.text.trim(test2))
--
--		local test3 = _.replaced(i.index, 'mf a ', '')
--		mw.log('test3 = ' .. mw.text.trim(test3))
--
--		local test4 = _.replaced(i.index, 'mf a', '')
--		mw.log('test4 = ' .. mw.text.trim(test4))
--
--		local test5 = mw.text.trim(_.replaced(i.index, '^mf a ?', ''))
--		mw.log('test5 = ' .. test5)
--
--		local test6 = _.replaced(i.index, '^mf a ?', '')
--		mw.log('test6 = ' .. test6)
--		local test7 = mw.text.trim(test6)
--		mw.log('test7 = ' .. test7)

		-- TODO: Simplify things a bit here (сделать циклом!):

		rest_index = _.replaced(i.index, '^mf a ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "mf a" из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(i.index, '^[mnf]+ [a-z/]+ ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "[mnf] [in/an]" из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(i.index, '^мн%.? неод%.? ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "мн. неод." из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(i.index, '^мн%.? одуш%.? ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "мн. одуш." из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(i.index, '^мн%.? ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "мн." из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(i.index, '^[-мжсо/]+%,? ?', '')   -- fixme: сюда частично попадает необрабатываемый пока "м//мн."
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "м/ж/с/мо/жо/со/..." из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
		e.add_error(i, 'TODO: process such errors')
		return _.ends(module, func)
	elseif i.adj then
		_.log_value(i.index, 'i.index (п)')
		orig_index = mw.text.trim(i.index)

		rest_index = _.replaced(i.index, '^п ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "п" из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
	elseif i.pronoun then
		_.log_value(i.index, 'i.index (мс)')
		orig_index = mw.text.trim(i.index)

		rest_index = _.replaced(i.index, '^мс ?', '')
		if rest_index ~= orig_index then
			i.rest_index = mw.text.trim(rest_index)
			_.log_info('Удаление "мс" из индекса')
			_.log_value(i.rest_index, 'i.rest_index')
			return _.ends(module, func)
		end
	end

	_.ends(module, func)
end


return export
