local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local degree = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/transform/degree')  -- '.'
local reducable = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/transform/reducable')  -- '.'
local adj_circles = require('Module:' .. dev_prefix .. 'inflection/ru/declension/modify/transform/circles/adj')  -- '.'


local module = 'modify.transform'


-- @starts
function export.transform(info)
	func = "transform"
	_.starts(module, func)

	local stem_stress_schema

	-- apply special cases (1) or (2) in index
	if info.adj then
		adj_circles.apply_adj_specific_1_2(info.data.stems, info.gender, info.rest_index)
	end

	--    *** для случая с расстановкой ударения  (см. ниже)
	--    local orig_stem = info.stem.unstressed
	--    if _.contains(info.rest_index, {'%(2%)', '②'}) then
	--        orig_stem = _.replaced(info.data.stems['gen_pl'], '́ ', '')  -- удаляем ударение для случая "сапожок *d(2)"
	--        mw.log('> Another `orig_stem`: ' .. tostring(orig_stem))
	--    end

	-- reducable
	info.rest_index = degree.apply_specific_degree(info.data.stems, info.data.endings, info.word.unstressed, info.stem.unstressed, info.stem.type, info.gender, info.stress_type, info.rest_index, info)
	reducable.apply_specific_reducable(info.data.stems, info.data.endings, info.word.unstressed, info.stem.unstressed, info.stem.type, info.gender, info.stress_type, info.rest_index, info, false)
	if not _.equals(info.stress_type, {"f", "f'"}) and _.contains(info.rest_index, '%*') then
		mw.log('# Обработка случая на препоследний слог основы при чередовании'); orig_stem = info.stem.unstressed
		if info.forced_stem then
			orig_stem = info.forced_stem
		end
		for key, stem in pairs(info.data.stems) do
			--            mw.log(' - ' .. key .. ' -> ' .. stem)
			--            mw.log('Ударение на основу?')
			--            mw.log(info.stress_schema['stem'][key])
			stem_stress_schema = info.stress_schema['stem']
			if not _.contains(stem, '[́ ё]') and _.has_key(stem_stress_schema[key]) and stem_stress_schema[key] then
				-- *** случай с расстановкой ударения  (см. выше)
				-- "Дополнительные правила об ударении", стр. 34
				old_value = info.data.stems[key]
				-- mw.log('> ' .. key .. ' (old): ' .. tostring(old_value))
				if info.data.stems[key] ~= orig_stem then  -- попытка обработать наличие беглой гласной (не знаю, сработает ли всегда)
					info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)({vowel})({consonant}*)$', '%1́ %2%3%4')
					if not _.contains(info.data.stems[key], '[́ ё]') then  -- если предпоследнего слога попросту нет
						-- сделаем хоть последний ударным
						info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
					end
				else
					info.data.stems[key] = _.replaced(stem, '({vowel})({consonant}*)$', '%1́ %2')
				end
				-- mw.log('> ' .. key .. ' (new): ' .. tostring(info.data.stems[key]))
				mw.log('  - [' .. key .. '] = "' .. tostring(old_value) .. '" -> "' .. tostring(info.data.stems[key]) .. '"')
			end
		end
	end

	-- Специфика по "ё"
	if _.contains(info.rest_index, 'ё') and not _.contains(info.data.endings['gen_pl'], '{vowel+ё}') and not _.contains(info.data.stems['gen_pl'], 'ё') then
		info.data.stems['gen_pl'] = _.replaced(info.data.stems['gen_pl'], 'е́?([^е]*)$', 'ё%1')
		info.rest_index = info.rest_index .. 'ё'  -- ???
	end

	_.ends(module, func)
end


return export
