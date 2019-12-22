local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'modify.prepare.stress_apply'


-- TODO: вместо "endings" может передавать просто data
-- @call
local function add_stress(endings, case)
	func = "add_stress"
	_.call(module, func)

	endings[case] = _.replaced(endings[case], '^({vowel})', '%1́ ')
end


-- @starts
function export.apply_stress_type(data)
	func = "apply_stress_type"
	_.starts(module, func)

	-- If we have "ё" specific    -- fixme: ???
	if _.contains(data.rest_index, 'ё') and data.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
		data.stem.stressed = _.replaced(data.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	end

	if data.stress_schema['stem']['sg'] then
		data.stems['nom_sg'] = data.stem.stressed
	else
		data.stems['nom_sg'] = data.stem.unstressed
		add_stress(data.endings, 'nom_sg')
	end

	-- TODO: Remove redundant duplicated code (with above)
	-- If we have "ё" specific
	-- _.log_value(data.stem.type, 'data.stem.type')
	-- if _.contains(data.rest_index, 'ё') and data.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
	--     data.stem.stressed = _.replaced(data.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	-- end

	-- TODO: process this individually !!!!
	if data.stress_schema['stem']['sg'] then
		data.stems['gen_sg'] = data.stem.stressed
		data.stems['dat_sg'] = data.stem.stressed
		data.stems['prp_sg'] = data.stem.stressed
	else
		data.stems['gen_sg'] = data.stem.unstressed
		data.stems['dat_sg'] = data.stem.unstressed
		data.stems['prp_sg'] = data.stem.unstressed
		add_stress(data.endings, 'gen_sg')
		add_stress(data.endings, 'dat_sg')
		add_stress(data.endings, 'prp_sg')
	end

	if data.stress_schema['stem']['ins_sg'] then
		data.stems['ins_sg'] = data.stem.stressed
	else
		data.stems['ins_sg'] = data.stem.unstressed
		add_stress(data.endings, 'ins_sg')
	end

	if data.gender == 'f' then
		if data.stress_schema['stem']['acc_sg'] then
			data.stems['acc_sg'] = data.stem.stressed
		else
			data.stems['acc_sg'] = data.stem.unstressed
			add_stress(data.endings, 'acc_sg')
		end
	end

	if data.stress_schema['stem']['nom_pl'] then
		data.stems['nom_pl'] = data.stem.stressed
	else
		data.stems['nom_pl'] = data.stem.unstressed
		add_stress(data.endings, 'nom_pl')
	end

	-- TODO: process this individually !!!! and just in the common loop for all cases :)
	if data.stress_schema['stem']['pl'] then
		data.stems['gen_pl'] = data.stem.stressed
		data.stems['dat_pl'] = data.stem.stressed
		data.stems['ins_pl'] = data.stem.stressed
		data.stems['prp_pl'] = data.stem.stressed
	else
		data.stems['gen_pl'] = data.stem.unstressed
		data.stems['dat_pl'] = data.stem.unstressed
		data.stems['ins_pl'] = data.stem.unstressed
		data.stems['prp_pl'] = data.stem.unstressed
		add_stress(data.endings, 'gen_pl')
		add_stress(data.endings, 'dat_pl')
		add_stress(data.endings, 'ins_pl')
		add_stress(data.endings, 'prp_pl')
	end

	if data.adj then
		data.stems['srt_sg'] = data.stem.unstressed
		data.stems['srt_pl'] = data.stem.unstressed

		if data.gender == 'm' then
			if not _.contains(data.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
				_.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
			else
				data.stems['srt_sg'] = data.stem.stressed
			end
		elseif data.gender == 'n' then
			if data.stress_schema['stem']['srt_sg_n'] then
				if not _.contains(data.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
					_.replace(data.stems, 'srt_sg', '({vowel})({consonant}*)$', '%1́ %2')
				else
					data.stems['srt_sg'] = data.stem.stressed
				end
			end
			if data.stress_schema['ending']['srt_sg_n'] then
				add_stress(data.endings, 'srt_sg')
			end
		elseif data.gender == 'f' then
			if data.stress_schema['stem']['srt_sg_f'] then
				data.stems['srt_sg'] = data.stem.stressed
			end
			if data.stress_schema['ending']['srt_sg_f'] then
				add_stress(data.endings, 'srt_sg')
			end
		end

		if data.stress_schema['stem']['srt_pl'] then
			data.stems['srt_pl'] = data.stem.stressed
		end
		if data.stress_schema['ending']['srt_pl'] then
			add_stress(data.endings, 'srt_pl')
		end
	end

	_.ends(module, func)
end


return export
