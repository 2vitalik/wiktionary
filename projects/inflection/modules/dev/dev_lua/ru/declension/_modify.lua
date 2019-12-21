local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local _prepare = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/_prepare')  -- '' =
local _transform = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/_transform')  -- '' =


local module = 'modify'


@a.starts(module)                                                             --
function export.modify(func, data)                                             --
	_prepare.prepare(data)                                                    --
	_transform.transform(data)                                                --
									                                          --
	_.ends(module, func)                                                      --
end                                                                         --


return export
