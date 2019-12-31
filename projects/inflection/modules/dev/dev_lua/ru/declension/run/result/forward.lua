local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local syllables = require("Модуль:слоги")


local module = 'run.result.forward'


-- @starts
function export.forward_args(i)
	func = "forward_args"
	_.starts(module, func)

--	INFO: Используется дважды -- при инициализации, и потом в самом конце

	local keys, args
	local r = i.result

	args = i.args
	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
	}  -- list
	for j, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			if args[key] == '-' then
				r[key] = args[key]
			else
				r[key] = args[key] .. '<sup>△</sup>'
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
	for j, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			r[key] = args[key]
		end
	end

	if _.has_key(r['слоги']) then
		if not _.contains(r['слоги'], '%<') then
			r['слоги'] = syllables.get_syllables(r['слоги'])
		end
	else
		r['слоги'] = i.word.unstressed  -- fixme: может всё-таки stressed?
	end

	_.ends(module, func)
end


return export
