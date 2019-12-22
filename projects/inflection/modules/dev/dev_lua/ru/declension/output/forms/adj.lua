local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


module = 'output.forms.adj'


-- @starts
function export.add_comparative(out_args, rest_index, stress_type, stem_type, stem)
	func = "add_comparative"
	_.starts(module, func)

	-- todo: move to `modify` (и сделать через основы и окончания)

	if _.contains(rest_index, '~') then
		out_args['comparative'] = '-'
		return _.ends(module, func)
	end

	if stem_type == 'velar' then
		new_stem = stem.unstressed
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

		out_args['comparative'] = new_stem .. 'е'
	else
		if _.equals(stress_type, {'a', 'a/a'}) then
			out_args['comparative'] = stem.stressed .. 'ее'
			out_args['comparative2'] = stem.stressed .. 'ей'
		else
			out_args['comparative'] = stem.unstressed .. 'е́е'
			out_args['comparative2'] = stem.unstressed .. 'е́й'
		end
	end

	_.ends(module, func)
end


return export
