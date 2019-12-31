local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse/common')  -- 'declension.'
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/result')  -- 'declension.'
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

	local info = parse.parse(base, args)
	info.frame = frame  -- todo: move to `parse`
	if r.has_error(info) then
		_.ends(module, func)
		return info.out_args
	end

--	INFO: Запуск основного алгоритма и получение результирующих словоформ:
	run.run(info)

	_.ends(module, func)
	return info.out_args
end


return export


-- todo: rename `i.data` to `i.parts`
-- todo: rename `i.out_args` to `i.result`
