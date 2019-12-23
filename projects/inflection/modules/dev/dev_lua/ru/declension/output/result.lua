local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local syllables = require("Модуль:слоги")


local module = 'output.result'


-- @starts
local function forward_args(out_args, info)
	func = "forward_args"
	_.starts(module, func)

	local keys, args

	args = info.args
	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
	}  -- list
	for i, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			if args[key] == '-' then
				out_args[key] = args[key]
			else
				out_args[key] = args[key] .. '<sup>△</sup>'
			end
		end
	end

	keys = {
		'П', 'Пр', 'Сч',
		'hide-text', 'зачин', 'слоги', 'дореф',
		'скл', 'зализняк', 'зализняк1', 'чередование',
		'pt', 'st', 'затрудн', 'клитика',
		'коммент', 'тип', 'степень',
	}  -- list
	for i, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			out_args[key] = args[key]
		end
	end

	if _.has_key(out_args['слоги']) then
		if not _.contains(out_args['слоги'], '%<') then
			out_args['слоги'] = syllables.get_syllables(out_args['слоги'])
		end
	else
		out_args['слоги'] = info.word.unstressed  -- fixme: может всё-таки stressed?
	end

	_.ends(module, func)
end


-- @starts
function export.finalize(info, out_args)
	func = "finalize"
	_.starts(module, func)

	forward_args(out_args, info)  -- fixme: move this to the ending of the main function

	_.ends(module, func)
	return out_args
end


return export
