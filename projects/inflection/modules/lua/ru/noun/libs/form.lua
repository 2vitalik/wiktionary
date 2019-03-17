local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local function init_forms(stems, endings)  -- Генерация словоформ
	_.log_func('forms', 'init_forms')

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


local function remove_stress_if_one_syllable(value)
	-- _.log_func('forms', 'remove_stress_if_one_syllable')

	if _.contains_once(value, '{vowel+ё}') then
		return _.replaced(value, '́ ', '')
	end
	return value
end


local function fix_stress(forms)
	_.log_func('forms', 'fix_stress')

	-- Add stress if there is no one
	if _.contains_several(forms['nom_sg'], '{vowel}') and not _.contains(forms['nom_sg'], '[́ ё]') then
		-- perhaps this is redundant for nom_sg?
		_.replace(forms, 'nom_sg', '({vowel})({consonant}*)$', '%1́ %2')
	end
	if _.contains_several(forms['gen_pl'], '{vowel+ё}') and not _.contains(forms['gen_pl'], '[́ ё]') then
		_.replace(forms, 'gen_pl', '({vowel})({consonant}*)$', '%1́ %2')
	end

	for key, value in pairs(forms) do
--		INFO Удаляем ударение, если только один слог:
		forms[key] = remove_stress_if_one_syllable(value)
	end
end


local function apply_obelus(forms, rest_index)
	_.log_func('forms', 'apply_obelus')

	if _.contains(rest_index, '÷') then
		forms['obelus'] = '1'
	end
end


-- Выбор винительного падежа
local function choose_accusative_forms(forms, data)
	_.log_func('forms', 'choose_accusative_forms')

	forms['acc_sg_in'] = ''
	forms['acc_sg_an'] = ''
	forms['acc_pl_in'] = ''
	forms['acc_pl_an'] = ''

	if data.gender == 'm' or (data.gender == 'n' and data.output_gender == 'm') then
		if data.animacy == 'in' then
			forms['acc_sg'] = forms['nom_sg']
		elseif data.animacy == 'an' then
			forms['acc_sg'] = forms['gen_sg']
		else
			forms['acc_sg_in'] = forms['nom_sg']
			forms['acc_sg_an'] = forms['gen_sg']
		end
	elseif data.gender == 'f' then
		if _.equals(data.stem_type, {'f-3rd', 'f-3rd-sibilant'}) then
			forms['acc_sg'] = forms['nom_sg']
		else
			forms['acc_sg'] = data.stems['acc_sg'] .. data.endings['acc_sg']
		end
	elseif data.gender == 'n' then
		forms['acc_sg'] = forms['nom_sg']
	end

	if data.animacy == 'in' then
		forms['acc_pl'] = forms['nom_pl']
	elseif data.animacy == 'an' then
		forms['acc_pl'] = forms['gen_pl']
	else
		forms['acc_pl_in'] = forms['nom_pl']
		forms['acc_pl_an'] = forms['gen_pl']
	end
end


local function second_ins_case(forms, gender)
	_.log_func('forms', 'second_ins_case')

	local ins_sg2

	-- Второй творительный
	if gender == 'f' then
		ins_sg2 = _.replaced(forms['ins_sg'], 'й$', 'ю')
		if ins_sg2 ~= forms['ins_sg'] then
			forms['ins_sg2'] = ins_sg2
		end
	end
end


local function apply_specific_3(forms, gender, rest_index)
	_.log_func('forms', 'apply_specific_3')

	-- Специфика по (3)
	if _.contains(rest_index, '%(3%)') or _.contains(rest_index, '③') then
		if _.endswith(forms['prp_sg'], 'и') then
			forms['prp_sg'] = forms['prp_sg'] .. ' // ' .. _.replaced(forms['prp_sg'], 'и$', 'е')
		end
		if gender == 'f' and _.endswith(forms['dat_sg'], 'и') then
			forms['dat_sg'] = forms['dat_sg'] .. ' // ' .. _.replaced(forms['dat_sg'], 'и$', 'е')
		end
	end
end


function export.generate_forms(data)
	_.log_func('forms', 'generate_forms')

	local forms, keys

	forms = init_forms(data.stems, data.endings)

	fix_stress(forms)

	for key, value in pairs(forms) do
		-- replace 'ё' with 'е' when unstressed
		if _.contains_once(data.stem, 'ё') and _.contains(value, '́ ') and _.contains(data.rest_index, 'ё') then
			forms[key] = _.replaced(value, 'ё', 'е')
		end
	end

	apply_obelus(forms, data.rest_index)

	choose_accusative_forms(forms, data)

	second_ins_case(forms, data.gender)

	apply_specific_3(forms, data.gender, data.rest_index)

	if data.adj then
		if data.postfix then
			keys = {
				'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
				'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
			}  -- list
			for i, key in pairs(keys) do  -- list
				forms[key] = forms[key] .. 'ся'
			end
		end
	end

	return forms
