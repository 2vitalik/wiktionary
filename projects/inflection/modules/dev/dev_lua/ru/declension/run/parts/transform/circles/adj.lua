local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


module = 'run.parts.transform.circles.adj'


-- @starts
function export.apply_adj_specific_1_2(stems, gender, rest_index)
	func = "apply_adj_specific_1_2"
	_.starts(module, func)

	if not _.endswith(stems['srt-sg'], 'нн') then
		-- todo: log some error?
		return _.ends(module, func)
	end
	if _.contains(rest_index, {'%(1%)', '①'}) then
		if gender == 'm' then
			_.replace(stems, 'srt-sg', 'нн$', 'н')
		end
	end
	if _.contains(rest_index, {'%(2%)', '②'}) then
		_.replace(stems, 'srt-sg', 'нн$', 'н')
		_.replace(stems, 'srt-pl', 'нн$', 'н')
	end

	_.ends(module, func)
end


return export