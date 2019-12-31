local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.error'


function export.has_error(i)
	return i.result.error ~= ''
end


-- @call
function export.add_error(i, error)
	func = "add_error"
	_.call(module, func)

	local r = i.result

	if r.error then
		r.error = r.error .. '<br/>'
	end
	r.error = r.error .. error
end


return export
