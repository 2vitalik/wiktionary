local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


function export.extract_stress_type(rest_index)
	_.log_func('stress', 'extract_stress_type')

	--    OLD: Старая версия кода:
--	local stress_regexp = "([abcdef][′']?[′']?)"
--	local stress_regexp2 = '(' .. stress_regexp .. '.*//.*' .. stress_regexp .. ')'
--	stress_regexp = '(' .. stress_regexp .. '(% ?.*))'
--	data.stress_type = _.extract(rest_index, stress_regexp2)
--	if not data.stress_type then
--		data.stress_type = _.extract(rest_index, stress_regexp)
--	end
	local stress_type, allowed_stress_types

--	INFO: Извлечение ударения из оставшейся части индекса:
	stress_type = _.extract(rest_index, "([abcdef][′']?[′']?)")

--	INFO: Замена особых апострофов в ударении на обычные:
	if stress_type then
		stress_type = _.replaced(stress_type, '′', "'")
	end

--	INFO: Список допустимых схем ударений:
	allowed_stress_types = {'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''" }

--	INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
	if stress_type and not _.equals(stress_type, allowed_stress_types) then
		return stress_type, {error='Ошибка: Неправильная схема ударения: ' .. stress_type}  -- dict
	end
	return stress_type, nil  -- INFO: `nil` здесь -- признак, что нет ошибок
end


-- Данные: ударность основы и окончания в зависимости от схемы ударения
function export.get_adj_stress_schema(stress_type)  -- INFO: Вычисление схемы ударения
	_.log_func('stress', 'get_adj_stress_schema')

	-- TODO: Пока не используется

	-- общий подход следующий:
	-- если схема среди перечисленных, значит, элемент под ударением (stressed), иначе — нет (unstressed)
	local stress_schema
	stress_schema = {  -- dict
		stem = {  -- dict
			full = _.startswith(stress_type, {"a", "a/"}),
			srt_sg_f = _.endswith(stress_type, {"/a", "/a'"}),
			srt_sg_n = _.endswith(stress_type, {"/a", "/c", "/a'", "/c'", "/c''"}),
			srt_pl = _.endswith(stress_type, {"/a", "/c", "/a'", "/b'", "/c'", "/c''"}),
		},  -- dict
		ending = {  -- dict
			full = _.startswith(stress_type, {"b", "b/"}),
			srt_sg_f = _.endswith(stress_type, {"/b", "/c", "/a'", "/b'", "/c'", "/c''"}),
			srt_sg_n = _.endswith(stress_type, {"/b", "/b'", "/c''"}),
			srt_pl = _.endswith(stress_type, {"/b", "/b'", "/c'", "/c''"}),
		},  -- dict
	}  -- dict

	types = {'stem', 'ending'}
	cases = {
		'sg', 'pl',
		'nom_sg', 'gen_sg', 'dat_sg', 'acc_sg', 'ins_sg', 'prp_sg',
		'nom_pl', 'gen_pl', 'dat_pl', 'acc_pl', 'ins_pl', 'prp_pl',
	}  -- list
	for i, type in pairs(types) do  -- list
		sg_value = stress_schema[type]['full']
		for i, case in pairs(cases) do  -- list
			stress_schema[type][case] = sg_value
		end
	end

	return stress_schema
end


function export.get_stress_schema(stress_type, adj, pronoun)  -- Пока не используется
	_.log_func('stress', 'get_stress_schema')

	if adj then
		return export.get_adj_stress_schema(stress_type)
	elseif pronoun then
		return export.get_pronoun_stress_schema(stress_type)
	else
		return export.get_noun_stress_schema(stress_type)
	end
end


-- TODO: вместо "endings" может передавать просто data
local function add_stress(endings, case)
	_.log_func('stress', 'add_stress')

	endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
end


function export.apply_stress_type(data)
	_.log_func('stress', 'apply_stress_type')

	-- If we have "ё" specific
	if _.contains(data.rest_index, 'ё') and not data.stem_type == 'n-3rd' then
		data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
	end

	if data.stress_schema['stem']['sg'] then
		data.stems['nom_sg'] = data.stem_stressed
	else
		data.stems['nom_sg'] = data.stem
		add_stress(data.endings, 'nom_sg')
	end

	-- If we have "ё" specific
	_.log_value(data.stem_type, 'data.stem_type')
	if _.contains(data.rest_index, 'ё') and data.stem_type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
		data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
	end

	-- TODO: process this individually !!!
	if data.stress_schema['stem']['sg'] then
		data.stems['gen_sg'] = data.stem_stressed
		data.stems['dat_sg'] = data.stem_stressed
		data.stems['prp_sg'] = data.stem_stressed
	else
		data.stems['gen_sg'] = data.stem
		data.stems['dat_sg'] = data.stem
		data.stems['prp_sg'] = data.stem
		add_stress(data.endings, 'gen_sg')
		add_stress(data.endings, 'dat_sg')
		add_stress(data.endings, 'prp_sg')
	end

	if data.stress_schema['stem']['ins_sg'] then
		data.stems['ins_sg'] = data.stem_stressed
	else
		data.stems['ins_sg'] = data.stem
		add_stress(data.endings, 'ins_sg')
	end

	if data.gender == 'f' then
		if data.stress_schema['stem']['acc_sg'] then
			data.stems['acc_sg'] = data.stem_stressed
		else
			data.stems['acc_sg'] = data.stem
			add_stress(data.endings, 'acc_sg')
		end
	end

	if data.stress_schema['stem']['nom_pl'] then
		data.stems['nom_pl'] = data.stem_stressed
	else
		data.stems['nom_pl'] = data.stem
		add_stress(data.endings, 'nom_pl')
	end

	if data.stress_schema['stem']['pl'] then
		data.stems['gen_pl'] = data.stem_stressed
		data.stems['dat_pl'] = data.stem_stressed
		data.stems['ins_pl'] = data.stem_stressed
		data.stems['prp_pl'] = data.stem_stressed
	else
		data.stems['gen_pl'] = data.stem
		data.stems['dat_pl'] = data.stem
		data.stems['ins_pl'] = data.stem
		data.stems['prp_pl'] = data.stem
		add_stress(data.endings, 'gen_pl')
		add_stress(data.endings, 'dat_pl')
		add_stress(data.endings, 'ins_pl')
		add_stress(data.endings, 'prp_pl')
	end
end


return export
