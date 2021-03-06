local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local stem_type = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stem_type')  -- '.'
local stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/init/process/stress')  -- '.'
local init_result = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/init_result')  -- '.'
local e = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/error')  -- '.'


local module = 'init.process'


-- @starts
function export.process(i)
	func = "process"
	_.starts(module, func)

	_.log_info('Извлечение информации об ударении (stress_type)')
	stress.extract_stress_type(i)  -- todo: move to `parse`
	_.log_value(i.stress_type, 'i.stress_type')

	if e.has_error(i) then
		return _.returns(module, func, i)
	end

	if not i.stress_type then  -- если ударение не указано
		if _.contains(i.rest_index, '0') then  -- если несклоняемая схема
			i.stress_type = ''
		else
--			INFO: Если при этом есть какой-то индекс, это явно ОШИБКА
			if _.has_value(i.rest_index) then
				e.add_error(i, 'Нераспознанная часть индекса: ' .. i.rest_index)
				return _.returns(module, func, i)
			end

--			INFO: Если же индекса вообще нет, то и формы просто не известны:
			i.has_index = false
			return _.returns(module, func, i)
		end
	end

	_.log_info('Вычисление схемы ударения')
	stress.get_stress_schema(i)

	_.log_info('Определение типа основы (stem_type)')
	stem_type.get_stem_type(i)
	_.log_value(i.stem.type, 'i.stem.type')
	_.log_value(i.stem.base_type, 'i.stem.base_type')

--	INFO: Итак, ударение мы получили.

--	INFO: Добавление ударения для `stem.stressed` (если его не было)
--	INFO: Например, в слове только один слог, или ударение было на окончание
	if not _.contains(i.stem.stressed, '[́ ё]') then  -- and not i.absent_stress ??
		if _.equals(i.stress_type, {"f", "f'"}) then
			i.stem.stressed = _.replaced(i.stem.stressed, '^({consonant}*)({vowel})', '%1%2́ ')
		elseif _.contains(i.rest_index, '%*') then
			-- pass  -- *** поставим ударение позже, после чередования
		else
			i.stem.stressed = _.replaced(i.stem.stressed, '({vowel})({consonant}*)$', '%1́ %2')
		end
	end

	_.log_value(i.stem.stressed, 'i.stem.stressed')

	_.log_info('Инициализируем `i.result`')
	init_result.init_result(i)

	return _.returns(module, func, i)
end


return export
