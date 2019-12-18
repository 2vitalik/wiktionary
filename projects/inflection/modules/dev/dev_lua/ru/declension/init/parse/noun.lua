local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


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
function export.extract_gender_animacy(info)
	func = "extract_gender_animacy"
	_.starts(module, func)

	local convert_animacy, orig_index, rest_index

	-- мо-жо - mf a
	-- ж//жо - f ina//a
	-- мо - m a
	-- с  - n ina
	info.pt = false

	if _.startswith(info.index, 'п') then
		info.adj = true
	elseif _.extract(info.index, '^м//ж') or _.extract(info.index, '^m//f') then
		info.gender = 'mf'
		info.animacy = 'in'
	elseif _.extract(info.index, '^м//с') or _.extract(info.index, '^m//n') then
		info.gender = 'mn'
		info.animacy = 'in'
	elseif _.extract(info.index, '^ж//м') or _.extract(info.index, '^f//m') then
		info.gender = 'fm'
		info.animacy = 'in'
	elseif _.extract(info.index, '^ж//с') or _.extract(info.index, '^f//n') then
		info.gender = 'fn'
		info.animacy = 'in'
	elseif _.extract(info.index, '^с//м') or _.extract(info.index, '^n//m') then
		info.gender = 'nm'
		info.animacy = 'in'
	elseif _.extract(info.index, '^с//ж') or _.extract(info.index, '^n//m') then
		info.gender = 'nm'
		info.animacy = 'in'
	elseif _.extract(info.index, '^мо%-жо') or _.extract(info.index, '^mf a') then
		info.gender = 'f'
		info.animacy = 'an'
		info.common_gender = true
	elseif _.extract(info.index, '^мн') then
		info.gender = ''
		info.animacy = ''
		info.common_gender = false
		info.pt = true
		if _.extract(info.index, 'одуш') then
			info.animacy = 'an'
		elseif _.extract(info.index, 'неод') then
			info.animacy = 'in'
		end
		-- TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
		info.rest_index = info.index
	elseif _.extract(info.index, '^мс') then
		info.pronoun = true
	elseif _.extract(info.index, '^м') then
		info.gender = 'm'
		info.animacy = get_cyrl_animacy(info.index, 'м')
		info.common_gender = false
	elseif _.extract(info.index, '^ж') then
		info.gender = 'f'
		info.animacy = get_cyrl_animacy(info.index, 'ж')
		info.common_gender = false
	elseif _.extract(info.index, '^с') then
		info.gender = 'n'
		info.animacy = get_cyrl_animacy(info.index, 'с')
		info.common_gender = false
	else
		info.gender = _.extract(info.index, '^([mnf])')
		info.animacy = _.extract(info.index, '^[mnf] ([a-z/]+)')
		info.common_gender = false
		if info.animacy then
			convert_animacy = {}
			convert_animacy['in'] = 'in'
			convert_animacy['an'] = 'an'
			convert_animacy['ina'] = 'in'
			convert_animacy['a'] = 'an'
			convert_animacy['a//ina'] = 'an//in'
			convert_animacy['ina//a'] = 'in//an'
			convert_animacy['anin'] = 'an//in'
			convert_animacy['inan'] = 'in//an'
			info.animacy = convert_animacy[info.animacy]
		end
	end

	-- Удаляем теперь соответствующий кусок индекса
	if (info.gender or info.gender == '') and info.animacy and not info.adj and not info.pronoun then
		_.log_value(info.index, 'info.index')
		orig_index = mw.text.trim(info.index)

--		local test1 = _.replaced(info.index, '^mf a ?', '')
--		mw.log('test1 = ' .. mw.text.trim(test1))
--
--		local test2 = _.replaced(info.index, '^mf a ', '')
--		mw.log('test2 = ' .. mw.text.trim(test2))
--
--		local test3 = _.replaced(info.index, 'mf a ', '')
--		mw.log('test3 = ' .. mw.text.trim(test3))
--
--		local test4 = _.replaced(info.index, 'mf a', '')
--		mw.log('test4 = ' .. mw.text.trim(test4))
--
--		local test5 = mw.text.trim(_.replaced(info.index, '^mf a ?', ''))
--		mw.log('test5 = ' .. test5)
--
--		local test6 = _.replaced(info.index, '^mf a ?', '')
--		mw.log('test6 = ' .. test6)
--		local test7 = mw.text.trim(test6)
--		mw.log('test7 = ' .. test7)

		-- TODO: Simplify things a bit here (сделать циклом!):

		rest_index = _.replaced(info.index, '^mf a ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "mf a" из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(info.index, '^[mnf]+ [a-z/]+ ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "[mnf] [in/an]" из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(info.index, '^мн%.? неод%.? ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн. неод." из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(info.index, '^мн%.? одуш%.? ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн. одуш." из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(info.index, '^мн%.? ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн." из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		rest_index = _.replaced(info.index, '^[-мжсо/]+%,? ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "м/ж/с/мо/жо/со/..." из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
		return {error = 'TODO'}  -- dict -- TODO: process such errors
	elseif info.adj then
		_.log_value(info.index, 'info.index (п)')
		orig_index = mw.text.trim(info.index)

		rest_index = _.replaced(info.index, '^п ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "п" из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
	elseif info.pronoun then
		_.log_value(info.index, 'info.index (мс)')
		orig_index = mw.text.trim(info.index)

		rest_index = _.replaced(info.index, '^мс ?', '')
		if rest_index ~= orig_index then
			info.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мс" из индекса')
			_.log_value(info.rest_index, 'info.rest_index')
			return _.ends(module, func)
		end
	end

	_.ends(module, func)
end


return export
