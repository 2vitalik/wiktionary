local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local index = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/index')  -- '..'
local result = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/out/result')  -- '..'


local module = 'output.init_out_args'

-- todo: move this to root `init` package


-- Формирование параметров рода и одушевлённости для подстановки в шаблон
-- @starts
local function forward_gender_animacy(i)
	func = "forward_gender_animacy"
	_.starts(module, func)

	local o = i.out_args

	-- Род:
	local genders = {m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж'}  -- dict

	if i.common_gender then
		o['род'] = 'общ'
	elseif i.output_gender then
		o['род'] = genders[i.output_gender]
	elseif i.gender then
		o['род'] = genders[i.gender]
	else
		-- pass
	end

	-- Одушевлённость:
	local animacies = {}  -- dict
	animacies['in'] = 'неодуш'
	animacies['an'] = 'одуш'
	animacies['in//an'] = 'неодуш-одуш'
	animacies['an//in'] = 'одуш-неодуш'

	if i.output_animacy then
		o['кат'] = animacies[i.output_animacy]
	else
		o['кат'] = animacies[i.animacy]
	end

	_.ends(module, func)
end


-- @starts
local function additional_arguments(i)
	func = "additional_arguments"
	_.starts(module, func)

	local o = i.out_args

	-- RU (склонение)
	if _.contains(i.rest_index, '0') then
		o['скл'] = 'не'
	elseif i.adj then
		o['скл'] = 'а'
	elseif i.pronoun then
		o['скл'] = 'мс'
	elseif _.endswith(i.word.unstressed, '[ая]') then
		o['скл'] = '1'
	else
		if i.gender == 'm' or i.gender == 'n' then
			o['скл'] = '2'
		else
			o['скл'] = '3'
		end
	end

	-- RU (чередование)
	if _.contains(i.index, '%*') then
		o['чередование'] = '1'
	end

	if i.pt then
		o['pt'] = '1'
	end

	-- RU ("-" в индексе)
	-- TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
	if i.rest_index then
		if _.contains(i.rest_index, {'%-', '—', '−'}) then
			o['st'] = '1'
			o['затрудн'] = '1'
		end
	else
		-- pass  -- TODO
	end

	_.ends(module, func)
end


-- @starts
function export.init_out_args(i)
	func = "init_out_args"
	_.starts(module, func)

	local o = i.out_args

	o['stem_type'] = i.stem.type  -- for testcases
	o['stress_type'] = i.stress_type  -- for categories   -- is really used?

	o['dev'] = dev_prefix

	index.get_zaliznyak(i)

	additional_arguments(i)

	if i.noun then
		forward_gender_animacy(i)
	end

	if not _.has_key(o['error_category']) and i.word.cleared ~= i.base then
		o['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
	end

	result.forward_args(i)

	_.ends(module, func)
end


return export
