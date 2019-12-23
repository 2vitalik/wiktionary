local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- constants:
local unstressed = 1
local stressed = 2
local module = 'data.endings.noun'


-- Данные: все стандартные окончания для двух типов основ
-- @call
function export.get_standard_noun_endings()
	func = "get_standard_noun_endings"
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
	e.m.hard['ins-sg'] = 'ом'
	e.m.hard['nom-pl'] = 'ы'
	e.m.hard['gen-pl'] = {'ов', 'ов'}  -- TODO: possibly we can join them together again: m_hard_gen_pl stressed and unstressed
	e.m.soft['nom-sg'] = 'ь'
	e.m.soft['gen-sg'] = 'я'
	e.m.soft['dat-sg'] = 'ю'
	e.m.soft['ins-sg'] = {'ем', 'ём'}
	e.m.soft['nom-pl'] = 'и'
	e.m.soft['gen-pl'] = {'ей', 'ей'}
	e.f.hard['nom-sg'] = 'а'
	e.f.hard['gen-sg'] = 'ы'
	e.f.hard['dat-sg'] = 'е'
	e.f.hard['acc-sg'] = 'у'
	e.f.hard['ins-sg'] = 'ой'
	e.f.hard['nom-pl'] = 'ы'
	e.f.hard['gen-pl'] = {'', ''}
	e.f.soft['nom-sg'] = 'я'
	e.f.soft['gen-sg'] = 'и'
	e.f.soft['dat-sg'] = {'е', 'е'}
	e.f.soft['acc-sg'] = 'ю'
	e.f.soft['ins-sg'] = {'ей', 'ёй'}
	e.f.soft['nom-pl'] = 'и'
	e.f.soft['gen-pl'] = {'ь', 'ей'}
	e.n.hard['nom-sg'] = 'о'
	e.n.hard['gen-sg'] = 'а'
	e.n.hard['dat-sg'] = 'у'
	e.n.hard['ins-sg'] = 'ом'
	e.n.hard['nom-pl'] = 'а'
	e.n.hard['gen-pl'] = {'', ''}
	e.n.soft['nom-sg'] = 'е',  -- was: {'е', 'ё'}
	e.n.soft['gen-sg'] = 'я'
	e.n.soft['dat-sg'] = 'ю'
	e.n.soft['ins-sg'] = {'ем', 'ём'}
	e.n.soft['nom-pl'] = 'я'
	e.n.soft['gen-pl'] = {'ь', 'ей'}
	e.common.hard['prp-sg'] = {'е', 'е'}
	e.common.hard['dat-pl'] = 'ам'
	e.common.hard['ins-pl'] = 'ами'
	e.common.hard['prp-pl'] = 'ах'
	e.common.soft['prp-sg'] = {'е', 'е'}
	e.common.soft['dat-pl'] = 'ям'
	e.common.soft['ins-pl'] = 'ями'
	e.common.soft['prp-pl'] = 'ях'
	return e
end


-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
-- @starts
function export.fix_noun_endings(endings, gender, stem_type, stress_schema)
	func = "fix_noun_endings"
	_.starts(module, func)

--	INFO: Replace "ы" to "и"
	if _.equals(stem_type, {'velar', 'sibilant'}) then
		if gender == 'f' then endings['gen-sg'] = 'и' end
		if gender == 'm' then endings['nom-pl'] = 'и' end
		if gender == 'f' then endings['nom-pl'] = 'и' end
	end

--	INFO: Replace unstressed "о" to "е"
	if _.equals(stem_type, {'sibilant', 'letter-ц'}) then
		if not stress_schema['ending']['nom-sg'] then
			if gender == 'n' then endings['nom-sg'] = 'е' end -- ???
		end
		if not stress_schema['ending']['ins-sg'] then
			if gender == 'm' then endings['ins-sg'] = 'ем' end
			if gender == 'n' then endings['ins-sg'] = 'ем' end
			if gender == 'f' then endings['ins-sg'] = 'ей' end
		end
		if not stress_schema['ending']['gen-pl'] then
			if gender == 'm' then endings['gen-pl'] = {'ев', 'ев'} end  -- TODO: should we change stressed value here?
		end
	end

	if _.equals(stem_type, 'sibilant') then
		-- Replace "ов", "ев", "ёв" and null to "ей"
		if gender == 'm' then endings['gen-pl'] = {'ей', 'ей'}   end
		if gender == 'n' then endings['gen-pl'][stressed] = 'ей' end
--		if gender == 'n' then endings['gen-pl'][unstressed] = '' end -- this is just don't changed
		if gender == 'f' then endings['gen-pl'][stressed] = 'ей' end
--		if gender == 'f' then endings['gen-pl'][unstressed] = '' end -- this is just don't changed
	end

--	INFO: Replace "ь" to "й"
	if _.equals(stem_type, {'vowel', 'letter-и'}) then
		if gender == 'm' then endings['nom-sg'] = 'й'             end -- ???
		if gender == 'n' then endings['gen-pl'][unstressed] = 'й' end
		if gender == 'f' then endings['gen-pl'][unstressed] = 'й' end
	end

--	INFO: Replace "ей" to "ев/ёв", and "ь,ей" to "й"
	if _.equals(stem_type, {'vowel', 'letter-и'}) then
		if gender == 'm' then endings['gen-pl'] = {'ев', 'ёв'} end
		if gender == 'n' then endings['gen-pl'] = {'й', 'й'}   end
		if gender == 'f' then endings['gen-pl'] = {'й', 'й'}   end
	end

	if _.equals(stem_type, 'letter-и') then
		if gender == 'f' then endings['dat-sg'][unstressed] = 'и' end
		endings['prp-sg'][unstressed] = 'и'
	end

	if _.equals(stem_type, 'm-3rd') then
		if gender == 'm' then endings['gen-sg'] = 'и' end
		if gender == 'm' then endings['dat-sg'] = 'и' end
		endings['prp-sg'] = {'и', 'и'}
	end

	if _.equals(stem_type, {'f-3rd', 'f-3rd-sibilant'}) then
		if gender == 'f' then endings['nom-sg'] = 'ь' end
		if gender == 'f' then endings['dat-sg'] = {'и', 'и'} end
		if gender == 'f' then endings['acc-sg'] = 'ь' end
		if gender == 'f' then endings['ins-sg'] = {'ью', 'ью'} end
		endings['prp-sg'] = {'и', 'и'}
		if gender == 'f' then endings['gen-pl'] = {'ей', 'ей'} end
	end

	if _.equals(stem_type, 'f-3rd-sibilant') then
		endings['dat-pl'] = 'ам'
		endings['ins-pl'] = 'ами'
		endings['prp-pl'] = 'ах'
	end

	_.ends(module, func)
end


return export
