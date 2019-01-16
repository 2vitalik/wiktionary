local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local function get_base_stem_type(stem_type)
	local change_stem_type

--	INFO: Выбор подходящего из двух типов
	change_stem_type = {}  -- dict
	-- hard
	change_stem_type['hard']  = 'hard'
	change_stem_type['velar'] = 'hard'
	change_stem_type['sibilant'] = 'hard'
	change_stem_type['letter-ц'] = 'hard'
	-- soft
	change_stem_type['soft']  = 'soft'
	change_stem_type['vowel'] = 'soft'
	change_stem_type['letter-и'] = 'soft'
	change_stem_type['m-3rd'] = 'soft'
	change_stem_type['f-3rd'] = 'soft'
	change_stem_type['f-3rd-sibilant'] = 'soft'
	change_stem_type['n-3rd'] = 'hard'
	return change_stem_type[stem_type]
end


function export.get_stem_type(stem, word, gender, adj)  -- INFO: Определение типа основы
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
			elseif _.endswith(word, 'я') or _.endswith(word, 'и') then
				stem_type = 'soft'
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
	local base_stem_type
	base_stem_type = get_base_stem_type(stem_type)

	return stem_type, base_stem_type
end

return export
