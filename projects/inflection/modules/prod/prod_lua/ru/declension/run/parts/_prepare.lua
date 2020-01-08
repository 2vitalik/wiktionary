local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/prepare/endings')  -- '..'
local stress_apply = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/prepare/stress_apply')  -- '..'


local module = 'run.parts.prepare'


-- @starts
function export.prepare(i)
	func = "prepare"
	_.starts(module, func)

--	INFO: Generates `.endings` and `.stems`

	-- todo: logging information
	endings.get_endings(i)

	-- todo: logging information
	i.parts.stems = {}  -- dict
	stress_apply.apply_stress_type(i)
	_.log_table(i.parts.stems, 'i.parts.stems')
	_.log_table(i.parts.endings, 'i.parts.endings')

	_.ends(module, func)
end


return export
