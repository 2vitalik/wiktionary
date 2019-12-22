local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local syllables = require("Модуль:слоги")


local module = 'output.result'


-- Использование дефисов вместо подчёркивания
-- @starts
local function replace_underscore_with_hyphen(out_args)
	func = "replace_underscore_with_hyphen"
	_.starts(module, func)

	local keys, old_key

	keys = {
		'nom-sg',   'gen-sg',   'dat-sg',   'acc-sg',   'ins-sg',   'prp-sg',
		'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
		'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
		'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
		'nom-pl',   'gen-pl',   'dat-pl',   'acc-pl',   'ins-pl',   'prp-pl',
--		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
--		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
		'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
		'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
		'ins-sg2',  -- temp?
		'ins-sg2-f',
	}  -- list
	for i, new_key in pairs(keys) do  -- list
		old_key = mw.ustring.gsub(new_key, '-', '_')
		if _.has_key(out_args[old_key]) then
			out_args[new_key] = out_args[old_key]
		end
	end

	_.ends(module, func)
end


-- @starts
local function forward_args(out_args, data)
	func = "forward_args"
	_.starts(module, func)

	local keys, args

	args = data.args
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
		out_args['слоги'] = data.word.unstressed  -- fixme: может всё-таки stressed?
	end

	_.ends(module, func)
end


-- @starts
function export.finalize(data, out_args)
	func = "finalize"
	_.starts(module, func)

	replace_underscore_with_hyphen(out_args)  -- fixme: this will be redundant soon
	forward_args(out_args, data)  -- fixme: move this to the ending of the main function

	_.ends(module, func)
	return out_args
end


return export
