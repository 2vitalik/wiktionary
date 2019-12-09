local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local noun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/noun/endings')  -- '.'
local adj_endings = require('Module:' .. dev_prefix .. 'inflection/ru/adj/endings')  -- '.'
local pronoun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/pronoun/endings')  -- '.'


-- constants:
local unstressed, stressed
unstressed = 1
stressed = 2


-- Схлопывание: Выбор окончаний в зависимости от рода и типа основы
local function get_base_endings(gender, base_stem_type, adj, pronoun)
	_.log_func('endings', 'get_base_endings')

	local standard_endings, keys

--	INFO: Получение списка всех стандартных окончаний
	if adj then
		standard_endings = adj_endings.get_standard_adj_endings()
	elseif pronoun then
		standard_endings = pronoun_endings.get_standard_pronoun_noun_endings()
	else
		standard_endings = noun_endings.get_standard_noun_endings()
	end

	if adj and gender == '' then  -- INFO: Случай с множественным числом
		keys = {'nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg', 'srt_sg'}
		for i, key in pairs(keys) do  -- list
			standard_endings['common'][base_stem_type][key] = ''
		end
		return standard_endings['common'][base_stem_type]
	end

--	INFO: Заполнение из общих данных для всех родов:
	for key, value in pairs(standard_endings['common'][base_stem_type]) do
		standard_endings[gender][base_stem_type][key] = value
	end

--	INFO: Возвращение соответствующих окончаний
	return standard_endings[gender][base_stem_type]
end


-- Изменение окончаний для случаев (1), (2), (3)
local function apply_specific_1_2(endings, gender, stem_type, base_stem_type, rest_index, adj, pronoun)
	_.log_func('endings', 'apply_specific_1_2')

	if adj or pronoun then
		-- pass  -- TODO

	else
		noun_endings.apply_noun_specific_1_2(endings, gender, stem_type, base_stem_type, rest_index)
	end
end


-- Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
local function choose_endings_stress(endings, gender, base_stem_type, stress_schema, adj, pronoun)
	_.log_func('endings', 'choose_endings_stress')

	local stress

	if adj then
		stress = stress_schema['ending']['nom_sg'] and stressed or unstressed

		if gender == 'm' and base_stem_type == 'hard' then
			endings['nom_sg'] = endings['nom_sg'][stress]
		end

		stress = stress_schema['ending']['srt_sg_n'] and stressed or unstressed

		if gender == 'n' and base_stem_type == 'soft' then
			endings['srt_sg'] = endings['srt_sg'][stress]
		end
	elseif pronoun then  -- TODO: может применить такой подход для всех случаев вообще?
		local keys = {'nom_sg', 'gen_sg', 'dat_sg', 'ins_sg', 'prp_sg', 'srt_sg'}
		for i, key in pairs(keys) do
			if type(endings[key]) == 'table' then
				stress = stress_schema['ending'][key] and stressed or unstressed
				endings[key] = endings[key][stress]
			end
		end
	else
		stress = stress_schema['ending']['dat_sg'] and stressed or unstressed

		if gender == 'f' and base_stem_type == 'soft' then
			endings['dat_sg'] = endings['dat_sg'][stress]
		end

		stress = stress_schema['ending']['prp_sg'] and stressed or unstressed

		endings['prp_sg'] = endings['prp_sg'][stress]

		stress = stress_schema['ending']['ins_sg'] and stressed or unstressed

		if base_stem_type == 'soft' then
			endings['ins_sg'] = endings['ins_sg'][stress]
		end

		stress = stress_schema['ending']['gen_pl'] and stressed or unstressed

		endings['gen_pl'] = endings['gen_pl'][stress]
	end
end


function export.get_endings(data)
	_.log_func('endings', 'get_endings')

--	INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
	local endings

	endings = get_base_endings(data.gender, data.base_stem_type, data.adj, data.pronoun)

--	INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
	if data.adj then  -- or data.pronoun
		adj_endings.fix_adj_pronoun_endings(endings, data.gender, data.stem_type, data.stress_schema, data.adj, false)
	elseif data.pronoun then
		pronoun_endings.fix_pronoun_noun_endings(endings, data.gender, data.stem_type, data.stress_schema)
	else
		noun_endings.fix_noun_endendings(endings, data.gender, data.stem_type, data.stress_schema)
	end

	-- apply special cases (1) or (2) in index
	apply_specific_1_2(endings, data.gender, data.stem_type, data.base_stem_type, data.rest_index, data.adj, data.pronoun)

	-- Resolve stressed/unstressed cases of endings
	choose_endings_stress(endings, data.gender, data.base_stem_type, data.stress_schema, data.adj, data.pronoun)

--	INFO: Особые случаи: `копьё с d*` и `питьё с b*`
	if data.gender == 'n' and data.base_stem_type == 'soft' and _.endswith(data.word, 'ё') then
		endings['nom_sg'] = 'ё'
	end

	return endings
end


return export