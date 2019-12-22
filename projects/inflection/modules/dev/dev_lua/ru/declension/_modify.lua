local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local _prepare = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/prepare')  -- '' =  -- '_' /prepare
local _transform = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/transform')  -- '' =  -- '_' /transform


local module = 'modify'


-- @starts
function export.modify(data)                                             --
	func = "modify"
	_.starts(module, func)

	_prepare.prepare(data)                                                    --
	_transform.transform(data)                                                --
									                                          --
	_.ends(module, func)                                                      --
end                                                                         --


return export
