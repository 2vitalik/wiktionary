local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


-- constants:
local unstressed, stressed
unstressed = 1
stressed = 2


-- Данные: все стандартные окончания для двух типов основ
function export.get_standard_noun_endings()
	_.log_func('endings', 'get_standard_noun_endings')

	-- TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
	return {
		m = {  -- стандартные окончания мужского рода
			hard = {
				nom_sg = '',
				gen_sg = 'а',
				dat_sg = 'у',
				ins_sg = 'ом',
				nom_pl = 'ы',
				gen_pl = {'ов', 'ов'},  -- TODO: possibly we can join them together again: m_hard_gen_pl stressed and unstressed
			},  -- dict
			soft = {
				nom_sg = 'ь',
				gen_sg = 'я',
				dat_sg = 'ю',
				ins_sg = {'ем', 'ём'},
				nom_pl = 'и',
				gen_pl = {'ей', 'ей'},
			},  -- dict
		},  -- dict
		f = {  -- стандартные окончания женского рода
			hard = {
				nom_sg = 'а',
				gen_sg = 'ы',
				dat_sg = 'е',
				acc_sg = 'у',
				ins_sg = 'ой',
				nom_pl = 'ы',
				gen_pl = {'', ''},
			},  -- dict
			soft = {
				nom_sg = 'я',
				gen_sg = 'и',
				dat_sg = {'е', 'е'},
				acc_sg = 'ю',
				ins_sg = {'ей', 'ёй'},
				nom_pl = 'и',
				gen_pl = {'ь', 'ей'},
			},  -- dict
		},  -- dict
		n = {  -- стандартные окончания среднего рода
			hard = {
				nom_sg = 'о',
				gen_sg = 'а',
				dat_sg = 'у',
				ins_sg = 'ом',
				nom_pl = 'а',
				gen_pl = {'', ''},
			},  -- dict
			soft = {
				nom_sg = 'е',  -- was: {'е', 'ё'}
				gen_sg = 'я',
				dat_sg = 'ю',
				ins_sg = {'ем', 'ём'},
				nom_pl = 'я',
				gen_pl = {'ь', 'ей'},
			},  -- dict
		},  -- dict
		common = {  -- common endings
			hard = {
				prp_sg = {'е', 'е'},
				dat_pl = 'ам',
				ins_pl = 'ами',
				prp_pl = 'ах',
			},  -- dict
			soft = {
				prp_sg = {'е', 'е'},
				dat_pl = 'ям',
				ins_pl = 'ями',
				prp_pl = 'ях',
			},  -- dict
		}  -- dict
	}  -- dict
	-- todo: сразу преобразовать в дефисы
end



-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
function export.fix_noun_endendings(endings, gender, stem_type, stress_schema)
	_.log_func('endings', 'fix_noun_endendings')

--	INFO: Replace "ы" to "и"
	if _.equals(stem_type, {'velar', 'sibilant'}) then
		if gender == 'f' then endings['gen_sg'] = 'и' end
		if gender == 'm' then endings['nom_pl'] = 'и' end
		if gender == 'f' then endings['nom_pl'] = 'и' end
	end

--	INFO: Replace unstressed "о" to "е"
	if _.equals(stem_type, {'sibilant', 'letter-ц'}) then
		if not stress_schema['ending']['nom_sg'] then
			if gender == 'n' then endings['nom_sg'] = 'е' end -- ???
		end
		if not stress_schema['ending']['ins_sg'] then
			if gender == 'm' then endings['ins_sg'] = 'ем' end
			if gender == 'n' then endings['ins_sg'] = 'ем' end
			if gender == 'f' then endings['ins_sg'] = 'ей' end
		end
		if not stress_schema['ending']['gen_pl'] then
			if gender == 'm' then endings['gen_pl'] = {'ев', 'ев'} end  -- TODO: should we change stressed value here?
		end
	end

	if _.equals(stem_type, 'sibilant') then
		-- Replace "ов", "ев", "ёв" and null to "ей"
		if gender == 'm' then endings['gen_pl'] = {'ей', 'ей'}   end
		if gender == 'n' then endings['gen_pl'][stressed] = 'ей' end
--		if gender == 'n' then endings['gen_pl'][unstressed] = '' end -- this is just don't changed
		if gender == 'f' then endings['gen_pl'][stressed] = 'ей' end
--		if gender == 'f' then endings['gen_pl'][unstressed] = '' end -- this is just don't changed
	end

--	INFO: Replace "ь" to "й"
	if _.equals(stem_type, {'vowel', 'letter-и'}) then
		if gender == 'm' then endings['nom_sg'] = 'й'             end -- ???
		if gender == 'n' then endings['gen_pl'][unstressed] = 'й' end
		if gender == 'f' then endings['gen_pl'][unstressed] = 'й' end
	end

--	INFO: Replace "ей" to "ев/ёв", and "ь,ей" to "й"
	if _.equals(stem_type, {'vowel', 'letter-и'}) then
		if gender == 'm' then endings['gen_pl'] = {'ев', 'ёв'} end
		if gender == 'n' then endings['gen_pl'] = {'й', 'й'}   end
		if gender == 'f' then endings['gen_pl'] = {'й', 'й'}   end
	end

	if _.equals(stem_type, 'letter-и') then
		if gender == 'f' then endings['dat_sg'][unstressed] = 'и' end
		endings['prp_sg'][unstressed] = 'и'
	end

	if _.equals(stem_type, 'm-3rd') then
		if gender == 'm' then endings['gen_sg'] = 'и' end
		if gender == 'm' then endings['dat_sg'] = 'и' end
		endings['prp_sg'] = {'и', 'и'}
	end

	if _.equals(stem_type, {'f-3rd', 'f-3rd-sibilant'}) then
		if gender == 'f' then endings['nom_sg'] = 'ь' end
		if gender == 'f' then endings['dat_sg'] = {'и', 'и'} end
		if gender == 'f' then endings['acc_sg'] = 'ь' end
		if gender == 'f' then endings['ins_sg'] = {'ью', 'ью'} end
		endings['prp_sg'] = {'и', 'и'}
		if gender == 'f' then endings['gen_pl'] = {'ей', 'ей'} end
	end

	if _.equals(stem_type, 'f-3rd-sibilant') then
		endings['dat_pl'] = 'ам'
		endings['ins_pl'] = 'ами'
		endings['prp_pl'] = 'ах'
	end
end


function export.apply_noun_specific_1_2(endings, gender, stem_type, base_stem_type, rest_index)
	if _.contains(rest_index, {'%(1%)', '①'}) then
		if base_stem_type == 'hard' then
			if gender == 'm' then endings['nom_pl'] = 'а' end
			if gender == 'n' then endings['nom_pl'] = 'ы' end
		end
		if base_stem_type == 'soft' then
			if gender == 'm' then endings['nom_pl'] = 'я' end
			if gender == 'n' then endings['nom_pl'] = 'и' end
		end
		if _.equals(stem_type, {'velar', 'sibilant'}) then  -- Replace "ы" to "и"
			if gender == 'n' then endings['nom_pl'] = 'и' end
		end
	end

	if _.contains(rest_index, {'%(2%)', '②'}) then
		if base_stem_type == 'hard' then
			if gender == 'm' then endings['gen_pl'] = {'', ''} end
			if gender == 'n' then endings['gen_pl'] = {'ов', 'ов'} end
			if gender == 'f' then endings['gen_pl'] = {'ей', 'ей' } end
		end
		if base_stem_type == 'soft' then
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
end


return export
