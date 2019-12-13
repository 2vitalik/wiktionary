local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'pronoun.endings'


-- @call
function export.get_standard_pronoun_endings()
	func = "get_standard_pronoun_endings"
	_.call(module, func)

	-- TODO: Пока что не используется

	-- TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
	return {
		m = {
			hard = {
				nom_sg = '',
				gen_sg = 'ого',
				dat_sg = 'ому',
				ins_sg = 'ым',
				prp_sg = 'ом',
			},  -- dict
			soft = {
				nom_sg = 'ь',
				gen_sg = 'его',
				dat_sg = 'ему',
				ins_sg = 'им',
				prp_sg = {'ем', 'ём'},
			},  -- dict
		},  -- dict
		f = {
			hard = {
				nom_sg = 'а',
				gen_sg = 'ой',
				dat_sg = 'ой',
				acc_sg = 'у',
				ins_sg = 'ой',
				prp_sg = 'ой',
			},  -- dict
			soft = {
				nom_sg = 'я',
				gen_sg = 'ей',
				dat_sg = 'ей',
				acc_sg = 'ю',
				ins_sg = 'ей',
				prp_sg = 'ей',
			},  -- dict
		},  -- dict
		n = {
			hard = {
				nom_sg = 'о',
				gen_sg = 'ого',
				dat_sg = 'ому',
				ins_sg = 'ым',
				prp_sg = 'ом',
			},  -- dict
			soft = {
				nom_sg = {'е', 'ё'},
				gen_sg = 'его',
				dat_sg = 'ему',
				ins_sg = 'им',
				prp_sg = 'ем',
			},  -- dict
		},  -- dict
		common = {  -- common endings
			hard = {
				nom_pl = 'ы',
				gen_pl = 'ых',
				dat_pl = 'ым',
				ins_pl = 'ыми',
				prp_pl = 'ых',
			},  -- dict
			soft = {
				nom_pl = 'и',
				gen_pl = 'их',
				dat_pl = 'им',
				ins_pl = 'ими',
				prp_pl = 'их',
			},  -- dict
		},  -- dict
	}  -- dict
	-- todo: сразу преобразовать в дефисы
end


-- @call
function export.get_standard_pronoun_noun_endings()
	func = "get_standard_pronoun_noun_endings"
	_.call(module, func)

	-- TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
	return {
		m = {
			hard = {
				nom_sg = '',
				gen_sg = 'а',
				dat_sg = 'у',
				ins_sg = 'ым',
				prp_sg = 'е',
			},  -- dict
			soft = {
				nom_sg = 'ь',
				gen_sg = 'я',
				dat_sg = 'ю',
				ins_sg = 'им',
				prp_sg = {'ем', 'ём'},
			},  -- dict
		},  -- dict
		f = {
			hard = {
				nom_sg = 'а',
				gen_sg = 'а',
				dat_sg = 'ой',
				acc_sg = 'у',
				ins_sg = 'ой',
				prp_sg = 'ой',
			},  -- dict
			soft = {
				nom_sg = 'я',
				gen_sg = 'ей',
				dat_sg = 'ей',
				acc_sg = 'ю',
				ins_sg = 'ей',
				prp_sg = 'ей',
			},  -- dict
		},  -- dict
		n = {
			hard = {
				nom_sg = 'о',
				gen_sg = 'а',
				dat_sg = 'у',
				ins_sg = 'ым',
				prp_sg = 'е',
			},  -- dict
			soft = {
				nom_sg = {'е', 'ё'},
				gen_sg = 'я',
				dat_sg = 'ю',
				ins_sg = 'им',
				prp_sg = {'ем', 'ём'},
			},  -- dict
		},  -- dict
		common = {  -- common endings
			hard = {
				nom_pl = 'ы',
				gen_pl = 'ых',
				dat_pl = 'ым',
				ins_pl = 'ыми',
				prp_pl = 'ых',
			},  -- dict
			soft = {
				nom_pl = 'и',
				gen_pl = 'их',
				dat_pl = 'им',
				ins_pl = 'ими',
				prp_pl = 'их',
			},  -- dict
		},  -- dict
	}  -- dict
	-- todo: сразу преобразовать в дефисы
end


-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
-- @starts
function export.fix_pronoun_noun_endings(endings, gender, stem_type, stress_schema)
	func = "fix_pronoun_noun_endings"
	_.starts(module, func)

--	INFO: Replace "ы" to "и"
	if _.equals(stem_type, {'sibilant'}) then
		if _.In(gender, {'m', 'n'}) then
			endings['ins_sg'] = 'им'
		end

		endings['nom_pl'] = 'и'
		endings['gen_pl'] = 'их'
		endings['dat_pl'] = 'им'
		endings['ins_pl'] = 'ими'
		endings['prp_pl'] = 'их'
	end

--	INFO: Other Replace
	if _.equals(stem_type, {'sibilant'}) then
		if gender == 'n' then
			endings['nom_sg'] = {'е', 'о' }
		end
		if _.In(gender, {'m', 'n'}) then
			endings['gen_sg'] = {'его', 'ого'}
			endings['dat_sg'] = {'ему', 'ому'}
			endings['prp_sg'] = {'ем', 'ом'}
		end
		if gender == 'f' then
			endings['gen_sg'] = {'ей', 'ой'}
			endings['dat_sg'] = {'ей', 'ой'}
			endings['ins_sg'] = {'ей', 'ой'}
			endings['prp_sg'] = {'ей', 'ой'}
		end
	end

	if _.equals(stem_type, {'vowel'}) then
		if _.In(gender, {'m', 'n'}) then
			endings['gen_sg'] = 'его'
			endings['dat_sg'] = 'ему'
		end
	end

	_.ends(module, func)
end


return export