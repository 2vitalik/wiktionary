local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'data.endings.pronoun'


-- @call
function export.get_standard_pronoun_endings()
	func = "get_standard_pronoun_endings"
	_.call(module, func)

	local e = {}  -- AttrDict
	e.m = {}  -- AttrDict
	e.f = {}  -- AttrDict
	e.n = {}  -- AttrDict
	e.common = {}  -- AttrDict
	e.m.hard = {}  -- dict
	e.m.soft = {}  -- dict
	e.f.hard = {}  -- dict
	e.f.soft = {}  -- dict
	e.n.hard = {}  -- dict
	e.n.soft = {}  -- dict
	e.common.hard = {}  -- dict
	e.common.soft = {}  -- dict
	e.m.hard['nom-sg'] = ''
	e.m.hard['gen-sg'] = 'ого'
	e.m.hard['dat-sg'] = 'ому'
	e.m.hard['ins-sg'] = 'ым'
	e.m.hard['prp-sg'] = 'ом'
	e.m.soft['nom-sg'] = 'ь'
	e.m.soft['gen-sg'] = 'его'
	e.m.soft['dat-sg'] = 'ему'
	e.m.soft['ins-sg'] = 'им'
	e.m.soft['prp-sg'] = {'ем', 'ём'}
	e.f.hard['nom-sg'] = 'а'
	e.f.hard['gen-sg'] = 'ой'
	e.f.hard['dat-sg'] = 'ой'
	e.f.hard['acc-sg'] = 'у'
	e.f.hard['ins-sg'] = 'ой'
	e.f.hard['prp-sg'] = 'ой'
	e.f.soft['nom-sg'] = 'я'
	e.f.soft['gen-sg'] = 'ей'
	e.f.soft['dat-sg'] = 'ей'
	e.f.soft['acc-sg'] = 'ю'
	e.f.soft['ins-sg'] = 'ей'
	e.f.soft['prp-sg'] = 'ей'
	e.n.hard['nom-sg'] = 'о'
	e.n.hard['gen-sg'] = 'ого'
	e.n.hard['dat-sg'] = 'ому'
	e.n.hard['ins-sg'] = 'ым'
	e.n.hard['prp-sg'] = 'ом'
	e.n.soft['nom-sg'] = {'е', 'ё'}
	e.n.soft['gen-sg'] = 'его'
	e.n.soft['dat-sg'] = 'ему'
	e.n.soft['ins-sg'] = 'им'
	e.n.soft['prp-sg'] = 'ем'
	e.common.hard['nom-pl'] = 'ы'
	e.common.hard['gen-pl'] = 'ых'
	e.common.hard['dat-pl'] = 'ым'
	e.common.hard['ins-pl'] = 'ыми'
	e.common.hard['prp-pl'] = 'ых'
	e.common.soft['nom-pl'] = 'и'
	e.common.soft['gen-pl'] = 'их'
	e.common.soft['dat-pl'] = 'им'
	e.common.soft['ins-pl'] = 'ими'
	e.common.soft['prp-pl'] = 'их'
	return e
end


-- @call
function export.get_standard_pronoun_noun_endings()
	func = "get_standard_pronoun_noun_endings"
	_.call(module, func)

	local e = {}  -- AttrDict
	e.m = {}  -- AttrDict
	e.f = {}  -- AttrDict
	e.n = {}  -- AttrDict
	e.common = {}  -- AttrDict
	e.m.hard = {}  -- dict
	e.m.soft = {}  -- dict
	e.f.hard = {}  -- dict
	e.f.soft = {}  -- dict
	e.n.hard = {}  -- dict
	e.n.soft = {}  -- dict
	e.common.hard = {}  -- dict
	e.common.soft = {}  -- dict
	e.m.hard['nom-sg'] = ''
	e.m.hard['gen-sg'] = 'а'
	e.m.hard['dat-sg'] = 'у'
	e.m.hard['ins-sg'] = 'ым'
	e.m.hard['prp-sg'] = 'е'
	e.m.soft['nom-sg'] = 'ь'
	e.m.soft['gen-sg'] = 'я'
	e.m.soft['dat-sg'] = 'ю'
	e.m.soft['ins-sg'] = 'им'
	e.m.soft['prp-sg'] = {'ем', 'ём'}
	e.f.hard['nom-sg'] = 'а'
	e.f.hard['gen-sg'] = 'а'
	e.f.hard['dat-sg'] = 'ой'
	e.f.hard['acc-sg'] = 'у'
	e.f.hard['ins-sg'] = 'ой'
	e.f.hard['prp-sg'] = 'ой'
	e.f.soft['nom-sg'] = 'я'
	e.f.soft['gen-sg'] = 'ей'
	e.f.soft['dat-sg'] = 'ей'
	e.f.soft['acc-sg'] = 'ю'
	e.f.soft['ins-sg'] = 'ей'
	e.f.soft['prp-sg'] = 'ей'
	e.n.hard['nom-sg'] = 'о'
	e.n.hard['gen-sg'] = 'а'
	e.n.hard['dat-sg'] = 'у'
	e.n.hard['ins-sg'] = 'ым'
	e.n.hard['prp-sg'] = 'е'
	e.n.soft['nom-sg'] = {'е', 'ё'}
	e.n.soft['gen-sg'] = 'я'
	e.n.soft['dat-sg'] = 'ю'
	e.n.soft['ins-sg'] = 'им'
	e.n.soft['prp-sg'] = {'ем', 'ём'}
	e.common.hard['nom-pl'] = 'ы'
	e.common.hard['gen-pl'] = 'ых'
	e.common.hard['dat-pl'] = 'ым'
	e.common.hard['ins-pl'] = 'ыми'
	e.common.hard['prp-pl'] = 'ых'
	e.common.soft['nom-pl'] = 'и'
	e.common.soft['gen-pl'] = 'их'
	e.common.soft['dat-pl'] = 'им'
	e.common.soft['ins-pl'] = 'ими'
	e.common.soft['prp-pl'] = 'их'
	return e
end


-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
-- @starts
function export.fix_pronoun_noun_endings(endings, gender, stem_type, stress_schema)
	func = "fix_pronoun_noun_endings"
	_.starts(module, func)

--	INFO: Replace "ы" to "и"
	if _.equals(stem_type, {'sibilant'}) then
		if _.In(gender, {'m', 'n'}) then
			endings['ins-sg'] = 'им'
		end

		endings['nom-pl'] = 'и'
		endings['gen-pl'] = 'их'
		endings['dat-pl'] = 'им'
		endings['ins-pl'] = 'ими'
		endings['prp-pl'] = 'их'
	end

--	INFO: Other Replace
	if _.equals(stem_type, {'sibilant'}) then
		if gender == 'n' then
			endings['nom-sg'] = {'е', 'о' }
		end
		if _.In(gender, {'m', 'n'}) then
			endings['gen-sg'] = {'его', 'ого'}
			endings['dat-sg'] = {'ему', 'ому'}
			endings['prp-sg'] = {'ем', 'ом'}
		end
		if gender == 'f' then
			endings['gen-sg'] = {'ей', 'ой'}
			endings['dat-sg'] = {'ей', 'ой'}
			endings['ins-sg'] = {'ей', 'ой'}
			endings['prp-sg'] = {'ей', 'ой'}
		end
	end

	if _.equals(stem_type, {'vowel'}) then
		if _.In(gender, {'m', 'n'}) then
			endings['gen-sg'] = 'его'
			endings['dat-sg'] = 'ему'
		end
	end

	_.ends(module, func)
end


return export
