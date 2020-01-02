local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on `prod` version

local export = {}
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')


local module = 'run.result.variations'


-- @starts
function export.join_forms(out_args_1, out_args_2)  -- todo: rename to `variations`
	func = "join_forms"
	_.starts(module, func)

	local keys, out_args, delim

	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'nom-sg-m', 'gen-sg-m', 'dat-sg-m', 'acc-sg-m', 'ins-sg-m', 'prp-sg-m',
		'nom-sg-n', 'gen-sg-n', 'dat-sg-n', 'acc-sg-n', 'ins-sg-n', 'prp-sg-n',
		'nom-sg-f', 'gen-sg-f', 'dat-sg-f', 'acc-sg-f', 'ins-sg-f', 'prp-sg-f',
		'srt-sg',  'srt-sg-m',  'srt-sg-n',  'srt-sg-f',  'srt-pl',
		'acc-sg-m-a', 'acc-sg-m-n', 'acc-pl-a', 'acc-pl-n',
		'ins-sg2',
		'ins-sg2-f',
		'зализняк1', 'зализняк',
		'error',
	}  -- list

	out_args = out_args_1
	out_args['зализняк-1'] = out_args_1['зализняк']
	out_args['зализняк-2'] = out_args_2['зализняк']
	for j, key in pairs(keys) do  -- list
		if not _.has_key(out_args[key]) and not _.has_key(out_args_2[key]) then
			-- pass
		elseif not _.has_key(out_args[key]) and _.has_key(out_args_2[key]) then  -- INFO: Если out_args[key] == nil
			out_args[key] = out_args_2[key]
		elseif out_args[key] ~= out_args_2[key] and out_args_2[key] then
			delim = '<br/>'
			if _.equals(key, {'зализняк1', 'зализняк'}) then
				delim = '&nbsp;'
			end
			-- TODO: <br/> только для падежей
			out_args[key] = out_args[key] .. '&nbsp;//' .. delim .. out_args_2[key]
		end
		if not _.has_key(out_args[key]) or not out_args[key] then  -- INFO: Если out_args[key] == nil
			out_args[key] = ''
		end
	end

	return _.returns(module, func, out_args)
end


-- @starts
function export.plus_forms(sub_forms)  -- todo: rename to `out_args`
	func = "plus_forms"
	_.starts(module, func)

	local keys, out_args, delim

	keys = {
		'nom-sg',  'gen-sg',  'dat-sg',  'acc-sg',  'ins-sg',  'prp-sg',
		'nom-pl',  'gen-pl',  'dat-pl',  'acc-pl',  'ins-pl',  'prp-pl',
		'ins-sg2',
		'зализняк1', 'зализняк',
		'error',
	}  -- list
	out_args = sub_forms[1]  -- todo: rename to `out_args`
	for j, forms2 in pairs(sub_forms) do  -- list  -- todo: rename to `out_args`
		if j ~= 1 then
			for j, key in pairs(keys) do  -- list
				if not out_args[key] and forms2[key] then  -- INFO: Если out_args[key] == nil
					out_args[key] = forms2[key]
				elseif out_args[key] ~= forms2[key] and forms2[key] then
					delim = '-'
					if _.equals(key, {'зализняк1', 'зализняк'}) then
						delim = ' + '
					end
					out_args[key] = out_args[key] .. delim .. forms2[key]
				end
				if not out_args[key] then  -- INFO: Если out_args[key] == nil
					out_args[key] = ''
				end
			end
		end
	end

	return _.returns(module, func, out_args)
end


return export
