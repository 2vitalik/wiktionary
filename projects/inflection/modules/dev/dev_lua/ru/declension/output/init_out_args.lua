local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'output.init_out_args'


-- Формирование параметров рода и одушевлённости для подстановки в шаблон
-- @starts
local function forward_gender_animacy(info)
	func = "forward_gender_animacy"
	_.starts(module, func)

	local genders, animacies

	-- Род:
	genders = {m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж' }  -- dict
	if info.common_gender then
		info.out_args['род'] = 'общ'
	elseif info.output_gender then
		info.out_args['род'] = genders[info.output_gender]
	elseif info.gender then
		info.out_args['род'] = genders[info.gender]
	else
		-- pass
	end

	-- Одушевлённость:
	animacies = {}  -- dict
	animacies['in'] = 'неодуш'
	animacies['an'] = 'одуш'
	animacies['in//an'] = 'неодуш-одуш'
	animacies['an//in'] = 'одуш-неодуш'
	if info.output_animacy then
		info.out_args['кат'] = animacies[info.output_animacy]
	else
		info.out_args['кат'] = animacies[info.animacy]
	end

	_.ends(module, func)
end


-- @starts
local function additional_arguments(info)
	func = "additional_arguments"
	_.starts(module, func)

	-- RU (склонение)
	if _.contains(info.rest_index, '0') then
		info.out_args['скл'] = 'не'
	elseif info.adj then
		info.out_args['скл'] = 'а'
	elseif info.pronoun then
		info.out_args['скл'] = 'мс'
	elseif _.endswith(info.word.unstressed, '[ая]') then
		info.out_args['скл'] = '1'
	else
		if info.gender == 'm' or info.gender == 'n' then
			info.out_args['скл'] = '2'
		else
			info.out_args['скл'] = '3'
		end
	end

	-- RU (чередование)
	if _.contains(info.index, '%*') then
		info.out_args['чередование'] = '1'
	end

	if info.pt then
		info.out_args['pt'] = '1'
	end

	-- RU ("-" в индексе)
	-- TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
	if info.rest_index then
		if _.contains(info.rest_index, {'%-', '—', '−'}) then
			info.out_args['st'] = '1'
			info.out_args['затрудн'] = '1'
		end
	else
		-- pass  -- TODO
	end

	_.ends(module, func)
end


-- @starts
local function init_out_args(info)
	func = "init_out_args"
	_.starts(module, func)

	info.out_args['stem_type'] = info.stem.type  -- for testcases
	info.out_args['stress_type'] = info.stress_type  -- for categories   -- is really used?

	info.out_args['dev'] = dev_prefix
	info.out_args['зализняк'] = '??'  -- значение по умолчанию

	additional_arguments(info)

	if info.noun then
		forward_gender_animacy(info)
	end

	if not _.has_key(info.out_args['error_category']) and info.word.cleared ~= info.base then
		info.out_args['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
	end

	_.ends(module, func)
end


return export
