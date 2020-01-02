local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'data.stress.pronoun'


-- @starts
function export.get_pronoun_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	func = "get_pronoun_stress_schema"
	_.starts(module, func)


	-- todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema
	local stress_schema = {}  -- AttrDict
	stress_schema.stem = {}  -- dict
	stress_schema.ending = {}  -- dict
	stress_schema.stem['sg'] = _.equals(stress_type, "a")
	stress_schema.stem['pl'] = _.equals(stress_type, "a")
	stress_schema.ending['sg'] = _.equals(stress_type, "b")
	stress_schema.ending['pl'] = _.equals(stress_type, "b")

	types = {'stem', 'ending'}
	sg_cases = {'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg'}  -- list
	pl_cases = {'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl'}  -- list
	for j, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['sg']
		pl_value = stress_schema[type]['pl']
		for j, case in pairs(sg_cases) do  -- list
			stress_schema[type][case] = sg_value
		end
		for j, case in pairs(pl_cases) do  -- list
			stress_schema[type][case] = pl_value
		end
	end

	return _.returns(module, func, stress_schema)
end


return export
