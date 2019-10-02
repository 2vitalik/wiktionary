local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- Данные: ударность основы и окончания в зависимости от схемы ударения
function export.get_noun_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	_.log_func('stress', 'get_noun_stress_schema')

	local stress_schema, types, sg_value, pl_value

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	stress_schema = {  -- dict
		stem = {  -- dict
			sg     = _.equals(stress_type, {"a", "c", "e"}),
			acc_sg = _.equals(stress_type, {"a", "c", "e", "d'", "f'"}),
			ins_sg = _.equals(stress_type, {"a", "c", "e", "b'", "f''"}),
			pl     = _.equals(stress_type, {"a", "d", "d'"}),
			nom_pl = _.equals(stress_type, {"a", "d", "d'", "e", "f", "f'", "f''"}),
		},  -- dict
		ending = {  -- dict
			sg     = _.equals(stress_type, {"b", "b'", "d", "d'", "f", "f'", "f''"}),
			acc_sg = _.equals(stress_type, {"b", "b'", "d", "f", "f''"}),
			ins_sg = _.equals(stress_type, {"b", "d", "d'", "f", "f'"}),
			pl     = _.equals(stress_type, {"b", "b'", "c", "e", "f", "f'", "f''"}),
			nom_pl = _.equals(stress_type, {"b", "b'", "c"}),
		},  -- dict
	}  -- dict

	types = {'stem', 'ending'}
	for i, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['sg']
		stress_schema[type]['nom_sg'] = sg_value
		stress_schema[type]['gen_sg'] = sg_value
		stress_schema[type]['dat_sg'] = sg_value
		stress_schema[type]['prp_sg'] = sg_value

		pl_value = stress_schema[type]['pl']
		stress_schema[type]['gen_pl'] = pl_value
		stress_schema[type]['dat_pl'] = pl_value
		stress_schema[type]['ins_pl'] = pl_value
		stress_schema[type]['prp_pl'] = pl_value
	end

	return stress_schema
end


return export
