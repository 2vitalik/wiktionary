local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local syllables = require("Модуль:слоги")

-- Использование дефисов вместо подчёркивания
local function replace_underscore_with_hyphen(forms)
	_.log_func('result', 'replace_underscore_with_hyphen')

	local keys, old_key

	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
--		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
--		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
		'ins-sg2',  -- temp?
	}  -- list
	for i, new_key in pairs(keys) do  -- list
		old_key = mw.ustring.gsub(new_key, '-', '_')
		if _.has_key(forms[old_key]) then
			forms[new_key] = forms[old_key]
		end
	end
end


-- Формирование параметров рода и одушевлённости для подстановки в шаблон
local function forward_gender_animacy(forms, data)
	_.log_func('result', 'forward_gender_animacy')

	local genders, animacies

	-- Род:
	genders = {m='муж', f='жен', n='ср' }  -- dict
	if data.common_gender then
		forms['род'] = 'общ'
	elseif data.output_gender then
		forms['род'] = genders[data.output_gender]
	elseif data.gender then
		forms['род'] = genders[data.gender]
	else
		-- pass
	end

	-- Одушевлённость:
	animacies = {}  -- dict
	animacies['in'] = 'неодуш'
	animacies['an'] = 'одуш'
	animacies['in//an'] = 'неодуш-одуш'
	animacies['an//in'] = 'одуш-неодуш'
	if data.output_animacy then
		forms['кат'] = animacies[data.output_animacy]
	else
		forms['кат'] = animacies[data.animacy]
	end
end


local function forward_args(forms, data)
	_.log_func('result', 'forward_args')

	local keys, args

	args = data.args
	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
	}  -- list
	for i, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			if args[key] == '-' then
				forms[key] = args[key]
			else
				forms[key] = args[key] .. '<sup>△</sup>'
			end
		end
	end

	keys = {
		'П', 'Пр', 'Сч',
		'hide-text', 'зачин', 'слоги', 'дореф',
		'скл', 'зализняк', 'зализняк1', 'чередование',
		'pt', 'st', 'затрудн', 'клитика',
	}  -- list
	for i, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			forms[key] = args[key]
		end
	end

	if _.has_key(forms['слоги']) then
		forms['слоги'] = syllables.get_syllables(forms['слоги'])
	else
		forms['слоги'] = data.word
	end

	if _.has_key(args['коммент']) then
		if not forms['коммент'] then
			forms['коммент'] = ''
		end
		forms['коммент'] = forms['коммент'] .. args['коммент']
	end
end


local function additional_arguments(forms, data)
	_.log_func('result', 'additional_arguments')

	-- RU (склонение)
	if _.contains(data.rest_index, '0') then
		forms['скл'] = 'не'
	elseif data.adj then
		forms['скл'] = 'а'
	elseif data.pronoun then
		forms['скл'] = 'мс'
	elseif _.endswith(data.word, '[ая]') then
		forms['скл'] = '1'
	else
		if data.gender == 'm' or data.gender == 'n' then
			forms['скл'] = '2'
		else
			forms['скл'] = '3'
		end
	end

	-- RU (чередование)
	if _.contains(data.index, '%*') then
		forms['чередование'] = '1'
	end

	if data.pt then
		forms['pt'] = '1'
	end

	-- RU ("-" в индексе)
	-- TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
	if data.rest_index then
		if _.contains(data.rest_index, {'%-', '—', '−'}) then
			forms['st'] = '1'
			forms['затрудн'] = '1'
		end
	else
		-- pass  -- TODO
	end
end


--------------------------------------------------------------------------------


function export.finalize(data, forms)
	_.log_func('result', 'finalize')

	forms['stem_type'] = data.stem_type  -- for testcases
	forms['stress_type'] = data.stress_type  -- for categories   -- is really used?
	forms['dev'] = dev_prefix

	additional_arguments(forms, data)
	replace_underscore_with_hyphen(forms)

	forward_gender_animacy(forms, data)
	forward_args(forms, data)

	if not _.has_key(forms['зализняк']) then
		forms['зализняк'] = '??'
	end

	if not _.has_key(forms['error_category']) and data.word_cleared ~= data.base then
		forms['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
	end

	return forms
end


return export
