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
function export.apply_stress_type(i)
	func = "apply_stress_type"
	_.starts(module, func)

	local d = i.data

	-- If we have "ё" specific    -- fixme: ???
	if _.contains(i.rest_index, 'ё') and i.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
		i.stem.stressed = _.replaced(i.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	end

	if i.stress_schema['stem']['sg'] then
		d.stems['nom-sg'] = i.stem.stressed
	else
		d.stems['nom-sg'] = i.stem.unstressed
		add_stress(i.data.endings, 'nom-sg')
	end

	-- TODO: Remove redundant duplicated code (with above)
	-- If we have "ё" specific
	-- _.log_value(info.stem.type, 'info.stem.type')
	-- if _.contains(info.rest_index, 'ё') and info.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
	--     info.stem.stressed = _.replaced(info.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	-- end

	-- TODO: process this individually !!!!
	if i.stress_schema['stem']['sg'] then
		d.stems['gen-sg'] = i.stem.stressed
		d.stems['dat-sg'] = i.stem.stressed
		d.stems['prp-sg'] = i.stem.stressed
	else
		d.stems['gen-sg'] = i.stem.unstressed
		d.stems['dat-sg'] = i.stem.unstressed
		d.stems['prp-sg'] = i.stem.unstressed
		add_stress(d.endings, 'gen-sg')
		add_stress(d.endings, 'dat-sg')
		add_stress(d.endings, 'prp-sg')
	end

	if i.stress_schema['stem']['ins-sg'] then
		d.stems['ins-sg'] = i.stem.stressed
	else
		d.stems['ins-sg'] = i.stem.unstressed
		add_stress(d.endings, 'ins-sg')
	end

	if i.gender == 'f' then
		if i.stress_schema['stem']['acc-sg'] then
			d.stems['acc-sg'] = i.stem.stressed
		else
			d.stems['acc-sg'] = i.stem.unstressed
			add_stress(d.endings, 'acc-sg')
		end
	end

	if i.stress_schema['stem']['nom-pl'] then
		d.stems['nom-pl'] = i.stem.stressed
	else
		d.stems['nom-pl'] = i.stem.unstressed
		add_stress(d.endings, 'nom-pl')
	end

	-- TODO: process this individually !!!! and just in the common loop for all cases :)
	if i.stress_schema['stem']['pl'] then
		d.stems['gen-pl'] = i.stem.stressed
		d.stems['dat-pl'] = i.stem.stressed
		d.stems['ins-pl'] = i.stem.stressed
		d.stems['prp-pl'] = i.stem.stressed
	else
		d.stems['gen-pl'] = i.stem.unstressed
		d.stems['dat-pl'] = i.stem.unstressed
		d.stems['ins-pl'] = i.stem.unstressed
		d.stems['prp-pl'] = i.stem.unstressed
		add_stress(d.endings, 'gen-pl')
		add_stress(d.endings, 'dat-pl')
		add_stress(d.endings, 'ins-pl')
		add_stress(d.endings, 'prp-pl')
	end

	if i.adj then
		d.stems['srt-sg'] = i.stem.unstressed
		d.stems['srt-pl'] = i.stem.unstressed

		if i.gender == 'm' then
			if not _.contains(i.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
				_.replace(d.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
			else
				d.stems['srt-sg'] = i.stem.stressed
			end
		elseif i.gender == 'n' then
			if i.stress_schema['stem']['srt-sg-n'] then
				if not _.contains(i.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
					_.replace(d.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
				else
					d.stems['srt-sg'] = i.stem.stressed
				end
			end
			if i.stress_schema['ending']['srt-sg-n'] then
				add_stress(d.endings, 'srt-sg')
			end
		elseif i.gender == 'f' then
			if i.stress_schema['stem']['srt-sg-f'] then
				d.stems['srt-sg'] = i.stem.stressed
			end
			if i.stress_schema['ending']['srt-sg-f'] then
				add_stress(d.endings, 'srt-sg')
			end
		end

		if i.stress_schema['stem']['srt-pl'] then
			d.stems['srt-pl'] = i.stem.stressed
		end
		if i.stress_schema['ending']['srt-pl'] then
			add_stress(d.endings, 'srt-pl')
		end
	end

	_.ends(module, func)
end


return export
