local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '..'


local module = 'init.parse.init_stem'


-- @starts
function export.init_stem(i)  -- todo rename to `init_stem`
	func = "init_stem"
	_.starts(module, func)


--	INFO: Исходное слово без ударения:
	i.word.unstressed = _.replaced(i.word.stressed, '́ ', '')  -- todo: move outside this function

--	INFO: Исходное слово вообще без ударений (в т.ч. без грависа):
	i.word.cleared = _.replaced(_.replaced(_.replaced(i.word.unstressed, '̀', ''), 'ѐ', 'е'), 'ѝ', 'и')

	if i.adj then
		if _.endswith(i.word.stressed, 'ся') then
			i.postfix = true
			i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]ся$', '')
			i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]ся$', '')
		else
			i.stem.unstressed = _.replaced(i.word.unstressed, '{vowel}[йяе]$', '')
			i.stem.stressed = _.replaced(i.word.stressed, '{vowel}́ ?[йяе]$', '')
		end
	else
--		INFO: Удаляем окончания (-а, -е, -ё, -о, -я, -й, -ь), чтобы получить основу:
		i.stem.unstressed = _.replaced(i.word.unstressed, '[аеёийоьыя]$', '')
		i.stem.stressed = _.replaced(i.word.stressed, '[аеёийоьыя]́ ?$', '')
	end

	_.log_value(i.word.unstressed, 'i.word.unstressed')
	_.log_value(i.stem.unstressed, 'i.stem.unstressed')
	_.log_value(i.stem.stressed, 'i.stem.stressed')

	--  INFO: Случай, когда не указано ударение у слова:
	local several_vowels = _.contains_several(i.word.stressed, '{vowel+ё}')
	local has_stress = _.contains(i.word.stressed, '[́ ё]')
	if several_vowels and not has_stress then
		_.log_info('Ошибка: Не указано ударение в слове')
		e.add_error(i, 'Ошибка: Не указано ударение в слове')
		i.result.error_category = 'Ошибка в шаблоне "сущ-ru" (не указано ударение в слове)'
	end

	_.ends(module, func)
end


return export
