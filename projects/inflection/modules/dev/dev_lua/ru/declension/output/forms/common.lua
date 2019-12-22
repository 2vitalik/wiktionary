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

	o['nom_sg'] = d.stems['nom_sg'] .. d.endings['nom_sg']
	o['gen_sg'] = d.stems['gen_sg'] .. d.endings['gen_sg']
	o['dat_sg'] = d.stems['dat_sg'] .. d.endings['dat_sg']
	o['acc_sg'] = ''
	o['ins_sg'] = d.stems['ins_sg'] .. d.endings['ins_sg']
	o['prp_sg'] = d.stems['prp_sg'] .. d.endings['prp_sg']
	o['nom_pl'] = d.stems['nom_pl'] .. d.endings['nom_pl']
	o['gen_pl'] = d.stems['gen_pl'] .. d.endings['gen_pl']
	o['dat_pl'] = d.stems['dat_pl'] .. d.endings['dat_pl']
	o['acc_pl'] = ''
	o['ins_pl'] = d.stems['ins_pl'] .. d.endings['ins_pl']
	o['prp_pl'] = d.stems['prp_pl'] .. d.endings['prp_pl']

	-- TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
end


-- @starts
local function init_srt_forms(o, stems, endings)  -- todo move to `init_forms` (with if i.adj) ?
	func = "init_srt_forms"
	_.starts(module, func)

	o['srt_sg'] = stems['srt_sg'] .. endings['srt_sg']
	o['srt_pl'] = stems['srt_pl'] .. endings['srt_pl']
	_.ends(module, func)
end


-- @starts
local function fix_stress(o)
	func = "fix_stress"
	_.starts(module, func)

	-- Add stress if there is no one
	if _.contains_several(o['nom_sg'], '{vowel}') and not _.contains(o['nom_sg'], '[́ ё]') then
		-- perhaps this is redundant for nom_sg?
		_.replace(o, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
	end
	if _.contains_several(o['gen_pl'], '{vowel+ё}') and not _.contains(o['gen_pl'], '[́ ё]') then
		_.replace(o, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
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

	o['acc_sg_in'] = ''
	o['acc_sg_an'] = ''
	o['acc_pl_in'] = ''
	o['acc_pl_an'] = ''

	if i.gender == 'm' or (i.gender == 'n' and i.output_gender == 'm') then
		if i.animacy == 'in' then
			o['acc_sg'] = o['nom_sg']
		elseif i.animacy == 'an' then
			o['acc_sg'] = o['gen_sg']
		else
			o['acc_sg_in'] = o['nom_sg']
			o['acc_sg_an'] = o['gen_sg']
		end
	elseif i.gender == 'f' then
		if _.equals(i.stem.type, {'f-3rd', 'f-3rd-sibilant'}) then
			o['acc_sg'] = o['nom_sg']
		else
			o['acc_sg'] = d.stems['acc_sg'] .. d.endings['acc_sg']  -- todo: don't use `data` here?
		end
	elseif i.gender == 'n' then
		o['acc_sg'] = o['nom_sg']
	end

	if i.animacy == 'in' then
		o['acc_pl'] = o['nom_pl']
	elseif i.animacy == 'an' then
		o['acc_pl'] = o['gen_pl']
	else
		o['acc_pl_in'] = o['nom_pl']
		o['acc_pl_an'] = o['gen_pl']
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
		ins_sg2 = _.replaced(out_args['ins_sg'], 'й$', 'ю')
		if ins_sg2 ~= out_args['ins_sg'] then
			out_args['ins_sg2'] = ins_sg2
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
			if i.adj and _.contains(i.stress_type, "a'") and i.gender == 'f' and key == 'srt_sg' then
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
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
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
		'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
		'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
		'nom_sg_m', 'gen_sg_m', 'dat_sg_m', 'acc_sg_m', 'ins_sg_m', 'prp_sg_m',
		'nom_sg_n', 'gen_sg_n', 'dat_sg_n', 'acc_sg_n', 'ins_sg_n', 'prp_sg_n',
		'nom_sg_f', 'gen_sg_f', 'dat_sg_f', 'acc_sg_f', 'ins_sg_f', 'prp_sg_f',
		'srt_sg',  'srt_sg_m',  'srt_sg_n',  'srt_sg_f',  'srt_pl',
		'acc_sg_m_a', 'acc_sg_m_n', 'acc_pl_a', 'acc_pl_n',
		'ins_sg2',
		'ins_sg2_f',
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
		'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
		'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
		-- 'ins_sg2',
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
