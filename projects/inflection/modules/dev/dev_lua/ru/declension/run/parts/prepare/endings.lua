local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- from shared_utils.io.json import json_load
local noun_circles = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/circles/noun')  -- '...'


-- constants:
local unstressed = 1
local stressed = 2
local module = 'run.parts.prepare.endings'


-- Схлопывание: Выбор окончания среди двух вариантов в зависимости от схемы ударения
-- @starts
local function choose_endings_stress(i)
	func = "choose_endings_stress"
	_.starts(module, func)

	local p = i.parts

	local keys = {
		'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg',  -- 'srt-sg',
		'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl',  -- 'srt-pl',
	}  -- list
	for j, key in pairs(keys) do  -- list
		if _.has_key(p.endings[key]) and type(p.endings[key]) == 'table' then  -- type
			local stress = i.stress_schema['ending'][key] and stressed or unstressed
			p.endings[key] = p.endings[key][stress]
		end
	end

	if i.adj and i.gender == 'n' then
		local stress = i.stress_schema['ending']['srt-sg-n'] and stressed or unstressed
		p.endings['srt-sg'] = p.endings['srt-sg'][stress]
	end

	_.ends(module, func)
end


-- @starts
function export.get_endings(i)
	func = "get_endings"
	_.starts(module, func)

--	INFO: Выбор базовых окончаний по роду и типу основы ('1-hard' или '2-soft')

	local p = i.parts

	unit = ''  -- todo: get from i.unit ?
	if i.adj then
		unit = 'adj'
	elseif i.pronoun then
		unit = 'pronoun'
	else
		unit = 'noun'
	end
	_.log_value(unit, 'unit')
	_.log_value(i.unit, 'i.unit')

	all_endings = mw.loadData('Module:' .. dev_prefix .. 'inflection/ru/declension/data/endings/' .. unit)
	local endings = all_endings[i.gender][i.stem.type]

	-- клонирование окончаний
	-- через mw.clone не работает, ошибка: "table from mw.loadData is read-only"
	p.endings = {}  -- dict
	local keys = {
		'nom-sg', 'gen-sg', 'dat-sg', 'acc-sg', 'ins-sg', 'prp-sg', 'srt-sg',
		'nom-pl', 'gen-pl', 'dat-pl', 'acc-pl', 'ins-pl', 'prp-pl', 'srt-pl',
	}  -- list
	for j, key in pairs(keys) do  -- list
		if _.has_key(endings[key]) then
			p.endings[key] = endings[key]
		end
	end

	-- стр. 29: для 8-го типа склонения:
	-- после шипящих `я` в окончаниях существительных заменяется на `а`
	if i.stem_type == '8-third' and _.endswith(i.stem.unstressed, '[жчшщ]') then
		p.endings['dat-pl'] = 'ам'
		p.endings['ins-pl'] = 'ами'
		p.endings['prp-pl'] = 'ах'
	end

	-- apply special cases (1) or (2) in index
	if not i.adj and not i.pronoun then  -- todo: move outside here (into `modify` package)
		noun_circles.apply_noun_specific_1_2(i)
	end

	-- Resolve stressed/unstressed cases of endings
	choose_endings_stress(i)

--	INFO: Особые случаи: `копьё с d*` и `питьё с b*`
	if i.gender == 'n' and i.stem.base_type == '2-soft' and _.endswith(i.word.unstressed, 'ё') then
		p.endings['nom-sg'] = 'ё'
	end

	_.ends(module, func)
end


return export
