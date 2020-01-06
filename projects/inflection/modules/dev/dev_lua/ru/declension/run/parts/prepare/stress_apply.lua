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

	-- If we have "ё" specific
	if _.contains(i.rest_index, 'ё') then
		if i.gender == 'n' and i.stem.type == '8-third' then
			-- pass  -- fixme: Не уверен насчёт необходимости проверки 'n' и '8-third' здесь, сделал для "время °"
		else
			i.stem.stressed = _.replaced(i.stem.stressed, 'е́?([^е]*)$', 'ё%1')
		end
	end

	local sg_cases = {'nom-sg', 'gen-sg', 'dat-sg', 'ins-sg', 'prp-sg'}  -- list
	local pl_cases = {'nom-pl', 'gen-pl', 'dat-pl', 'ins-pl', 'prp-pl'}  -- list

	if i.calc_sg then
		for j, case in pairs(sg_cases) do  -- list
			if i.stress_schema['stem'][case] then
				p.stems[case] = i.stem.stressed
			else
				p.stems[case] = i.stem.unstressed
				add_stress(p.endings, case)
			end
		end

		if i.gender == 'f' then
			if i.stress_schema['stem']['acc-sg'] then
				p.stems['acc-sg'] = i.stem.stressed
			else
				p.stems['acc-sg'] = i.stem.unstressed
				add_stress(p.endings, 'acc-sg')
			end
		end
	end

	if i.calc_pl then
		for j, case in pairs(pl_cases) do  -- list
			if i.stress_schema['stem'][case] then
				p.stems[case] = i.stem.stressed
			else
				p.stems[case] = i.stem.unstressed
				add_stress(p.endings, case)
			end
		end
	end

	if i.adj then
		if i.calc_sg then
			p.stems['srt-sg'] = i.stem.unstressed

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
		end

		if i.calc_pl then
			p.stems['srt-pl'] = i.stem.unstressed

			if i.stress_schema['stem']['srt-pl'] then
				p.stems['srt-pl'] = i.stem.stressed
			end
			if i.stress_schema['ending']['srt-pl'] then
				add_stress(p.endings, 'srt-pl')
			end
		end
	end

	_.ends(module, func)
end


return export
