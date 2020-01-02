local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.forms.common'


-- @starts
function export.fix_stress(o)
	func = "fix_stress"
	_.starts(module, func)

	-- Add stress if there is no one
	if _.contains_several(o['nom-sg'], '{vowel}') and not _.contains(o['nom-sg'], '[́ ё]') then
		-- perhaps this is redundant for nom-sg?
		_.replace(o, 'nom-sg', '({vowel})({consonant}*)$', '%1́ %2')
	end
	if _.contains_several(o['gen-pl'], '{vowel+ё}') and not _.contains(o['gen-pl'], '[́ ё]') then
		_.replace(o, 'gen-pl', '({vowel})({consonant}*)$', '%1́ %2')
	end

	_.ends(module, func)
end


-- Выбор винительного падежа
-- @starts
function export.choose_accusative_forms(i)
	func = "choose_accusative_forms"
	_.starts(module, func)

	local p = i.parts
	local r = i.result

	r['acc-sg-in'] = ''
	r['acc-sg-an'] = ''
	r['acc-pl-in'] = ''
	r['acc-pl-an'] = ''

	if i.gender == 'm' or (i.gender == 'n' and i.output_gender == 'm') then
		if i.animacy == 'in' then
			r['acc-sg'] = r['nom-sg']
		elseif i.animacy == 'an' then
			r['acc-sg'] = r['gen-sg']
		else
			r['acc-sg-in'] = r['nom-sg']
			r['acc-sg-an'] = r['gen-sg']
		end
	elseif i.gender == 'f' then
		if _.equals(i.stem.type, {'f-3rd', 'f-3rd-sibilant'}) then
			r['acc-sg'] = r['nom-sg']
		else
			r['acc-sg'] = p.stems['acc-sg'] .. p.endings['acc-sg']  -- todo: don't use `data` here?
		end
	elseif i.gender == 'n' then
		r['acc-sg'] = r['nom-sg']
	end

	if i.animacy == 'in' then
		r['acc-pl'] = r['nom-pl']
	elseif i.animacy == 'an' then
		r['acc-pl'] = r['gen-pl']
	else
		r['acc-pl-in'] = r['nom-pl']
		r['acc-pl-an'] = r['gen-pl']
	end

	_.ends(module, func)
end


-- @starts
function export.second_ins_case(i)
	func = "second_ins_case"
	_.starts(module, func)

	local r = i.result

	-- Второй творительный
	if i.gender == 'f' then
		local ins_sg2 = _.replaced(r['ins-sg'], 'й$', 'ю')
		if ins_sg2 ~= r['ins-sg'] then
			r['ins-sg2'] = ins_sg2
		end
	end

	_.ends(module, func)
end


return export
