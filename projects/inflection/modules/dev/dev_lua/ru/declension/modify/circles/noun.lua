local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- constants:
local unstressed = 1
local stressed = 2
local module = 'modify.circles.noun'


-- @starts
function export.apply_noun_specific_1_2(endings, gender, stem_type, stem_base_type, rest_index)
	func = "apply_noun_specific_1_2"
	_.starts(module, func)

	if _.contains(rest_index, {'%(1%)', '①'}) then
		if stem_base_type == 'hard' then
			if gender == 'm' then endings['nom_pl'] = 'а' end
			if gender == 'n' then endings['nom_pl'] = 'ы' end
		end
		if stem_base_type == 'soft' then
			if gender == 'm' then endings['nom_pl'] = 'я' end
			if gender == 'n' then endings['nom_pl'] = 'и' end
		end
		if _.equals(stem_type, {'velar', 'sibilant'}) then  -- Replace "ы" to "и"
			if gender == 'n' then endings['nom_pl'] = 'и' end
		end
	end

	if _.contains(rest_index, {'%(2%)', '②'}) then
		if stem_base_type == 'hard' then
			if gender == 'm' then endings['gen_pl'] = {'', ''} end
			if gender == 'n' then endings['gen_pl'] = {'ов', 'ов'} end
			if gender == 'f' then endings['gen_pl'] = {'ей', 'ей' } end
		end
		if stem_base_type == 'soft' then
			if gender == 'm' then endings['gen_pl'] = {'ь', 'ь'} end
			if gender == 'n' then endings['gen_pl'] = {'ев', 'ёв'}  end
			if gender == 'f' then endings['gen_pl'] = {'ей', 'ей' } end
		end
		if _.equals(stem_type, {'sibilant', 'letter-ц'}) then  -- Replace unstressed "о" to "е"
			if gender == 'n' then endings['gen_pl'][unstressed] = 'ев' end
		end

--		-- Possibly we don't need this:
--			-- Replace "ов", "ев", "ёв" and null to "ей"
--			if stem_type = {'sibilant'}}
--				if gender == 'n' then endings['gen_pl'] = {'ей', 'ей'}
--				if gender == 'm' then endings['gen_pl'][stressed] = 'ей'
--			end
--			-- Replace "ь" to "й"
--			if stem_type = {'vowel', 'letter-и'}}
--				if gender == 'm' then endings['gen_pl'][stressed] = {'й', 'й'}
--			end
--			-- Replace "ей" to "ев/ёв", and "ь,ей" to "й"
--			if stem_type = {'vowel', 'letter-и'}}
--				if gender == 'f' then endings['gen_pl'][unstressed] = {'ев', 'ёв'}
--				if gender == 'm' then endings['gen_pl'][stressed] = {'й', 'й'}
--			end
--		--
	end

	_.ends(module, func)
end


return export
