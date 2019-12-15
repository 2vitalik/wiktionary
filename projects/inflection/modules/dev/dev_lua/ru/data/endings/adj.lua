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

	-- TODO: Возвращать ключи уже с дефисами вместо подчёркиваний
	return {
		m = {
			hard = {
				nom_sg = {'ый', 'ой'},
				gen_sg = 'ого',
				dat_sg = 'ому',
				ins_sg = 'ым',
				prp_sg = 'ом',
				srt_sg = '',
			},  -- dict
			soft = {
				nom_sg = 'ий',
				gen_sg = 'его',
				dat_sg = 'ему',
				ins_sg = 'им',
				prp_sg = 'ем',
				srt_sg = 'ь',
			},  -- dict
		},  -- dict
		f = {
			hard = {
				nom_sg = 'ая',
				gen_sg = 'ой',
				dat_sg = 'ой',
				acc_sg = 'ую',
				ins_sg = 'ой',
				prp_sg = 'ой',
				srt_sg = 'а',
			},  -- dict
			soft = {
				nom_sg = 'яя',
				gen_sg = 'ей',
				dat_sg = 'ей',
				acc_sg = 'юю',
				ins_sg = 'ей',
				prp_sg = 'ей',
				srt_sg = 'я',
			},  -- dict
		},  -- dict
		n = {
			hard = {
				nom_sg = 'ое',
				gen_sg = 'ого',
				dat_sg = 'ому',
				ins_sg = 'ым',
				prp_sg = 'ом',
				srt_sg='о',
			},  -- dict
			soft = {
				nom_sg = 'ее',
				gen_sg = 'его',
				dat_sg = 'ему',
				ins_sg = 'им',
				prp_sg = 'ем',
				srt_sg={'е', 'ё'},
			},  -- dict
		},  -- dict
		common = {  -- common endings
			hard = {
				nom_pl = 'ые',
				gen_pl = 'ых',
				dat_pl = 'ым',
				ins_pl = 'ыми',
				prp_pl = 'ых',
				srt_pl = 'ы',
			},  -- dict
			soft = {
				nom_pl = 'ие',
				gen_pl = 'их',
				dat_pl = 'им',
				ins_pl = 'ими',
				prp_pl = 'их',
				srt_pl = 'и',
			},  -- dict
		},  -- dict
	}  -- dict
	-- todo: сразу преобразовать в дефисы
end


-- Изменение окончаний для остальных типов основ (базирующихся на первых двух)
-- @starts
function export.fix_adj_pronoun_endings(endings, gender, stem_type, stress_schema, adj, pronoun)
	func = "fix_adj_pronoun_endings"
	_.starts(module, func)

--	INFO: Replace "ы" to "и"
	if _.equals(stem_type, {'velar', 'sibilant'}) then
		if gender == 'm' then
			if adj then
				endings['nom_sg'][unstressed] = 'ий'
			end
			endings['ins_sg'] = 'им'
		end
		if gender == 'n' then
			endings['ins_sg'] = 'им'
		end

		if adj then
			endings['nom_pl'] = 'ие'
		elseif pronoun then
			endings['nom_pl'] = 'и'
		end
		endings['gen_pl'] = 'их'
		endings['dat_pl'] = 'им'
		endings['ins_pl'] = 'ими'
		endings['prp_pl'] = 'их'
		if adj then
			endings['srt_pl'] = 'и'
		end
	end

--	INFO: Replace unstressed "о" to "е"
	if _.equals(stem_type, {'sibilant', 'letter-ц'}) then
		if not stress_schema['ending']['sg'] then
			if gender == 'm' then
				if adj then
					endings['nom_sg'][stressed] = 'ей'
				end
				endings['gen_sg'] = 'его'
				endings['dat_sg'] = 'ему'
				endings['prp_sg'] = 'ем'
			end
			if gender == 'n' then
				endings['nom_sg'] = 'ее'
				endings['gen_sg'] = 'его'
				endings['dat_sg'] = 'ему'
				endings['prp_sg'] = 'ем'
			end
			if gender == 'f' then
				endings['gen_sg'] = 'ей'
				endings['dat_sg'] = 'ей'
				endings['ins_sg'] = 'ей'
				endings['prp_sg'] = 'ей'
			end
		end
		if not stress_schema['ending']['srt_sg_n'] then
			if gender == 'n' then
				if adj then
					endings['srt_sg'] = 'е'
				end
			end
		end
	end

--	INFO: Replace "ь" to "й"
	if _.equals(stem_type, {'vowel'}) then
		if gender == 'm' then
			if adj then
				endings['srt_sg'] = 'й'
			end
		end
	end

	_.ends(module, func)
end


return export
