local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


function export.get_pronoun_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	_.log_func('stress', 'get_pronoun_stress_schema')

	-- TODO: Пока не используется

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema
	stress_schema = {  -- dict
		stem = {  -- dict
			sg = _.equals(stress_type, "a"),
			pl = _.equals(stress_type, "b"),
		},  -- dict
		ending = {  -- dict
			sg = _.equals(stress_type, "b"),
			pl = _.equals(stress_type, "a"),
		},  -- dict
	}  -- dict
	return stress_schema
end


return export
