local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/prepare/endings')  -- '.'
local stress_apply = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/prepare/stress_apply')  -- '.'


local module = 'modify.prepare'


-- @starts
function export.prepare(info)
	func = "prepare"
	_.starts(module, func)

--	INFO: Generates `.endings` and `.stems`

	-- todo: create info.data.* !!!

	-- todo: logging info
	info.data.endings = endings.get_endings(info)

	-- todo: logging info
	info.data.stems = {}  -- dict
	stress_apply.apply_stress_type(info)
	_.log_table(info.data.stems, 'info.data.stems')
	_.log_table(info.data.endings, 'info.data.endings')

	_.ends(module, func)
end


return export
