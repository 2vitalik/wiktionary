local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'init.process.stem_type'


-- @starts
local function get_stem_base_type(i)
	func = "get_stem_base_type"
	_.starts(module, func)

--	INFO: Выбор подходящего из двух типов

	if _.equals(i.stem.type, {'1-hard', '3-velar', '4-sibilant', '5-letter-ц'}) then
		return _.returns(module, func, '1-hard')
	end

	if _.equals(i.stem.type, {'2-soft', '6-vowel', '7-letter-и'}) then
		return _.returns(module, func, '2-soft')
	end

	if _.equals(i.stem.type, {'8-third'}) then
		if i.gender == 'n' then
			return _.returns(module, func, '1-hard')
		end
		if i.gender == 'm' or i.gender == 'f' then
			return _.returns(module, func, '2-soft')
		end
	end

	return _.returns(module, func, '?')
end


-- @starts
function export.get_stem_type(i)  -- INFO: Определение типа основы
	func = "get_stem_type"
	_.starts(module, func)

	local word = i.word.unstressed
	local stem = i.stem.unstressed

	i.stem.type = ''

	if _.endswith(stem, '[гкх]') then
		i.stem.type = '3-velar'
	elseif _.endswith(stem, '[жчшщ]') then
		i.stem.type = '4-sibilant'
	elseif _.endswith(stem, 'ц') then
		i.stem.type = '5-letter-ц'
	elseif _.endswith(stem, {'[йь]', '[аоеёуыэюя]'}) then
		i.stem.type = '6-vowel'
	elseif _.endswith(stem, 'и') then
		i.stem.type = '7-letter-и'
	else
		if i.adj then
			if _.endswith(word, {'ый', 'ой', 'ая', 'ое', 'ые'}) then
				i.stem.type = '1-hard'
			elseif _.endswith(word, {'ий', 'яя', 'ее', 'ие'}) then
				i.stem.type = '2-soft'
			end
		elseif i.gender == 'm' then
			if stem == word or _.endswith(word, 'ы') then
				i.stem.type = '1-hard'
			elseif _.endswith(word, 'путь') then
				i.stem.type = '8-third'
			elseif _.endswith(word, 'ь') or _.endswith(word, 'и') then
				i.stem.type = '2-soft'
			elseif _.endswith(word, 'а') then
				i.stem.type = '1-hard'
				-- i.gender = 'f' ??
			elseif _.endswith(word, 'я') then
				i.stem.type = '2-soft'
				-- i.gender = 'f' ??
			end
		elseif i.gender == 'f' then
			if _.endswith(word, 'а') or _.endswith(word, 'ы') then
				i.stem.type = '1-hard'
			elseif _.endswith(word, 'я') then
				i.stem.type = '2-soft'
			elseif _.endswith(word, 'и') and _.contains(i.rest_index, '2') then  -- todo: а что если нет индекса??
				i.stem.type = '2-soft'
			elseif _.endswith(word, 'и') and _.contains(i.rest_index, '8') then
				i.stem.type = '8-third'
			elseif _.endswith(word, 'ь') then  -- conflict in pl
				i.stem.type = '8-third'
			end
		elseif i.gender == 'n' then
			if _.endswith(word, 'о') or _.endswith(word, 'а') then
				i.stem.type = '1-hard'
			elseif _.endswith(word, 'мя') or _.endswith(word, 'мена') then
				i.stem.type = '8-third'
			elseif _.endswith(word, 'е') or _.endswith(word, 'я') then
				i.stem.type = '2-soft'
			end
		end
	end

--	if gender == 'm' then
--		if _.endswith(word, {'а', 'я'}) then
--			i.gender = 'f'
--		end
--	end

	if i.gender == 'f' and i.stem.type == '4-sibilant' and _.endswith(word, 'ь') then
		i.stem.type = '8-third'
	end
	if i.stem.type == '' then
		i.stem.type = '1-hard'
		-- e.add_error(i, 'Неизвестный тип основы')  -- fixme ?
		-- return _.ends(module, func)
	end

--	INFO: Выбор подходящего `stem_type` из двух базовых типов: '1-hard' и '2-soft'
	i.stem.base_type = get_stem_base_type(i)

	_.ends(module, func)
end

return export
