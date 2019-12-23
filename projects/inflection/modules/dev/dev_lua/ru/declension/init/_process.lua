local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local stem_type = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stem_type')  -- '.'
local stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stress')  -- '.'
local o = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/init_out_args')  -- '.'
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/result')  -- '.'


local module = 'init.process'


-- @starts
function export.process(i)
	func = "process"
	_.starts(module, func)

	_.log_info('Извлечение информации об ударении (stress_type)')
	stress.extract_stress_type(i)  -- todo: move to `parse`
	_.log_value(i.stress_type, 'info.stress_type')

	if r.has_error(i) then
		_.ends(module, func)
		return i
	end

	_.log_info('Вычисление схемы ударения')
	stress.get_stress_schema(i)
	_.log_table(i.stress_schema['stem'], "info.stress_schema['stem']")
	_.log_table(i.stress_schema['ending'], "info.stress_schema['ending']")

	_.log_info('Определение типа основы (stem_type)')
	stem_type.get_stem_type(i)
	_.log_value(i.stem.type, 'info.stem.type')
	_.log_value(i.stem.base_type, 'info.stem.base_type')

	_.log_info('Инициализируем `info.out_args`')
	o.init_out_args(i)

	_.ends(module, func)
	return i
end


return export
