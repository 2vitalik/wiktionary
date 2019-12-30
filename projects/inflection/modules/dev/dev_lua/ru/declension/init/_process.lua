local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local stem_type = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stem_type')  -- '.'
local stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stress')  -- '.'
local o = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/init_out_args')  -- '.'
local r = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/result')  -- '.'


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

	if not i.stress_type then  -- если ударение не указано
		if _.contains(i.rest_index, '0') then  -- если несклоняемая схема
			i.stress_type = ''
		else
--			INFO: Если при этом есть какой-то индекс, это явно ОШИБКА
			if _.has_value(i.rest_index) then
				r.add_error(i, 'Нераспознанная часть индекса: ' .. i.rest_index)
				_.ends(module, func)
				return i
			end

--			INFO: Если же индекса вообще нет, то и формы просто не известны:
			i.has_index = false
			_.ends(module, func)
			return i
		end
	end

	_.log_info('Вычисление схемы ударения')
	stress.get_stress_schema(i)
	_.log_table(i.stress_schema['stem'], "info.stress_schema['stem']")
	_.log_table(i.stress_schema['ending'], "info.stress_schema['ending']")

	_.log_info('Определение типа основы (stem_type)')
	stem_type.get_stem_type(i)
	_.log_value(i.stem.type, 'info.stem.type')
	_.log_value(i.stem.base_type, 'info.stem.base_type')

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem.stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(i.stem.stressed, '[́ ё]') then  -- and not info.absent_stress ??
		if _.equals(i.stress_type, {"f", "f'"}) then
			i.stem.stressed = _.replaced(i.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(i.rest_index, '%*') then
			-- pass  -- *** поставим ударение позже, после чередования
		else
			i.stem.stressed = _.replaced(i.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(i.stem.stressed, 'info.stem.stressed')

	_.log_info('Инициализируем `info.out_args`')
	o.init_out_args(i)

	_.ends(module, func)
	return i
end


return export
