local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.forms.init'


-- @call
function export.init_forms(i)  -- Генерация словоформ
	func = "init_forms"
	_.call(module, func)

	local r = i.result
	local p = i.parts

	if i.calc_sg then
		r['nom-sg'] = p.stems['nom-sg'] .. p.endings['nom-sg']
		r['gen-sg'] = p.stems['gen-sg'] .. p.endings['gen-sg']
		r['dat-sg'] = p.stems['dat-sg'] .. p.endings['dat-sg']
		r['acc-sg'] = ''
		r['ins-sg'] = p.stems['ins-sg'] .. p.endings['ins-sg']
		r['prp-sg'] = p.stems['prp-sg'] .. p.endings['prp-sg']
	end

	if i.calc_pl then
		r['nom-pl'] = p.stems['nom-pl'] .. p.endings['nom-pl']
		r['gen-pl'] = p.stems['gen-pl'] .. p.endings['gen-pl']
		r['dat-pl'] = p.stems['dat-pl'] .. p.endings['dat-pl']
		r['acc-pl'] = ''
		r['ins-pl'] = p.stems['ins-pl'] .. p.endings['ins-pl']
		r['prp-pl'] = p.stems['prp-pl'] .. p.endings['prp-pl']
	end
end


-- @starts
function export.init_srt_forms(i)  -- todo move to `init_forms` (with if i.adj) ?
	func = "init_srt_forms"
	_.starts(module, func)

	local p = i.parts
	local r = i.result

	if i.calc_sg then
		r['srt-sg'] = p.stems['srt-sg'] .. p.endings['srt-sg']
	end
	if i.calc_pl then
		r['srt-pl'] = p.stems['srt-pl'] .. p.endings['srt-pl']
	end
	_.ends(module, func)
end


return export
