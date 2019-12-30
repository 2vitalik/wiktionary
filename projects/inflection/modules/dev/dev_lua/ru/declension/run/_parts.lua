local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local _prepare = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/prepare')  -- '.'  -- '_' /prepare
local _transform = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform')  -- '.'  -- '_' /transform


local module = 'modify'


-- @starts
function export.generate_parts(i)
	func = "generate_parts"
	_.starts(module, func)

	_prepare.prepare(i)
	_transform.transform(i)

	_.ends(module, func)
end


return export
