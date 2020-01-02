local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'data.stress.noun'


-- Данные: ударность основы и окончания в зависимости от схемы ударения
-- @starts
function export.get_noun_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	func = "get_noun_stress_schema"
	_.starts(module, func)

	local stress_schema, types, sg_value, pl_value

	-- todo: Сгенерировать все `stress_schema` для всех видов `stress_type` заранее и потом просто использовать/загружать их

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema = {}  -- AttrDict
	stress_schema.stem = {}  -- dict
	stress_schema.ending = {}  -- dict
	stress_schema.stem['sg']     = _.equals(stress_type, {"a", "c", "e"})
	stress_schema.stem['acc-sg'] = _.equals(stress_type, {"a", "c", "e", "d'", "f'"})
	stress_schema.stem['ins-sg'] = _.equals(stress_type, {"a", "c", "e", "b'", "f''"})
	stress_schema.stem['pl']     = _.equals(stress_type, {"a", "d", "d'"})
	stress_schema.stem['nom-pl'] = _.equals(stress_type, {"a", "d", "d'", "e", "f", "f'", "f''"})
	stress_schema.ending['sg']     = _.equals(stress_type, {"b", "b'", "d", "d'", "f", "f'", "f''"})
	stress_schema.ending['acc-sg'] = _.equals(stress_type, {"b", "b'", "d", "f", "f''"})
	stress_schema.ending['ins-sg'] = _.equals(stress_type, {"b", "d", "d'", "f", "f'"})
	stress_schema.ending['pl']     = _.equals(stress_type, {"b", "b'", "c", "e", "f", "f'", "f''"})
	stress_schema.ending['nom-pl'] = _.equals(stress_type, {"b", "b'", "c"})

	types = {'stem', 'ending'}
	for j, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['sg']
		stress_schema[type]['nom-sg'] = sg_value
		stress_schema[type]['gen-sg'] = sg_value
		stress_schema[type]['dat-sg'] = sg_value
		stress_schema[type]['prp-sg'] = sg_value

		pl_value = stress_schema[type]['pl']
		stress_schema[type]['gen-pl'] = pl_value
		stress_schema[type]['dat-pl'] = pl_value
		stress_schema[type]['ins-pl'] = pl_value
		stress_schema[type]['prp-pl'] = pl_value
	end

	return _.returns(module, func, stress_schema)
end


return export
