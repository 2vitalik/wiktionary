local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


module = 'output.forms.adj'


-- @starts
function export.add_comparative(i)
	func = "add_comparative"
	_.starts(module, func)

	-- todo: move to `modify` (и сделать через основы и окончания)
	local o = i.out_args

	if _.contains(i.rest_index, '~') then
		o['comparative'] = '-'
		return _.ends(module, func)
	end

	if i.stem.type == 'velar' then
		new_stem = i.stem.unstressed
		if _.endswith(new_stem, 'к') then
			new_stem = _.replaced(new_stem, 'к$', 'ч')
		elseif _.endswith(new_stem, 'г') then
			new_stem = _.replaced(new_stem, 'г$', 'ж')
		elseif _.endswith(new_stem, 'х') then
			new_stem = _.replaced(new_stem, 'х$', 'ш')
		else
			-- pass  -- todo: some error here
		end

		-- ударение на предпоследний слог:
		new_stem = _.replaced(new_stem, '({vowel})({consonant}*)$', '%1́ %2')

		o['comparative'] = new_stem .. 'е'
	else
		if _.equals(i.stress_type, {'a', 'a/a'}) then
			o['comparative'] = i.stem.stressed .. 'ее'
			o['comparative2'] = i.stem.stressed .. 'ей'
		else
			o['comparative'] = i.stem.unstressed .. 'е́е'
			o['comparative2'] = i.stem.unstressed .. 'е́й'
		end
	end

	_.ends(module, func)
end


return export
