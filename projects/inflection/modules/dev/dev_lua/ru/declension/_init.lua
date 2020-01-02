local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local parse = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/parse')  -- ''  -- '_' /parse


local module = 'init'


local function prepare_regexp_patterns()
	_.clear_stash()
	_.add_stash('{vowel}', '[аеиоуыэюяАЕИОУЫЭЮЯ]')
	_.add_stash('{vowel+ё}', '[аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
	_.add_stash('{consonant}', '[^аеёиоуыэюяАЕЁИОУЫЭЮЯ]')
end


-- @starts
function export.init_info(base, args, frame)
	func = "init_info"
	_.starts(module, func)

	prepare_regexp_patterns()  -- INFO: Заполняем шаблоны для регулярок

	i = parse.parse(base, args, frame)

	return _.returns(module, func, i)
end


return export
