local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local noun_forms = require('Module:' .. dev_prefix .. 'inflection/ru/declension/output/forms/noun')  -- '..'


local module = 'output.forms.common'


-- @call
local function init_forms(stems, endings)  -- Генерация словоформ
	func = "init_forms"
	_.call(module, func)

	return {
		nom_sg = stems['nom_sg'] .. endings['nom_sg'],
		gen_sg = stems['gen_sg'] .. endings['gen_sg'],
		dat_sg = stems['dat_sg'] .. endings['dat_sg'],
		acc_sg = '',
		ins_sg = stems['ins_sg'] .. endings['ins_sg'],
		prp_sg = stems['prp_sg'] .. endings['prp_sg'],
		nom_pl = stems['nom_pl'] .. endings['nom_pl'],
		gen_pl = stems['gen_pl'] .. endings['gen_pl'],
		dat_pl = stems['dat_pl'] .. endings['dat_pl'],
		acc_pl = '',
		ins_pl = stems['ins_pl'] .. endings['ins_pl'],
		prp_pl = stems['prp_pl'] .. endings['prp_pl'],
	}  -- dict
	-- TODO: может инициировать и вообще везде работать уже с дефисами? Например, функцией сразу же преобразовывать
end


-- @starts
local function init_srt_forms(out_args, stems, endings)
	func = "init_srt_forms"
	_.starts(module, func)

	out_args['srt_sg'] = stems['srt_sg'] .. endings['srt_sg']
	out_args['srt_pl'] = stems['srt_pl'] .. endings['srt_pl']
	_.ends(module, func)
end


-- @starts
local function fix_stress(out_args)
	func = "fix_stress"
	_.starts(module, func)

	-- Add stress if there is no one
	if _.contains_several(out_args['nom_sg'], '{vowel}') and not _.contains(out_args['nom_sg'], '[́ ё]') then
		-- perhaps this is redundant for nom_sg?
		_.replace(out_args, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
	end
	if _.contains_several(out_args['gen_pl'], '{vowel+ё}') and not _.contains(out_args['gen_pl'], '[́ ё]') then
		_.replace(out_args, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
	end

	_.ends(module, func)
end


-- Выбор винительного падежа
-- @starts
local function choose_accusative_forms(out_args, data)
	func = "choose_accusative_forms"
	_.starts(module, func)

	out_args['acc_sg_in'] = ''
	out_args['acc_sg_an'] = ''
	out_args['acc_pl_in'] = ''
	out_args['acc_pl_an'] = ''

	if data.gender == 'm' or (data.gender == 'n' and data.output_gender == 'm') then
		if data.animacy == 'in' then
			out_args['acc_sg'] = out_args['nom_sg']
		elseif data.animacy == 'an' then
			out_args['acc_sg'] = out_args['gen_sg']
		else
			out_args['acc_sg_in'] = out_args['nom_sg']
			out_args['acc_sg_an'] = out_args['gen_sg']
		end
	elseif data.gender == 'f' then
		if _.equals(data.stem_type, {'f-3rd', 'f-3rd-sibilant'}) then
			out_args['acc_sg'] = out_args['nom_sg']
		else
			out_args['acc_sg'] = data.stems['acc_sg'] .. data.endings['acc_sg']
		end
	elseif data.gender == 'n' then
		out_args['acc_sg'] = out_args['nom_sg']
	end

	if data.animacy == 'in' then
		out_args['acc_pl'] = out_args['nom_pl']
	elseif data.animacy == 'an' then
		out_args['acc_pl'] = out_args['gen_pl']
	else
		out_args['acc_pl_in'] = out_args['nom_pl']
		out_args['acc_pl_an'] = out_args['gen_pl']
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
function export.generate_forms(data)
	func = "generate_forms"
	_.starts(module, func)

	local out_args, keys

	out_args = init_forms(data.stems, data.endings)
	if data.adj then
		init_srt_forms(out_args, data.stems, data.endings)
		if _.contains(data.rest_index, {'⊠', '%(x%)', '%(х%)', '%(X%)', '%(Х%)'}) then
			out_args['краткая'] = '⊠'
		elseif _.contains(data.rest_index, {'✕', '×', 'x', 'х', 'X', 'Х'}) then
			out_args['краткая'] = '✕'
		elseif _.contains(data.rest_index, {'%-', '—', '−'}) then
			out_args['краткая'] = '−'
		else
			out_args['краткая'] = '1'
		end
	end

	fix_stress(out_args)

	for key, value in pairs(out_args) do
		-- replace 'ё' with 'е' when unstressed
		-- if _.contains_once(data.stem.unstressed, 'ё') and _.contains(value, '́ ') and _.contains(data.rest_index, 'ё') then  -- trying to bug-fix
		if _.contains_once(value, 'ё') and _.contains(value, '́ ') and _.contains(data.rest_index, 'ё') then
			if data.adj and _.contains(data.stress_type, "a'") and data.gender == 'f' and key == 'srt_sg' then
				out_args[key] = _.replaced(value, 'ё', 'е') .. ' // ' .. _.replaced(value, '́', '')
			else
				out_args[key] = _.replaced(value, 'ё', 'е')  -- обычный случай
			end
		end
	end

	if data.noun then
		noun_forms.apply_obelus(out_args, data.rest_index)
	end

	choose_accusative_forms(out_args, data)

	second_ins_case(out_args, data.gender)

	if data.noun then
		noun_forms.apply_specific_3(out_args, data.gender, data.rest_index)
	end

	for key, value in pairs(out_args) do
--		INFO Удаляем ударение, если только один слог:
		out_args[key] = noun_forms.remove_stress_if_one_syllable(value)
	end

	if data.adj then
		if data.postfix then
			keys = {
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			}  -- list
			for i, key in pairs(keys) do  -- list
				out_args[key] = out_args[key] .. 'ся'
			end
		end
	end

	_.ends(module, func)
	return out_args
end


-- @starts
function export.join_forms(out_args_1, out_args_2)
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
function export.plus_forms(sub_forms)
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
	out_args = sub_forms[1]
	for i, forms2 in pairs(sub_forms) do  -- list
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
