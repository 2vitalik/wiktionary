local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


function export.template(base, args)
	return dev_prefix .. 'inflection/ru/adj'
end


return export
