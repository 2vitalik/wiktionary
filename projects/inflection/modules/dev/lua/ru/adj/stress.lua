local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- Данные: ударность основы и окончания в зависимости от схемы ударения
function export.get_adj_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	_.log_func('stress', 'get_adj_stress_schema')

	local stress_schema, types, cases, sg_value

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema
	stress_schema = {  -- dict
		stem = {  -- dict
			full = _.startswith(stress_type, {"a", "a/"}),
			srt_sg = true,
			srt_sg_f = _.endswith(stress_type, {"/a", "/a'"}) or _.equals(stress_type, {'a', "a'"}),
			srt_sg_n = _.endswith(stress_type, {"/a", "/c", "/a'", "/c'", "/c''"}) or _.equals(stress_type, {'a', "a'"}),
			srt_pl = _.endswith(stress_type, {"/a", "/c", "/a'", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'a', "a'", "b'"}),
		},  -- dict
		ending = {  -- dict
			full = _.startswith(stress_type, {"b", "b/"}),
			srt_sg = false,
			srt_sg_f = _.endswith(stress_type, {"/b", "/c", "/a'", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'b', "a'", "b'"}),
			srt_sg_n = _.endswith(stress_type, {"/b", "/b'", "/c''"}) or _.equals(stress_type, {'b', "b'"}),
			srt_pl = _.endswith(stress_type, {"/b", "/b'", "/c'", "/c''"}) or _.equals(stress_type, {'b', "b'"}),
		},  -- dict
	}  -- dict

	types = {'stem', 'ending'}
	cases = {
		'sg', 'pl',
		'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
		'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
	}  -- list
	for i, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['full']
		for i, case in pairs(cases) do  -- list
			stress_schema[type][case] = sg_value
		end
	end

	return stress_schema
end


return export
