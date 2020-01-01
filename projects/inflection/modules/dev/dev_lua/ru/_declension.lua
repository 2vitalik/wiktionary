local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse')  -- 'declension.'  -- '_' /parse
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- 'declension.'
local run = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run')  -- '_' /run


local module = 'declension'


local function prepare_stash()  -- todo rename to `prepare_regexp_templates` or patterns
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


-- @starts
function export.forms(base, args, frame)  -- todo: rename to `out_args`
	func = "forms"
	_.starts(module, func)

	prepare_stash()  -- INFO: Заполняем шаблоны для регулярок

	-- `i` -- main `info` object
	local i = parse.parse(base, args, frame)
	if e.has_error(i) then
		_.ends(module, func)
		return i.result
	end

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	run.run(i)

	_.ends(module, func)
	return i.result
end


return export
