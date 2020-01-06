local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local degree = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/degree')  -- '..'
local reducable = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/reducable')  -- '..'
local adj_circles = require('Module:' .. dev_prefix .. 'inflection/ru/declension/run/parts/transform/circles/adj')  -- '..'


local module = 'run.parts.transform'


-- @starts
function export.transform(i)
	func = "transform"
	_.starts(module, func)

	local stem_stress_schema
	local p = i.parts

	-- apply special cases (1) or (2) in index
	if i.adj then
		adj_circles.apply_adj_specific_1_2(i)
	end

	--    *** для случая с расстановкой ударения  (см. ниже)
	--    local orig_stem = i.stem.unstressed
	--    if _.contains(i.rest_index, {'%(2%)', '②'}) then
	--        orig_stem = _.replaced(p.stems['gen-pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
	--        mw.log('> Another `orig_stem`: ' .. tostring(orig_stem))
	--    end

	-- reducable
	i.rest_index = degree.apply_specific_degree(i)
	reducable.apply_specific_reducable(i, i.gender, i.rest_index, false)
	if not _.equals(i.stress_type, {"f", "f'"}) and _.contains(i.rest_index, '%*') then
		_.log_info('Обработка случая на препоследний слог основы при чередовании')
		orig_stem = i.stem.unstressed
		if i.forced_stem then
			orig_stem = i.forced_stem
		end
		for key, stem in pairs(p.stems) do
			-- mw.log(' - ' .. key .. ' -> ' .. stem)
			-- mw.log('Ударение на основу?')
			-- mw.log(i.stress_schema['stem'][key])
			stem_stress_schema = i.stress_schema['stem']
			if not _.contains(stem, '[́ ё]') and _.has_key(stem_stress_schema[key]) and stem_stress_schema[key] then
				-- *** случай с расстановкой ударения  (см. выше)
				-- "Дополнительные правила об ударении", стр. 34
				old_value = p.stems[key]
				-- mw.log('> ' .. key .. ' (old): ' .. tostring(old_value))
				if p.stems[key] ~= orig_stem then  -- попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
					p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
					if not _.contains(p.stems[key], '[́ ё]') then  -- если предпоследнего слога попросту нет
						-- сделаем хоть последний ударным
						p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
					end
				else
					p.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
				end
				-- mw.log('> ' .. key .. ' (new): ' .. tostring(p.stems[key]))
				mw.log('  - [' .. key .. '] = "' .. tostring(old_value) .. '" -> "' .. tostring(p.stems[key]) .. '"')
			end
		end
	end

	if i.calc_pl then
		-- Специфика по "ё"
		if _.contains(i.rest_index, 'ё') and not _.contains(p.endings['gen-pl'], '{vowel+ё}') and not _.contains(p.stems['gen-pl'], 'ё') then
			p.stems['gen-pl'] = _.replaced(p.stems['gen-pl'], 'е́?([^е]*)$', 'ё%1')
			i.rest_index = i.rest_index .. 'ё'  -- ???
		end
	end

	_.ends(module, func)
end


return export
