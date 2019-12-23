local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local adj_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/adj')  -- '..'
local pronoun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/pronoun')  -- '..'
local noun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/noun')  -- '..'
local noun_circles = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/transform/circles/noun')  -- '..'


-- constants:
local unstressed = 1
local stressed = 2
local module = 'modify.prepare.endings'


-- Схлопывание: Выбор окончаний в зависимости от рода и типа основы
-- @starts
local function get_base_endings(gender, stem_base_type, adj, pronoun)
	func = "get_base_endings"
	_.starts(module, func)

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
		keys = {'nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg', 'srt-sg'}
		for i, key in pairs(keys) do  -- list
			standard_endings['common'][stem_base_type][key] = ''
		end
		_.ends(module, func)
		return standard_endings['common'][stem_base_type]
	end

--	INFO: Заполнение из общих данных для всех родов:
	for key, value in pairs(standard_endings['common'][stem_base_type]) do
		standard_endings[gender][stem_base_type][key] = value
	end

--	INFO: Возвращение соответствующих окончаний
	_.ends(module, func)
	return standard_endings[gender][stem_base_type]
end


-- Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
-- @starts
local function choose_endings_stress(endings, gender, stem_base_type, stress_schema, adj, pronoun)
	func = "choose_endings_stress"
	_.starts(module, func)

	local stress, keys

	-- todo: we can generate one table for all genders only once at the beginning !!! and just use/load it here

	if adj then
		stress = stress_schema['ending']['nom-sg'] and stressed or unstressed

		if gender == 'm' and stem_base_type == 'hard' then
			endings['nom-sg'] = endings['nom-sg'][stress]
		end

		stress = stress_schema['ending']['srt-sg-n'] and stressed or unstressed

		if gender == 'n' and stem_base_type == 'soft' then
			endings['srt-sg'] = endings['srt-sg'][stress]
		end
	elseif pronoun then  -- TODO: может применить такой подход для всех случаев вообще?
		keys = {'nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg'}  -- list
		for i, key in pairs(keys) do  -- list
			if type(endings[key]) == 'table' then
				stress = stress_schema['ending'][key] and stressed or unstressed
				endings[key] = endings[key][stress]
			end
		end
	else
		stress = stress_schema['ending']['dat-sg'] and stressed or unstressed

		if gender == 'f' and stem_base_type == 'soft' then
			endings['dat-sg'] = endings['dat-sg'][stress]
		end

		stress = stress_schema['ending']['prp-sg'] and stressed or unstressed

		endings['prp-sg'] = endings['prp-sg'][stress]

		stress = stress_schema['ending']['ins-sg'] and stressed or unstressed

		if stem_base_type == 'soft' then
			endings['ins-sg'] = endings['ins-sg'][stress]
		end

		stress = stress_schema['ending']['gen-pl'] and stressed or unstressed

		endings['gen-pl'] = endings['gen-pl'][stress]
	end

	_.ends(module, func)
end


-- @starts
function export.get_endings(info)
	func = "get_endings"
	_.starts(module, func)

--	INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')
	local endings

	endings = get_base_endings(info.gender, info.stem.base_type, info.adj, info.pronoun)

--	INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
	if info.adj then  -- or info.pronoun
		adj_endings.fix_adj_pronoun_endings(endings, info.gender, info.stem.type, info.stress_schema, info.adj, false)
	elseif info.pronoun then
		pronoun_endings.fix_pronoun_noun_endings(endings, info.gender, info.stem.type, info.stress_schema)
	else
		noun_endings.fix_noun_endings(endings, info.gender, info.stem.type, info.stress_schema)
	end

	-- apply special cases (1) or (2) in index
	if not info.adj and not info.pronoun then  -- todo: move outside here (into `modify` package)
		noun_circles.apply_noun_specific_1_2(endings, info.gender, info.stem.type, info.stem.base_type, info.rest_index)
	end

	-- Resolve stressed/unstressed cases of endings
	choose_endings_stress(endings, info.gender, info.stem.base_type, info.stress_schema, info.adj, info.pronoun)

--	INFO: Особые случаи: `копьё с d*` и `питьё с b*`
	if info.gender == 'n' and info.stem.base_type == 'soft' and _.endswith(info.word.unstressed, 'ё') then
		endings['nom-sg'] = 'ё'
	end

	_.ends(module, func)
	return endings
end


return export