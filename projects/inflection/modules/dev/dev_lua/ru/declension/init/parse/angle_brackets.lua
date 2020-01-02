local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local init_stem = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/init_stem')  -- '..'
local noun_parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/noun')  -- '..'
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.parse.angle_brackets'


-- @starts
function export.angle_brackets(i)
	func = "angle_brackets"
	_.starts(module, func)

	local angle_index = _.extract(i.rest_index, '%<([^>]+)%>')
	if angle_index then
		if not i.pt then
			i.output_gender = i.gender
			i.output_animacy = i.animacy
		end

		i.orig_index = i.index
		i.index = angle_index

		local pt_backup = i.pt
		noun_parse.extract_gender_animacy(i)
		i.pt = pt_backup

		if e.has_error(i) then
			return _.ends(module, func)
		end

		_.log_value(i.adj, 'i.adj')
		if i.adj then  -- fixme: Для прилагательных надо по-особенному?
			init_stem.init_stem(i)
			if e.has_error(i) then
				return _.ends(module, func)
			end
		end
	end

	_.ends(module, func)
end


return export
