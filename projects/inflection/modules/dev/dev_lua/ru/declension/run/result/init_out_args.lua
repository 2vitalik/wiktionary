local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local index = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/index')  -- '..'
local forward = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/result/forward')  -- '..'


local module = 'run.result.init_out_args'

-- todo: move this to root `init` package


-- Формирование параметров рода и одушевлённости для подстановки в шаблон
-- @starts
local function forward_gender_animacy(i)
	func = "forward_gender_animacy"
	_.starts(module, func)

	local r = i.result

	-- Род:
	local genders = {m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж'}  -- dict

	if i.common_gender then
		r['род'] = 'общ'
	elseif i.output_gender then
		r['род'] = genders[i.output_gender]
	elseif i.gender then
		r['род'] = genders[i.gender]
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
		r['кат'] = animacies[i.output_animacy]
	else
		r['кат'] = animacies[i.animacy]
	end

	_.ends(module, func)
end


-- @starts
local function additional_arguments(i)
	func = "additional_arguments"
	_.starts(module, func)

	local r = i.result

	-- RU (склонение)
	if _.contains(i.rest_index, '0') then
		r['скл'] = 'не'
	elseif i.adj then
		r['скл'] = 'а'
	elseif i.pronoun then
		r['скл'] = 'мс'
	elseif _.endswith(i.word.unstressed, '[ая]') then
		r['скл'] = '1'
	else
		if i.gender == 'm' or i.gender == 'n' then
			r['скл'] = '2'
		else
			r['скл'] = '3'
		end
	end

	-- RU (чередование)
	if _.contains(i.index, '%*') then
		r['чередование'] = '1'
	end

	if i.pt then
		r['pt'] = '1'
	end

	-- RU ("-" в индексе)
	-- TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
	if i.rest_index then
		if _.contains(i.rest_index, {'%-', '—', '−'}) then
			r['st'] = '1'
			r['затрудн'] = '1'
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

	local r = i.result

	r['stem_type'] = i.stem.type  -- for testcases
	r['stress_type'] = i.stress_type  -- for categories   -- is really used?

	r['dev'] = dev_prefix

	index.get_zaliznyak(i)

	additional_arguments(i)

	if i.noun then
		forward_gender_animacy(i)
	end

	if _.contains(i.rest_index, {'⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)'}) then
		r['краткая'] = '⊠'
	elseif _.contains(i.rest_index, {'✕', '×', 'x', 'х', 'X', 'Х'}) then
		r['краткая'] = '✕'
	elseif _.contains(i.rest_index, {'%-', '—', '−'}) then
		r['краткая'] = '−'
	else
		r['краткая'] = '1'
	end

	if not _.has_key(r['error_category']) and i.word.cleared ~= i.base then
		r['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
	end

	forward.forward_args(i)

	_.ends(module, func)
end


return export
