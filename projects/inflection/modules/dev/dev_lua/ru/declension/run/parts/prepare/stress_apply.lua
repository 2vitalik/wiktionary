local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.parts.prepare.stress_apply'


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

	local p = i.parts

	-- If we have "ё" specific    -- fixme: ???
	if _.contains(i.rest_index, 'ё') and i.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
		i.stem.stressed = _.replaced(i.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	end

	if i.stress_schema['stem']['sg'] then
		p.stems['nom-sg'] = i.stem.stressed
	else
		p.stems['nom-sg'] = i.stem.unstressed
		add_stress(p.endings, 'nom-sg')
	end

	-- TODO: Remove redundant duplicated code (with above)
	-- If we have "ё" specific
	-- _.log_value(info.stem.type, 'info.stem.type')
	-- if _.contains(info.rest_index, 'ё') and info.stem.type ~= 'n-3rd' then  -- Не уверен насчёт необходимости проверки 'n-3rd' здесь, сделал для "время °"
	--     info.stem.stressed = _.replaced(info.stem.stressed, 'е́?([^е]*)$', 'ё%1')
	-- end

	-- TODO: process this individually !!!!
	if i.stress_schema['stem']['sg'] then
		p.stems['gen-sg'] = i.stem.stressed
		p.stems['dat-sg'] = i.stem.stressed
		p.stems['prp-sg'] = i.stem.stressed
	else
		p.stems['gen-sg'] = i.stem.unstressed
		p.stems['dat-sg'] = i.stem.unstressed
		p.stems['prp-sg'] = i.stem.unstressed
		add_stress(p.endings, 'gen-sg')
		add_stress(p.endings, 'dat-sg')
		add_stress(p.endings, 'prp-sg')
	end

	if i.stress_schema['stem']['ins-sg'] then
		p.stems['ins-sg'] = i.stem.stressed
	else
		p.stems['ins-sg'] = i.stem.unstressed
		add_stress(p.endings, 'ins-sg')
	end

	if i.gender == 'f' then
		if i.stress_schema['stem']['acc-sg'] then
			p.stems['acc-sg'] = i.stem.stressed
		else
			p.stems['acc-sg'] = i.stem.unstressed
			add_stress(p.endings, 'acc-sg')
		end
	end

	if i.stress_schema['stem']['nom-pl'] then
		p.stems['nom-pl'] = i.stem.stressed
	else
		p.stems['nom-pl'] = i.stem.unstressed
		add_stress(p.endings, 'nom-pl')
	end

	-- TODO: process this individually !!!! and just in the common loop for all cases :)
	if i.stress_schema['stem']['pl'] then
		p.stems['gen-pl'] = i.stem.stressed
		p.stems['dat-pl'] = i.stem.stressed
		p.stems['ins-pl'] = i.stem.stressed
		p.stems['prp-pl'] = i.stem.stressed
	else
		p.stems['gen-pl'] = i.stem.unstressed
		p.stems['dat-pl'] = i.stem.unstressed
		p.stems['ins-pl'] = i.stem.unstressed
		p.stems['prp-pl'] = i.stem.unstressed
		add_stress(p.endings, 'gen-pl')
		add_stress(p.endings, 'dat-pl')
		add_stress(p.endings, 'ins-pl')
		add_stress(p.endings, 'prp-pl')
	end

	if i.adj then
		p.stems['srt-sg'] = i.stem.unstressed
		p.stems['srt-pl'] = i.stem.unstressed

		if i.gender == 'm' then
			if not _.contains(i.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
				_.replace(p.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
			else
				p.stems['srt-sg'] = i.stem.stressed
			end
		elseif i.gender == 'n' then
			if i.stress_schema['stem']['srt-sg-n'] then
				if not _.contains(i.stem.stressed, '[ ́ё]') then  -- todo: возможно мы должны также менять stem.stressed изначально?
					_.replace(p.stems, 'srt-sg', '({vowel})({consonant}*)$', '%1́ %2')
				else
					p.stems['srt-sg'] = i.stem.stressed
				end
			end
			if i.stress_schema['ending']['srt-sg-n'] then
				add_stress(p.endings, 'srt-sg')
			end
		elseif i.gender == 'f' then
			if i.stress_schema['stem']['srt-sg-f'] then
				p.stems['srt-sg'] = i.stem.stressed
			end
			if i.stress_schema['ending']['srt-sg-f'] then
				add_stress(p.endings, 'srt-sg')
			end
		end

		if i.stress_schema['stem']['srt-pl'] then
			p.stems['srt-pl'] = i.stem.stressed
		end
		if i.stress_schema['ending']['srt-pl'] then
			add_stress(p.endings, 'srt-pl')
		end
	end

	_.ends(module, func)
end


return export
