local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- constants:
local unstressed = 1
local stressed = 2
local module = 'run.parts.transform.circles.noun'


-- @starts
function export.apply_noun_specific_1_2(i)
	func = "apply_noun_specific_1_2"
	_.starts(module, func)

	local p = i.parts

	if _.contains(i.rest_index, {'%(1%)', '①'}) then
		if i.stem.base_type == '1-hard' then
			if i.gender == 'm' then p.endings['nom-pl'] = 'а' end
			if i.gender == 'n' then p.endings['nom-pl'] = 'ы' end
		end
		if i.stem.base_type == '2-soft' then
			if i.gender == 'm' then p.endings['nom-pl'] = 'я' end
			if i.gender == 'n' then p.endings['nom-pl'] = 'и' end
		end
		if _.equals(i.stem.type, {'3-velar', '4-sibilant'}) then  -- Replace "ы" to "и"
			if i.gender == 'n' then p.endings['nom-pl'] = 'и' end
		end
	end

	if _.contains(i.rest_index, {'%(2%)', '②'}) then
		if i.stem.base_type == '1-hard' then
			if i.gender == 'm' then p.endings['gen-pl'] = {'', ''} end
			if i.gender == 'n' then p.endings['gen-pl'] = {'ов', 'ов'} end
			if i.gender == 'f' then p.endings['gen-pl'] = {'ей', 'ей' } end
		end
		if i.stem.base_type == '2-soft' then
			if i.gender == 'm' then p.endings['gen-pl'] = {'ь', 'ь'} end
			if i.gender == 'n' then p.endings['gen-pl'] = {'ев', 'ёв'}  end
			if i.gender == 'f' then p.endings['gen-pl'] = {'ей', 'ей' } end
		end
		if _.equals(i.stem.type, {'4-sibilant', '5-letter-ц'}) then  -- Replace unstressed "о" to "е"
			if i.gender == 'n' then p.endings['gen-pl'][unstressed] = 'ев' end
		end

--		-- Possibly we don't need this:
--			-- Replace "ов", "ев", "ёв" and null to "ей"
--			if i.stem.type = {'4-sibilant'}}
--				if i.gender == 'n' then p.endings['gen-pl'] = {'ей', 'ей'}
--				if i.gender == 'm' then p.endings['gen-pl'][stressed] = 'ей'
--			end
--			-- Replace "ь" to "й"
--			if i.stem.type = {'6-vowel', '7-letter-и'}}
--				if i.gender == 'm' then p.endings['gen-pl'][stressed] = {'й', 'й'}
--			end
--			-- Replace "ей" to "ев/ёв", and "ь,ей" to "й"
--			if i.stem.type = {'6-vowel', '7-letter-и'}}
--				if i.gender == 'f' then p.endings['gen-pl'][unstressed] = {'ев', 'ёв'}
--				if i.gender == 'm' then p.endings['gen-pl'][stressed] = {'й', 'й'}
--			end
--		--
	end

	_.ends(module, func)
end


return export
