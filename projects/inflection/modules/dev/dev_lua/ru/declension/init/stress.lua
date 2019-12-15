local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local adj_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/adj')  -- '.'
local pronoun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/pronoun')  -- '.'
local noun_stress = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/stress/noun')  -- '.'


local module = 'init.stress'


-- @starts
function export.extract_stress_type(rest_index)
	func = "extract_stress_type"
	_.starts(module, func)

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
	stress_type = _.extract(rest_index, "([abcdef][′']?[′']?[/]?[abc]?[′']?[′']?)")

--	INFO: Замена особых апострофов в ударении на обычные:
	if stress_type then
		stress_type = _.replaced(stress_type, '′', "'")
	end

--	INFO: Список допустимых схем ударений:
	allowed_stress_types = {
		'a', "a'", 'b', "b'", 'c', 'd', "d'", 'e', 'f', "f'", "f''",
		'a/a', 'a/b', 'a/c', "a/a'", "a/b'", "a/c'", "a/c''",
		'b/a', 'b/b', 'b/c', "b/a'", "b/b'", "b/c'", "b/c''",
	}

--	INFO: Если ударение есть и оно не из допустимого списка -- это ошибка
	if stress_type and not _.equals(stress_type, allowed_stress_types) then
		_.ends(module, func)
		return stress_type, {error='Ошибка: Неправильная схема ударения: ' .. stress_type}  -- dict
	end

	_.ends(module, func)
	return stress_type, nil  -- INFO: `nil` здесь -- признак, что нет ошибок
end


-- @starts
function export.get_stress_schema(stress_type, adj, pronoun)  -- Пока не используется
	func = "get_stress_schema"
	_.starts(module, func)

	local result = ''
	if adj then
		result = adj_stress.get_adj_stress_schema(stress_type)
	elseif pronoun then
		result = pronoun_stress.get_pronoun_stress_schema(stress_type)
	else
		result = noun_stress.get_noun_stress_schema(stress_type)
	end

	_.ends(module, func)
	return result
end


-- TODO: вместо "endings" может передавать просто data
-- @call
local function add_stress(endings, case)
	func = "add_stress"
	_.call(module, func)

	endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
end


-- @starts
function export.apply_stress_type(data)
	func = "apply_stress_type"
	_.starts(module, func)

	-- If we have "ё" specific
	if _.contains(data.rest_index, 'ё') and data.stem_type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
		data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
	end

	if data.stress_schema['stem']['sg'] then
		data.stems['nom_sg'] = data.stem_stressed
	else
		data.stems['nom_sg'] = data.stem
		add_stress(data.endings, 'nom_sg')
	end

	-- TODO: Remove redundant duplicated code (with above)
	-- If we have "ё" specific
	-- _.log_value(data.stem_type, 'data.stem_type')
	-- if _.contains(data.rest_index, 'ё') and data.stem_type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
	--     data.stem_stressed = _.replaced(data.stem_stressed, 'е́?([^е]*)$', 'ё%1')
	-- end

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

	if data.adj then
		data.stems['srt_sg'] = data.stem
		data.stems['srt_pl'] = data.stem

		if data.gender == 'm' then
			if not _.contains(data.stem_stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem_stressed изначально?
				_.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
			else
				data.stems['srt_sg'] = data.stem_stressed
			end
		elseif data.gender == 'n' then
			if data.stress_schema['stem']['srt_sg_n'] then
				if not _.contains(data.stem_stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem_stressed изначально?
					_.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
				else
					data.stems['srt_sg'] = data.stem_stressed
				end
			end
			if data.stress_schema['ending']['srt_sg_n'] then
				add_stress(data.endings, 'srt_sg')
			end
		elseif data.gender == 'f' then
			if data.stress_schema['stem']['srt_sg_f'] then
				data.stems['srt_sg'] = data.stem_stressed
			end
			if data.stress_schema['ending']['srt_sg_f'] then
				add_stress(data.endings, 'srt_sg')
			end
		end

		if data.stress_schema['stem']['srt_pl'] then
			data.stems['srt_pl'] = data.stem_stressed
		end
		if data.stress_schema['ending']['srt_pl'] then
			add_stress(data.endings, 'srt_pl')
		end
	end

	_.ends(module, func)
end


return export
