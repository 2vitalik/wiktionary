local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'init.process.stem_type'


-- @starts
local function get_stem_base_type(stem_type)
	func = "get_stem_base_type"
	_.starts(module, func)

	local stem_base_types

--	INFO: Выбор подходящего из двух типов

--	TODO: make one big dict?

	stem_base_types = {}  -- dict
	-- hard
	stem_base_types['hard']  = 'hard'
	stem_base_types['velar'] = 'hard'
	stem_base_types['sibilant'] = 'hard'
	stem_base_types['letter-ц'] = 'hard'
	-- soft
	stem_base_types['soft']  = 'soft'
	stem_base_types['vowel'] = 'soft'
	stem_base_types['letter-и'] = 'soft'
	stem_base_types['m-3rd'] = 'soft'
	stem_base_types['f-3rd'] = 'soft'
	stem_base_types['f-3rd-sibilant'] = 'soft'
	stem_base_types['n-3rd'] = 'hard'

	_.ends(module, func)
	return stem_base_types[stem_type]
end


-- @starts
function export.get_stem_type(stem, word, gender, adj, rest_index)  -- INFO: Определение типа основы
	func = "get_stem_type"
	_.starts(module, func)

	local stem_type

	if _.endswith(stem, '[гкх]') then
		stem_type = 'velar'  -- todo: '3-velar'
	elseif _.endswith(stem, '[жчшщ]') then
		stem_type = 'sibilant'
	elseif _.endswith(stem, 'ц') then
		stem_type = 'letter-ц'
	elseif _.endswith(stem, {'[йь]', '[аоеёуыэюя]'}) then
		stem_type = 'vowel'
	elseif _.endswith(stem, 'и') then
		stem_type = 'letter-и'
	else
		if adj then
			if _.endswith(word, {'ый', 'ой', 'ая', 'ое', 'ые'}) then
				stem_type = 'hard'
			elseif _.endswith(word, {'ий', 'яя', 'ее', 'ие'}) then
				stem_type = 'soft'
			end
		elseif gender == 'm' then
			if stem == word or _.endswith(word, 'ы') then
				stem_type = 'hard'
			elseif _.endswith(word, 'путь') then
				stem_type = 'm-3rd'
			elseif _.endswith(word, 'ь') or _.endswith(word, 'и') then
				stem_type = 'soft'
			elseif _.endswith(word, 'а') then
--				data.gender = 'f'
				stem_type = 'hard'
			elseif _.endswith(word, 'я') then
--				data.gender = 'f'
				stem_type = 'soft'
			end
		elseif gender == 'f' then
			if _.endswith(word, 'а') or _.endswith(word, 'ы') then
				stem_type = 'hard'
			elseif _.endswith(word, 'я') then
				stem_type = 'soft'
			elseif _.endswith(word, 'и') and _.contains(rest_index, '2') then  -- todo: а что если нет индекса??
				stem_type = 'soft'
			elseif _.endswith(word, 'и') and _.contains(rest_index, '8') then
				stem_type = 'f-3rd'
			elseif _.endswith(word, 'ь') then  -- conflict in pl
				stem_type = 'f-3rd'
			end
		elseif gender == 'n' then
			if _.endswith(word, 'о') or _.endswith(word, 'а') then
				stem_type = 'hard'
			elseif _.endswith(word, 'мя')  or _.endswith(word, 'мена') then
				stem_type = 'n-3rd'
			elseif _.endswith(word, 'е') or _.endswith(word, 'я') then
				stem_type = 'soft'
			end
		end
	end

--	if gender == 'm' then
--		if _.endswith(word, {'а', 'я'}) then
--			data.gender = 'f'
--		end
--	end

	if gender == 'f' and stem_type == 'sibilant' and _.endswith(word, 'ь') then
		stem_type = 'f-3rd-sibilant'
	end
	if stem_type == '' then
		stem_type = 'hard'
	end

--	INFO: Выбор подходящего `stem_type` из двух базовых типов: 'hard' и 'soft'
	local stem_base_type
	stem_base_type = get_stem_base_type(stem_type)

	_.ends(module, func)
	return stem_type, stem_base_type
end

return export
