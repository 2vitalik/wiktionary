local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local syllables = require("Модуль:слоги")


local module = 'output.result'


-- Использование дефисов вместо подчёркивания
-- @starts
local function replace_underscore_with_hyphen(out_args)
	func = "replace_underscore_with_hyphen"
	_.starts(module, func)

	local keys, old_key

	keys = {
		'nom-sg',   'gen-sg',   'dat-sg',   'acc-sg',   'ins-sg',   'prp-sg',
		'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
		'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
		'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
		'nom-pl',   'gen-pl',   'dat-pl',   'acc-pl',   'ins-pl',   'prp-pl',
--		'nom-sg2', 'gen-sg2', 'dat-sg2', 'acc-sg2', 'ins-sg2', 'prp-sg2',
--		'nom-pl2', 'gen-pl2', 'dat-pl2', 'acc-pl2', 'ins-pl2', 'prp-pl2',
		'voc-sg',  'loc-sg',  'prt-sg',
		'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
		'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
		'ins-sg2',  -- temp?
		'ins-sg2-f',
	}  -- list
	for i, new_key in pairs(keys) do  -- list
		old_key = mw.ustring.gsub(new_key, '-', '_')
		if _.has_key(out_args[old_key]) then
			out_args[new_key] = out_args[old_key]
		end
	end

	_.ends(module, func)
end


-- Формирование параметров рода и одушевлённости для подстановки в шаблон
-- @starts
local function forward_gender_animacy(out_args, data)
	func = "forward_gender_animacy"
	_.starts(module, func)

	local genders, animacies

	-- Род:
	genders = {m='муж', f='жен', n='ср', mf='мж', mn='мс', fm='жм', fn='жс', nm='см', nf='сж' }  -- dict
	if data.common_gender then
		out_args['род'] = 'общ'
	elseif data.output_gender then
		out_args['род'] = genders[data.output_gender]
	elseif data.gender then
		out_args['род'] = genders[data.gender]
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
		out_args['кат'] = animacies[data.output_animacy]
	else
		out_args['кат'] = animacies[data.animacy]
	end

	_.ends(module, func)
end


-- @starts
local function forward_args(out_args, data)
	func = "forward_args"
	_.starts(module, func)

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
				out_args[key] = args[key]
			else
				out_args[key] = args[key] .. '<sup>△</sup>'
			end
		end
	end

	keys = {
		'П', 'Пр', 'Сч',
		'hide-text', 'зачин', 'слоги', 'дореф',
		'скл', 'зализняк', 'зализняк1', 'чередование',
		'pt', 'st', 'затрудн', 'клитика',
		'коммент', 'тип', 'степень',
	}  -- list
	for i, key in pairs(keys) do  -- list
		if _.has_value(args[key]) then
			out_args[key] = args[key]
		end
	end

	if _.has_key(out_args['слоги']) then
		if not _.contains(out_args['слоги'], '%<') then
			out_args['слоги'] = syllables.get_syllables(out_args['слоги'])
		end
	else
		out_args['слоги'] = data.word.unstressed  -- fixme: может всё-таки stressed?
	end

	_.ends(module, func)
end


-- @starts
local function additional_arguments(out_args, data)
	func = "additional_arguments"
	_.starts(module, func)

	-- RU (склонение)
	if _.contains(data.rest_index, '0') then
		out_args['скл'] = 'не'
	elseif data.adj then
		out_args['скл'] = 'а'
	elseif data.pronoun then
		out_args['скл'] = 'мс'
	elseif _.endswith(data.word.unstressed, '[ая]') then
		out_args['скл'] = '1'
	else
		if data.gender == 'm' or data.gender == 'n' then
			out_args['скл'] = '2'
		else
			out_args['скл'] = '3'
		end
	end

	-- RU (чередование)
	if _.contains(data.index, '%*') then
		out_args['чередование'] = '1'
	end

	if data.pt then
		out_args['pt'] = '1'
	end

	-- RU ("-" в индексе)
	-- TODO: Здесь может быть глюк, если случай глобального `//` и `rest_index` пуст (а исходный `index` не подходит, т.к. там может быть не тот дефис -- в роде)
	if data.rest_index then
		if _.contains(data.rest_index, {'%-', '—', '−'}) then
			out_args['st'] = '1'
			out_args['затрудн'] = '1'
		end
	else
		-- pass  -- TODO
	end

	_.ends(module, func)
end


--------------------------------------------------------------------------------


-- @starts
function export.finalize(data, out_args)
	func = "finalize"
	_.starts(module, func)

	out_args['stem_type'] = data.stem.type  -- for testcases
	out_args['stress_type'] = data.stress_type  -- for categories   -- is really used?
	out_args['dev'] = dev_prefix

	additional_arguments(out_args, data)
	replace_underscore_with_hyphen(out_args)

	if data.noun then
		forward_gender_animacy(out_args, data)
	end

	forward_args(out_args, data)

	if not _.has_key(out_args['зализняк']) then
		out_args['зализняк'] = '??'
	end

	if not _.has_key(out_args['error_category']) and data.word_cleared ~= data.base then
		out_args['error_category'] = 'Ошибка в шаблоне "сущ-ru" (слово не совпадает с заголовком статьи)'
	end

	_.ends(module, func)
	return out_args
end


return export
