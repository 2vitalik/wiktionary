local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/forms/noun')  -- '..'
local adj_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/forms/adj')  -- '..'


local module = 'output.forms.common'


-- @call
local function init_forms(i)  -- Генерация словоформ
	func = "init_forms"
	_.call(module, func)

	local o = i.out_args
	local d = i.data

	o['nom-sg'] = d.stems['nom-sg'] .. d.endings['nom-sg']
	o['gen-sg'] = d.stems['gen-sg'] .. d.endings['gen-sg']
	o['dat-sg'] = d.stems['dat-sg'] .. d.endings['dat-sg']
	o['acc-sg'] = ''
	o['ins-sg'] = d.stems['ins-sg'] .. d.endings['ins-sg']
	o['prp-sg'] = d.stems['prp-sg'] .. d.endings['prp-sg']
	o['nom-pl'] = d.stems['nom-pl'] .. d.endings['nom-pl']
	o['gen-pl'] = d.stems['gen-pl'] .. d.endings['gen-pl']
	o['dat-pl'] = d.stems['dat-pl'] .. d.endings['dat-pl']
	o['acc-pl'] = ''
	o['ins-pl'] = d.stems['ins-pl'] .. d.endings['ins-pl']
	o['prp-pl'] = d.stems['prp-pl'] .. d.endings['prp-pl']

	-- TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
end


-- @starts
local function init_srt_forms(o, stems, endings)  -- todo move to `init_forms` (with if i.adj) ?
	func = "init_srt_forms"
	_.starts(module, func)

	o['srt-sg'] = stems['srt-sg'] .. endings['srt-sg']
	o['srt-pl'] = stems['srt-pl'] .. endings['srt-pl']
	_.ends(module, func)
end


-- @starts
local function fix_stress(o)
	func = "fix_stress"
	_.starts(module, func)

	-- Add stress if there is no one
	if _.contains_several(o['nom-sg'], '{vowel}') and not _.contains(o['nom-sg'], '[́ ё]') then
		-- perhaps this is redundant for nom-sg?
		_.replace(o, 'nom-sg', '({vowel})({consonant}*)$', '%1́ %2')
	end
	if _.contains_several(o['gen-pl'], '{vowel+ё}') and not _.contains(o['gen-pl'], '[́ ё]') then
		_.replace(o, 'gen-pl', '({vowel})({consonant}*)$', '%1́ %2')
	end

	_.ends(module, func)
end


-- Выбор винительного падежа
-- @starts
local function choose_accusative_forms(i)
	func = "choose_accusative_forms"
	_.starts(module, func)

	local o = i.out_args
	local d = i.data

	o['acc-sg-in'] = ''
	o['acc-sg-an'] = ''
	o['acc-pl-in'] = ''
	o['acc-pl-an'] = ''

	if i.gender == 'm' or (i.gender == 'n' and i.output_gender == 'm') then
		if i.animacy == 'in' then
			o['acc-sg'] = o['nom-sg']
		elseif i.animacy == 'an' then
			o['acc-sg'] = o['gen-sg']
		else
			o['acc-sg-in'] = o['nom-sg']
			o['acc-sg-an'] = o['gen-sg']
		end
	elseif i.gender == 'f' then
		if _.equals(i.stem.type, {'f-3rd', 'f-3rd-sibilant'}) then
			o['acc-sg'] = o['nom-sg']
		else
			o['acc-sg'] = d.stems['acc-sg'] .. d.endings['acc-sg']  -- todo: don't use `data` here?
		end
	elseif i.gender == 'n' then
		o['acc-sg'] = o['nom-sg']
	end

	if i.animacy == 'in' then
		o['acc-pl'] = o['nom-pl']
	elseif i.animacy == 'an' then
		o['acc-pl'] = o['gen-pl']
	else
		o['acc-pl-in'] = o['nom-pl']
		o['acc-pl-an'] = o['gen-pl']
	end

	_.ends(module, func)
end


-- @starts
local function second_ins_case(out_args, gender)
	func = "second_ins_case"
	_.starts(module, func)

	local ins_sg2

	-- Второй творительный
	if gender == 'f' then
		ins_sg2 = _.replaced(out_args['ins-sg'], 'й$', 'ю')
		if ins_sg2 ~= out_args['ins-sg'] then
			out_args['ins-sg2'] = ins_sg2
		end
	end

	_.ends(module, func)
end


