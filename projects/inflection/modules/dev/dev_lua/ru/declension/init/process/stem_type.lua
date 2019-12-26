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
function export.get_stem_type(i)  -- INFO: Определение типа основы
	func = "get_stem_type"
	_.starts(module, func)

	local word = i.word.unstressed
	local stem = i.stem.unstressed

	i.stem.type = ''

	if _.endswith(stem, '[гкх]') then
		i.stem.type = 'velar'  -- todo: '3-velar'
	elseif _.endswith(stem, '[жчшщ]') then
		i.stem.type = 'sibilant'
	elseif _.endswith(stem, 'ц') then
		i.stem.type = 'letter-ц'
	elseif _.endswith(stem, {'[йь]', '[аоеёуыэюя]'}) then
		i.stem.type = 'vowel'
	elseif _.endswith(stem, 'и') then
		i.stem.type = 'letter-и'
	else
		if i.adj then
			if _.endswith(word, {'ый', 'ой', 'ая', 'ое', 'ые'}) then
				i.stem.type = 'hard'
			elseif _.endswith(word, {'ий', 'яя', 'ее', 'ие'}) then
				i.stem.type = 'soft'
			end
		elseif i.gender == 'm' then
			if stem == word or _.endswith(word, 'ы') then
				i.stem.type = 'hard'
			elseif _.endswith(word, 'путь') then
				i.stem.type = 'm-3rd'
			elseif _.endswith(word, 'ь') or _.endswith(word, 'и') then
				i.stem.type = 'soft'
			elseif _.endswith(word, 'а') then
--				i.gender = 'f'
				i.stem.type = 'hard'
			elseif _.endswith(word, 'я') then
--				i.gender = 'f'
				i.stem.type = 'soft'
			end
		elseif i.gender == 'f' then
			if _.endswith(word, 'а') or _.endswith(word, 'ы') then
				i.stem.type = 'hard'
			elseif _.endswith(word, 'я') then
				i.stem.type = 'soft'
			elseif _.endswith(word, 'и') and _.contains(i.rest_index, '2') then  -- todo: а что если нет индекса??
				i.stem.type = 'soft'
			elseif _.endswith(word, 'и') and _.contains(i.rest_index, '8') then
				i.stem.type = 'f-3rd'
			elseif _.endswith(word, 'ь') then  -- conflict in pl
				i.stem.type = 'f-3rd'
			end
		elseif i.gender == 'n' then
			if _.endswith(word, 'о') or _.endswith(word, 'а') then
				i.stem.type = 'hard'
			elseif _.endswith(word, 'мя')  or _.endswith(word, 'мена') then
				i.stem.type = 'n-3rd'
			elseif _.endswith(word, 'е') or _.endswith(word, 'я') then
				i.stem.type = 'soft'
			end
		end
	end

--	if gender == 'm' then
--		if _.endswith(word, {'а', 'я'}) then
--			i.gender = 'f'
--		end
--	end

	if i.gender == 'f' and i.stem.type == 'sibilant' and _.endswith(word, 'ь') then
		i.stem.type = 'f-3rd-sibilant'
	end
	if i.stem.type == '' then
		i.stem.type = 'hard'
		-- r.add_error(i, 'Неизвестный тип основы')
		-- return _.ends(module, func)
	end

--	INFO: Выбор подходящего `stem_type` из двух базовых типов: 'hard' и 'soft'
	i.stem.base_type = get_stem_base_type(i.stem.type)

	_.ends(module, func)
end

return export
