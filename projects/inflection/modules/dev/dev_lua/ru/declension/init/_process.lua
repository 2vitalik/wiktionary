local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local stem_type = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stem_type')  -- '.'
local stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stress')  -- '.'
local o = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/init_out_args')  -- '.'


local module = 'init.process'


-- @starts
function export.process(info)
	func = "process"
	_.starts(module, func)

	_.log_info('Извлечение информации об ударении (stress_type)')
	info.stress_type, error = stress.extract_stress_type(info.rest_index)  -- todo: move to `parse`
	_.log_value(info.stress_type, 'info.stress_type')

	if error then
		-- out_args = result.finalize(data, error)
		-- todo: save error somewhere in `info` !!!
		_.ends(module, func)
		return info
		-- return out_args
	end

	_.log_info('Вычисление схемы ударения')
	info.stress_schema = stress.get_stress_schema(info.stress_type, info.adj, info.pronoun)
	_.log_table(info.stress_schema['stem'], "info.stress_schema['stem']")
	_.log_table(info.stress_schema['ending'], "info.stress_schema['ending']")

	_.log_info('Определение типа основы (stem_type)')
	info.stem.type, info.stem.base_type = stem_type.get_stem_type(info.stem.unstressed, info.word.unstressed, info.gender, info.adj, info.rest_index)
	_.log_value(info.stem.type, 'info.stem.type')
	_.log_value(info.stem.base_type, 'info.stem.base_type')

	_.log_info('Инициализируем `info.out_args`')
	o.init_out_args(info)

	_.ends(module, func)
	return info
end


return export
