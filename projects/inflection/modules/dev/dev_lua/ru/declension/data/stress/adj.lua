local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'data.stress.adj'


-- Данные: ударность основы и окончания в зависимости от схемы ударения
-- @starts
function export.get_adj_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	func = "get_adj_stress_schema"
	_.starts(module, func)

	-- todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema = {}  -- AttrDict
	stress_schema.stem = {}  -- dict
	stress_schema.ending = {}  -- dict
	stress_schema.stem['full'] = _.startswith(stress_type, {"a", "a/"})
	stress_schema.stem['srt-sg-m'] = true
	stress_schema.stem['srt-sg-f'] = _.endswith(stress_type, {"/a", "/a'"}) or _.equals(stress_type, {'a', "a'"})
	stress_schema.stem['srt-sg-n'] = _.endswith(stress_type, {"/a", "/c", "/a'", "/c'", "/c''"}) or _.equals(stress_type, {'a', "a'"})
	stress_schema.stem['srt-pl'] = _.endswith(stress_type, {"/a", "/c", "/a'", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'a', "a'", "b'"})
	stress_schema.ending['full'] = _.startswith(stress_type, {"b", "b/"})
	stress_schema.ending['srt-sg-m'] = false
	stress_schema.ending['srt-sg-f'] = _.endswith(stress_type, {"/b", "/c", "/a'", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'b', "a'", "b'"})
	stress_schema.ending['srt-sg-n'] = _.endswith(stress_type, {"/b", "/b'", "/c''"}) or _.equals(stress_type, {'b', "b'"})
	stress_schema.ending['srt-pl'] = _.endswith(stress_type, {"/b", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'b', "b'"})

	local types = {'stem', 'ending'}
	local cases
	cases = {
		'sg', 'pl',
		'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
		'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
	}  -- list
	for j, type in pairs(types) do  -- list
		local sg_value = stress_schema[type]['full']
		for j, case in pairs(cases) do  -- list
			stress_schema[type][case] = sg_value
		end
	end

	_.ends(module, func)
	return stress_schema
end


return export
