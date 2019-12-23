local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- constants:
local unstressed = 1
local stressed = 2
local module = 'data.endings.adj'


-- Данные: все стандартные окончания для двух типов основ
-- @call
function export.get_standard_adj_endings()
	func = "get_standard_adj_endings"
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
	e.m.hard['nom-sg'] = {'ый', 'ой'}
	e.m.hard['gen-sg'] = 'ого'
	e.m.hard['dat-sg'] = 'ому'
	e.m.hard['ins-sg'] = 'ым'
	e.m.hard['prp-sg'] = 'ом'
	e.m.hard['srt-sg'] = ''
	e.m.soft['nom-sg'] = 'ий'
	e.m.soft['gen-sg'] = 'его'
	e.m.soft['dat-sg'] = 'ему'
	e.m.soft['ins-sg'] = 'им'
	e.m.soft['prp-sg'] = 'ем'
	e.m.soft['srt-sg'] = 'ь'
	e.f.hard['nom-sg'] = 'ая'
	e.f.hard['gen-sg'] = 'ой'
	e.f.hard['dat-sg'] = 'ой'
	e.f.hard['acc-sg'] = 'ую'
	e.f.hard['ins-sg'] = 'ой'
	e.f.hard['prp-sg'] = 'ой'
	e.f.hard['srt-sg'] = 'а'
	e.f.soft['nom-sg'] = 'яя'
	e.f.soft['gen-sg'] = 'ей'
	e.f.soft['dat-sg'] = 'ей'
	e.f.soft['acc-sg'] = 'юю'
	e.f.soft['ins-sg'] = 'ей'
	e.f.soft['prp-sg'] = 'ей'
	e.f.soft['srt-sg'] = 'я'
	e.n.hard['nom-sg'] = 'ое'
	e.n.hard['gen-sg'] = 'ого'
	e.n.hard['dat-sg'] = 'ому'
	e.n.hard['ins-sg'] = 'ым'
	e.n.hard['prp-sg'] = 'ом'
	e.n.hard['srt-sg'] = 'о'
	e.n.soft['nom-sg'] = 'ее'
	e.n.soft['gen-sg'] = 'его'
	e.n.soft['dat-sg'] = 'ему'
	e.n.soft['ins-sg'] = 'им'
	e.n.soft['prp-sg'] = 'ем'
	e.n.soft['srt-sg'] = {'е', 'ё'}
	e.common.hard['nom-pl'] = 'ые'
	e.common.hard['gen-pl'] = 'ых'
	e.common.hard['dat-pl'] = 'ым'
	e.common.hard['ins-pl'] = 'ыми'
	e.common.hard['prp-pl'] = 'ых'
	e.common.hard['srt-pl'] = 'ы'
	e.common.soft['nom-pl'] = 'ие'
	e.common.soft['gen-pl'] = 'их'
	e.common.soft['dat-pl'] = 'им'
	e.common.soft['ins-pl'] = 'ими'
	e.common.soft['prp-pl'] = 'их'
	e.common.soft['srt-pl'] = 'и'
	return e
end


-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
-- @starts
function export.fix_adj_pronoun_endings(i, pronoun)
	func = "fix_adj_pronoun_endings"
	_.starts(module, func)

	local d = i.data

--	INFO: Replace "ы" to "и"
	if _.equals(i.stem.type, {'velar', 'sibilant'}) then
		if i.gender == 'm' then
			if i.adj then
				d.endings['nom-sg'][unstressed] = 'ий'
			end
			d.endings['ins-sg'] = 'им'
		end
		if i.gender == 'n' then
			d.endings['ins-sg'] = 'им'
		end

		if i.adj then
			d.endings['nom-pl'] = 'ие'
		elseif pronoun then
			d.endings['nom-pl'] = 'и'
		end
		d.endings['gen-pl'] = 'их'
		d.endings['dat-pl'] = 'им'
		d.endings['ins-pl'] = 'ими'
		d.endings['prp-pl'] = 'их'
		if i.adj then
			d.endings['srt-pl'] = 'и'
		end
	end

--	INFO: Replace unstressed "о" to "е"
	if _.equals(i.stem.type, {'sibilant', 'letter-ц'}) then
		if not i.stress_schema['ending']['sg'] then
			if i.gender == 'm' then
				if i.adj then
					d.endings['nom-sg'][stressed] = 'ей'
				end
				d.endings['gen-sg'] = 'его'
				d.endings['dat-sg'] = 'ему'
				d.endings['prp-sg'] = 'ем'
			end
			if i.gender == 'n' then
				d.endings['nom-sg'] = 'ее'
				d.endings['gen-sg'] = 'его'
				d.endings['dat-sg'] = 'ему'
				d.endings['prp-sg'] = 'ем'
			end
			if i.gender == 'f' then
				d.endings['gen-sg'] = 'ей'
				d.endings['dat-sg'] = 'ей'
				d.endings['ins-sg'] = 'ей'
				d.endings['prp-sg'] = 'ей'
			end
		end
		if not i.stress_schema['ending']['srt-sg-n'] then
			if i.gender == 'n' then
				if i.adj then
					d.endings['srt-sg'] = 'е'
				end
			end
		end
	end

--	INFO: Replace "ь" to "й"
	if _.equals(i.stem.type, {'vowel'}) then
		if i.gender == 'm' then
			if i.adj then
				d.endings['srt-sg'] = 'й'
			end
		end
	end

	_.ends(module, func)
end


return export
