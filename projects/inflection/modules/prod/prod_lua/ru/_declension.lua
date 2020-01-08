local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local init = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init')  -- '_' /init
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- 'declension.'
local run = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run')  -- '_' /run


local module = 'declension'


-- @starts
function export.forms(base, args, frame)  -- todo: rename to `out_args`
	func = "forms"
	_.starts(module, func)

	local i = init.init_info(base, args, frame)
	if e.has_error(i) then
		return _.returns(module, func, i.result)
	end

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	run.run(i)

	return _.returns(module, func, i.result)
end


return export
