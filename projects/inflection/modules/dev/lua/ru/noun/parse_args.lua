local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local function get_cyrl_animacy(index, gender)
	_.log_func('parse_args', 'get_cyrl_animacy')

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


function export.extract_gender_animacy(data)
	_.log_func('parse_args', 'extract_gender_animacy')

	local convert_animacy, orig_index, rest_index

	-- мо-жо - mf a
	-- ж//жо - f ina//a
	-- мо - m a
	-- с  - n ina
	data.pt = false

	if _.startswith(data.index, 'п') then
		data.adj = true
	elseif _.extract(data.index, '^м//ж') or _.extract(data.index, '^m//f') then
		data.gender = 'mf'
		data.animacy = 'in'
	elseif _.extract(data.index, '^м//с') or _.extract(data.index, '^m//n') then
		data.gender = 'mn'
		data.animacy = 'in'
	elseif _.extract(data.index, '^ж//м') or _.extract(data.index, '^f//m') then
		data.gender = 'fm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^ж//с') or _.extract(data.index, '^f//n') then
		data.gender = 'fn'
		data.animacy = 'in'
	elseif _.extract(data.index, '^с//м') or _.extract(data.index, '^n//m') then
		data.gender = 'nm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^с//ж') or _.extract(data.index, '^n//m') then
		data.gender = 'nm'
		data.animacy = 'in'
	elseif _.extract(data.index, '^мо%-жо') or _.extract(data.index, '^mf a') then
		data.gender = 'f'
		data.animacy = 'an'
		data.common_gender = true
	elseif _.extract(data.index, '^мн') then
		data.gender = ''
		data.animacy = ''
		data.common_gender = false
		data.pt = true
		if _.extract(data.index, 'одуш') then
			data.animacy = 'an'
		elseif _.extract(data.index, 'неод') then
			data.animacy = 'in'
		end
		-- TODO: Также удалить это ниже для rest_index, аналогично как удаляется м, мо и т.п.
		data.rest_index = data.index
	elseif _.extract(data.index, '^мс') then
		data.pronoun = true
	elseif _.extract(data.index, '^м') then
		data.gender = 'm'
		data.animacy = get_cyrl_animacy(data.index, 'м')
		data.common_gender = false
	elseif _.extract(data.index, '^ж') then
		data.gender = 'f'
		data.animacy = get_cyrl_animacy(data.index, 'ж')
		data.common_gender = false
	elseif _.extract(data.index, '^с') then
		data.gender = 'n'
		data.animacy = get_cyrl_animacy(data.index, 'с')
		data.common_gender = false
	else
		data.gender = _.extract(data.index, '^([mnf])')
		data.animacy = _.extract(data.index, '^[mnf] ([a-z/]+)')
		data.common_gender = false
		if data.animacy then
			convert_animacy = {}
			convert_animacy['in'] = 'in'
			convert_animacy['an'] = 'an'
			convert_animacy['ina'] = 'in'
			convert_animacy['a'] = 'an'
			convert_animacy['a//ina'] = 'an//in'
			convert_animacy['ina//a'] = 'in//an'
			convert_animacy['anin'] = 'an//in'
			convert_animacy['inan'] = 'in//an'
			data.animacy = convert_animacy[data.animacy]
		end
	end

	-- Удаляем теперь соответствующий кусок индекса
	if (data.gender or data.gender == '') and data.animacy and not data.adj and not data.pronoun then
		_.log_value(data.index, 'data.index')
		orig_index = mw.text.trim(data.index)

--		local test1 = _.replaced(data.index, '^mf a ?', '')
--		mw.log('test1 = ' .. mw.text.trim(test1))
--
--		local test2 = _.replaced(data.index, '^mf a ', '')
--		mw.log('test2 = ' .. mw.text.trim(test2))
--
--		local test3 = _.replaced(data.index, 'mf a ', '')
--		mw.log('test3 = ' .. mw.text.trim(test3))
--
--		local test4 = _.replaced(data.index, 'mf a', '')
--		mw.log('test4 = ' .. mw.text.trim(test4))
--
--		local test5 = mw.text.trim(_.replaced(data.index, '^mf a ?', ''))
--		mw.log('test5 = ' .. test5)
--
--		local test6 = _.replaced(data.index, '^mf a ?', '')
--		mw.log('test6 = ' .. test6)
--		local test7 = mw.text.trim(test6)
--		mw.log('test7 = ' .. test7)

		-- TODO: Simplify things a bit here (сделать циклом!):

		rest_index = _.replaced(data.index, '^mf a ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "mf a" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^[mnf]+ [a-z/]+ ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "[mnf] [in/an]" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^мн%.? неод%.? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн. неод." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^мн%.? одуш%.? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн. одуш." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^мн%.? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мн." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		rest_index = _.replaced(data.index, '^[-мжсо/]+%,? ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "м/ж/с/мо/жо/со/..." из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
		return {error = 'TODO'}  -- dict -- TODO: process such errors
	elseif data.adj then
		_.log_value(data.index, 'data.index (п)')
		orig_index = mw.text.trim(data.index)

		rest_index = _.replaced(data.index, '^п ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "п" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
	elseif data.pronoun then
		_.log_value(data.index, 'data.index (мс)')
		orig_index = mw.text.trim(data.index)

		rest_index = _.replaced(data.index, '^мс ?', '')
		if rest_index ~= orig_index then
			data.rest_index = mw.text.trim(rest_index)
			mw.log('  -- Удаление "мс" из индекса')
			_.log_value(data.rest_index, 'data.rest_index')
			return
		end
	end
end


function export.angle_brackets(data)
	_.log_func('parse_args', 'angle_brackets')

	local another_index, pt, error

	another_index = _.extract(data.rest_index, '%<([^>]+)%>')
	if another_index then
		pt = data.pt
		if not pt then
			data.output_gender = data.gender
			data.output_animacy = data.animacy
		end
		data.orig_index = data.index
		data.index = another_index
		error = extract_gender_animacy(data)
		data.pt = pt
		if error then return error end

		_.log_value(data.adj, 'data.adj')
		if data.adj then  -- Для прилагательных надо по-особенному?
			return data, {error = 'TODO'}  -- dict
		end
	end
end


return export
