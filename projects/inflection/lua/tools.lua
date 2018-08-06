local export = {}

local u = require('Module:utils')

local function trim_stress(str)
	-- remove space after stress (we put it in the code just to make visually readable sources)
	local result, count = mw.ustring.gsub(str, '́ ', '́')
	return result
end

export.stash = {}

function export.clear_stash()
	export.stash = {}
end

function export.add_stash(name, value)
	export.stash[name] = value
end

function export.apply_stash(str)
	for name, value in pairs(export.stash) do
		str = mw.ustring.gsub(str, u.escape(name), value)
	end
	return str
end

function export.replaced(str, pattern, replace_to)
	pattern = export.apply_stash(pattern)
	return mw.ustring.gsub(str, trim_stress(pattern), trim_stress(replace_to))
end

function export.replace(dict, key, pattern, replace_to)
	if key == 'all_sg' then
		local keys = {'gen_sg', 'dat_sg', 'prp_sg' }  -- without 'nom_sg', 'acc_sg' and 'ins_sg'
		for i, key in pairs(keys) do
			dict[key] = export.replaced(dict[key], pattern, replace_to)
		end
	elseif key == 'all_pl' then
		local keys = {'nom_pl', 'gen_pl', 'dat_pl', 'ins_pl', 'prp_pl' }  -- without 'acc_pl'
		for i, key in pairs(keys) do
			dict[key] = export.replaced(dict[key], pattern, replace_to)
		end
	else
		dict[key] = export.replaced(dict[key], pattern, replace_to)
	end
end

function export.extract(str, pattern)
	pattern = export.apply_stash(pattern)
	return mw.ustring.match(str, trim_stress(pattern))
end

function export.check(str, values, checker)
	if type(values) == 'string' then
		values = {values}
	end
	for i, value in pairs(values) do
		value = trim_stress(export.apply_stash(value))
		local ok =
			   checker == 'equals'           and value == str
			or checker == 'startswith'       and mw.ustring.match(str, "^" .. value) ~= nil
			or checker == 'endswith'         and mw.ustring.match(str, value .. "$") ~= nil
			or checker == 'penultimate'      and mw.ustring.match(str, value .. ".$") ~= nil
			or checker == 'contains'         and mw.ustring.match(str, value) ~= nil
			or checker == 'contains_once'    and table.getn(mw.text.split(str, value)) == 2
			or checker == 'contains_several' and table.getn(mw.text.split(str, value)) > 2
		if ok then
			return true
		end
	end
	return false
end

function export.equals(str, values)
	return export.check(str, values, 'equals')
end

function export.In(str, values)
	return export.equals(str, values)
end

function export.startswith(str, values)
	return export.check(str, values, 'startswith')
end

function export.endswith(str, values)
	return export.check(str, values, 'endswith')
end

function export.penultimate(str, values)
	return export.check(str, values, 'penultimate')
end

function export.contains(str, values)
	return export.check(str, values, 'contains')
end

function export.contains_once(str, values)
	return export.check(str, values, 'contains_once')
end

function export.contains_several(str, values)
	return export.check(str, values, 'contains_several')
end

-- TODO
--function export.log(args, ...)
--	if nil then
--		'ERROR'
--	end
--end

function export.log_table(t, name)
	mw.log('@ `' .. name .. '` values:')
	for key, value in pairs(t) do
		mw.log(' - ["' .. tostring(key) .. '"] = "' .. tostring(value) .. '"')
	end
end

function export.check2(value)
	-- just return value itself (need for python conversion scripts)
	return value
end

function export.set(value)
	-- just check if variable `value` has non-empty value
	return value and value ~= ''
end

function export.empty(value)
	return value == nil or value == ''
end

return export
