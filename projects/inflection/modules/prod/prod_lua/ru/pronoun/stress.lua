local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'pronoun.stress'


-- @starts
function export.get_pronoun_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	func = "get_pronoun_stress_schema"
	_.starts(module, func)

	-- TODO: Пока не используется

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema
	stress_schema = {  -- dict
		stem = {  -- dict
			sg = _.equals(stress_type, "a"),
			pl = _.equals(stress_type, "a"),
		},  -- dict
		ending = {  -- dict
			sg = _.equals(stress_type, "b"),
			pl = _.equals(stress_type, "b"),
		},  -- dict
	}  -- dict

	types = {'stem', 'ending'}
	sg_cases = {'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg'}  -- list
	pl_cases = {'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl'}  -- list
	for i, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['sg']
		pl_value = stress_schema[type]['pl']
		for i, case in pairs(sg_cases) do  -- list
			stress_schema[type][case] = sg_value
		end
		for i, case in pairs(pl_cases) do  -- list
			stress_schema[type][case] = pl_value
		end
	end

	_.ends(module, func)
	return stress_schema
end


return export
