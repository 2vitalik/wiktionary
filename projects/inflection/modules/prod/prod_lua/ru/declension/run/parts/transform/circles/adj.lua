local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


module = 'run.parts.transform.circles.adj'


-- @starts
function export.apply_adj_specific_1_2(i)
	func = "apply_adj_specific_1_2"
	_.starts(module, func)

	local p = i.parts

	if i.calc_sg then
		if not _.endswith(p.stems['srt-sg'], 'нн') then
			-- todo: log some error?
			return _.ends(module, func)
		end
		if _.contains(i.rest_index, {'%(1%)', '①'}) then
			if i.gender == 'm' then
				_.replace(p.stems, 'srt-sg', 'нн$', 'н')
			end
		end
	end

	if _.contains(i.rest_index, {'%(2%)', '②'}) then
		if i.calc_sg then
			_.replace(p.stems, 'srt-sg', 'нн$', 'н')
		end
		if i.calc_pl then
			_.replace(p.stems, 'srt-pl', 'нн$', 'н')
		end
	end

	_.ends(module, func)
end


return export
