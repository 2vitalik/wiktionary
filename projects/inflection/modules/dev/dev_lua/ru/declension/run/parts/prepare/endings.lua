local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local adj_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/adj')  -- '...'
local pronoun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/pronoun')  -- '...'
local noun_endings = require('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/noun')  -- '...'
local noun_circles = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/circles/noun')  -- '...'


-- constants:
local unstressed = 1
local stressed = 2
local module = 'run.parts.prepare.endings'


-- Схлопывание: Выбор окончаний в зависимости от рода и типа основы
-- @starts
local function get_base_endings(i)
	func = "get_base_endings"
	_.starts(module, func)

	local standard_endings, keys

--	INFO: Получение списка всех стандартных окончаний
	if i.adj then
		standard_endings = adj_endings.get_standard_adj_endings()
	elseif i.pronoun then
		standard_endings = pronoun_endings.get_standard_pronoun_noun_endings()
	else
		standard_endings = noun_endings.get_standard_noun_endings()
	end

	if i.adj and i.gender == '' then  -- INFO: Случай с множественным числом
		keys = {'nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg', 'srt-sg'}
		for j, key in pairs(keys) do  -- list
			standard_endings['common'][i.stem.base_type][key] = ''
		end
		return _.returns(module, func, standard_endings['common'][i.stem.base_type])
	end

--	INFO: Заполнение из общих данных для всех родов:
	for key, value in pairs(standard_endings['common'][i.stem.base_type]) do
		standard_endings[i.gender][i.stem.base_type][key] = value
	end

--	INFO: Возвращение соответствующих окончаний
	return _.returns(module, func, standard_endings[i.gender][i.stem.base_type])
end


-- Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
-- @starts
local function choose_endings_stress(i)
	func = "choose_endings_stress"
	_.starts(module, func)

	local stress
	local p = i.parts

	-- todo: we can generate one table for all genders only once at the beginning !!! and just use/load it here

	if i.adj then
		stress = i.stress_schema['ending']['nom-sg'] and stressed or unstressed

		if i.gender == 'm' and i.stem.base_type == 'hard' then
			p.endings['nom-sg'] = p.endings['nom-sg'][stress]
		end

		stress = i.stress_schema['ending']['srt-sg-n'] and stressed or unstressed

		if i.gender == 'n' and i.stem.base_type == 'soft' then
			p.endings['srt-sg'] = p.endings['srt-sg'][stress]
		end
	elseif i.pronoun then  -- TODO: может применить такой подход для всех случаев вообще?
		local keys = {'nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg'}  -- list
		for j, key in pairs(keys) do  -- list
			if type(p.endings[key]) == 'table' then
				stress = i.stress_schema['ending'][key] and stressed or unstressed
				p.endings[key] = p.endings[key][stress]
			end
		end
	else
		stress = i.stress_schema['ending']['dat-sg'] and stressed or unstressed

		if i.gender == 'f' and i.stem.base_type == 'soft' then
			p.endings['dat-sg'] = p.endings['dat-sg'][stress]
		end

		stress = i.stress_schema['ending']['prp-sg'] and stressed or unstressed

		p.endings['prp-sg'] = p.endings['prp-sg'][stress]

		stress = i.stress_schema['ending']['ins-sg'] and stressed or unstressed

		if i.stem.base_type == 'soft' then
			p.endings['ins-sg'] = p.endings['ins-sg'][stress]
		end

		stress = i.stress_schema['ending']['gen-pl'] and stressed or unstressed

		p.endings['gen-pl'] = p.endings['gen-pl'][stress]
	end

	_.ends(module, func)
end


-- @starts
function export.get_endings(i)
	func = "get_endings"
	_.starts(module, func)

--	INFO: Выбор базовых окончаний по роду и типу основы ('hard' или 'soft')

	local p = i.parts

	p.endings = get_base_endings(i)

--	INFO: Изменение окончаний для нестандартного типов основы ('velar', 'sibilant', 'vowel' и т.п.)
	if i.adj then  -- or i.pronoun
		adj_endings.fix_adj_pronoun_endings(i, false)
	elseif i.pronoun then
		pronoun_endings.fix_pronoun_noun_endings(i)
	else
		noun_endings.fix_noun_endings(i)
	end

	-- apply special cases (1) or (2) in index
	if not i.adj and not i.pronoun then  -- todo: move outside here (into `modify` package)
		noun_circles.apply_noun_specific_1_2(i)
	end

	-- Resolve stressed/unstressed cases of endings
	choose_endings_stress(i)

--	INFO: Особые случаи: `копьё с d*` и `питьё с b*`
	if i.gender == 'n' and i.stem.base_type == 'soft' and _.endswith(i.word.unstressed, 'ё') then
		p.endings['nom-sg'] = 'ё'
	end

	_.ends(module, func)
end


return export