-- @starts
function export.generate_out_args(i)
	func = "generate_out_args"
	_.starts(module, func)

	local o = i.out_args

	init_forms(i)
	if i.adj then
		init_srt_forms(o, i.data.stems, i.data.endings)
		if _.contains(i.rest_index, {'⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)'}) then
			o['краткая'] = '⊠'
		elseif _.contains(i.rest_index, {'✕', '×', 'x', 'х', 'X', 'Х'}) then
			o['краткая'] = '✕'
		elseif _.contains(i.rest_index, {'%-', '—', '−'}) then
			o['краткая'] = '−'
		else
			o['краткая'] = '1'
		end
	end

	fix_stress(o)

	for key, value in pairs(o) do
		-- replace 'ё' with 'е' when unstressed
		-- if _.contains_once(info.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(info.rest_index, 'ё') then  -- trying to bug-fix
		if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(i.rest_index, 'ё') then
			if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt-sg' then
				o[key] = _.replaced(value, 'ё', 'е') .. ' // ' .. _.replaced(value, '́', '')
			else
				o[key] = _.replaced(value, 'ё', 'е')  -- обычный случай
			end
		end
	end

	if i.noun then
		noun_forms.apply_obelus(o, i.rest_index)
	end

	choose_accusative_forms(i)

	second_ins_case(o, i.gender)

	if i.noun then
		noun_forms.apply_specific_3(o, i.gender, i.rest_index)
	end

	if i.adj then
		adj_forms.add_comparative(o, i.rest_index, i.stress_type, i.stem.type, i.stem)
	end

	for key, value in pairs(o) do
--		INFO Удаляем ударение, если только один слог:
		o[key] = noun_forms.remove_stress_if_one_syllable(value)
	end

	if i.adj then
		if i.postfix then
			local keys
			keys = {
				'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',
				'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',
			}  -- list
			for j, key in pairs(keys) do  -- list
				o[key] = o[key] .. 'ся'
			end
		end
	end

	_.ends(module, func)
end


-- @starts
function export.join_forms(out_args_1, out_args_2)  -- todo: rename to `out_args`
	func = "join_forms"
	_.starts(module, func)

	local keys, out_args, delim

	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
		'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
		'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
		'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
		'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
		'ins-sg2',
		'ins-sg2-f',
		'зализняк1', 'зализняк',
		'error',
	}  -- list

	out_args = out_args_1
	out_args['зализняк-1'] = out_args_1['зализняк']
	out_args['зализняк-2'] = out_args_2['зализняк']
	for i, key in pairs(keys) do  -- list
		if not _.has_key(out_args[key]) and not _.has_key(out_args_2[key]) then
			-- pass
		elseif not _.has_key(out_args[key]) and _.has_key(out_args_2[key]) then  -- INFO: Если out_args[key] == nil
			out_args[key] = out_args_2[key]
		elseif out_args[key] ~= out_args_2[key] and out_args_2[key] then
			delim = '<br/>'
			if _.equals(key, {'зализняк1', 'зализняк'}) then
				delim = '&nbsp;'
			end
			-- TODO: <br/> только для падежей
			out_args[key] = out_args[key] .. '&nbsp;//' .. delim .. out_args_2[key]
		end
		if not _.has_key(out_args[key]) or not out_args[key] then  -- INFO: Если out_args[key] == nil
			out_args[key] = ''
		end
	end

	_.ends(module, func)
	return out_args
end


-- @starts
function export.plus_forms(sub_forms)  -- todo: rename to `out_args`
	func = "plus_forms"
	_.starts(module, func)

	local keys, out_args, delim

	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		-- 'ins-sg2',
		'зализняк1', 'зализняк',
		'error',
	}  -- list
	out_args = sub_forms[1]  -- todo: rename to `out_args`
	for i, forms2 in pairs(sub_forms) do  -- list  -- todo: rename to `out_args`
		if i ~= 1 then
			for j, key in pairs(keys) do  -- list
				if not out_args[key] and forms2[key] then  -- INFO: Если out_args[key] == nil
					out_args[key] = forms2[key]
				elseif out_args[key] ~= forms2[key] and forms2[key] then
					delim = '-'
					if _.equals(key, {'зализняк1', 'зализняк'}) then
						delim = ' + '
					end
					out_args[key] = out_args[key] .. delim .. forms2[key]
				end
				if not out_args[key] then  -- INFO: Если out_args[key] == nil
					out_args[key] = ''
				end
			end
		end
	end

	_.ends(module, func)
	return out_args
end


return export