end


--------------------------------------------------------------------------------


local function prt_case(forms, args, index)  -- Разделительный падеж
	_.log_func('forms', 'prt_case')

	if _.contains(index, 'Р2') or _.contains(index, 'Р₂') then
		forms['prt_sg'] = forms['dat_sg']
	end
	if _.has_value(args['Р']) then
		forms['prt_sg'] = args['Р']
	end
end


local function loc_case(forms, args, index)  -- Местный падеж
	_.log_func('forms', 'loc_case')

	local loc, loc_prep

	if _.contains(index, 'П2') or _.contains(index, 'П₂') then
		loc = forms['dat_sg']
		loc = _.replaced(loc, '́ ', '')
		loc = _.replaced(loc, 'ё', 'е')
		loc = _.replaced(loc, '({vowel})({consonant}*)$', '%1́ %2')
		loc = remove_stress_if_one_syllable(loc)
		forms['loc_sg'] = loc
		loc_prep = '?'
		loc_prep = _.extract(index, 'П2%((.+)%)')
		if not loc_prep then
			loc_prep = _.extract(index, 'П₂%((.+)%)')
		end
		if not loc_prep then
			loc_prep = 'в, на'
		end
		forms['loc_sg'] = '(' .. loc_prep .. ') ' .. forms['loc_sg']
		if _.contains(index, '%[П') then
			forms['loc_sg'] = forms['loc_sg'] .. ' // ' .. forms['prp_sg']
		end
	end
	if _.has_value(args['М']) then
		forms['loc_sg'] = args['М']
	end
end


local function voc_case(forms, args, index, word)  -- Звательный падеж
	_.log_func('forms', 'voc_case')

	if _.has_value(args['З']) then
		forms['voc_sg'] = args['З']
	elseif _.contains(index, 'З') then
		if _.endswith(word, {'а', 'я'}) then
			forms['voc_sg'] = forms['gen_pl']
		else
			forms['error'] = 'Ошибка: Для автоматического звательного падежа, слово должно оканчиваться на -а/-я'
		end
	end
end


function export.special_cases(forms, args, index, word)
	_.log_func('forms', 'special_cases')

	prt_case(forms, args, index)
	loc_case(forms, args, index)
	voc_case(forms, args, index, word)
end


--------------------------------------------------------------------------------


function export.join_forms(forms1, forms2)
	_.log_func('forms', 'join_forms')

	local keys, forms, delim

	keys = {
		'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
		'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
		'ins_sg2',
		'зализняк1', 'зализняк',
		'error',
	}  -- list

	forms = forms1
	forms['зализняк-1'] = forms1['зализняк']
	forms['зализняк-2'] = forms2['зализняк']
	for i, key in pairs(keys) do  -- list
		if not forms[key] and forms2[key] then  -- INFO: Если forms[key] == nil
			forms[key] = forms2[key]
		elseif forms[key] ~= forms2[key] and forms2[key] then
			delim = '<br/>'
			if _.equals(key, {'зализняк1', 'зализняк'}) then
				delim = '&nbsp;'
			end
			-- TODO: <br/> только для падежей
			forms[key] = forms[key] .. '&nbsp;//' .. delim .. forms2[key]
		end
		if not forms[key] then  -- INFO: Если forms[key] == nil
			forms[key] = ''
		end
	end
	return forms
end


function export.plus_forms(sub_forms)
	_.log_func('forms', 'plus_forms')

	local keys, forms, delim

	keys = {
		'nom_sg',  'gen_sg',  'dat_sg',  'acc_sg',  'ins_sg',  'prp_sg',
		'nom_pl',  'gen_pl',  'dat_pl',  'acc_pl',  'ins_pl',  'prp_pl',
		'ins_sg2',
		'зализняк1', 'зализняк',
		'error',
	}  -- list
	forms = sub_forms[1]
	for i, forms2 in pairs(sub_forms) do  -- list
		if i ~= 1 then
			for j, key in pairs(keys) do  -- list
				if not forms[key] and forms2[key] then  -- INFO: Если forms[key] == nil
					forms[key] = forms2[key]
				elseif forms[key] ~= forms2[key] and forms2[key] then
					delim = '-'
					if _.equals(key, {'зализняк1', 'зализняк'}) then
						delim = ' + '
					end
					forms[key] = forms[key] .. delim .. forms2[key]
				end
				if not forms[key] then  -- INFO: Если forms[key] == nil
					forms[key] = ''
				end
			end
		end
	end
	return forms
end


return export
