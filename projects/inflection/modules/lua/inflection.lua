
local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local export = {}
local u = require("Module:utils")
local wu = require("Module:wiki-utils")
local _ = require('Module:' .. dev_prefix .. 'inflection/tools')

-- Function to load corresponding unit
local function load_unit(unit_name)
	if unit_name == '' then
		return nil
	end
	return require("Module:" .. dev_prefix .. "inflection/" .. unit_name);
end

local function remove_stress(value)
	value = mw.ustring.gsub(value, '́', '')
	value = mw.ustring.gsub(value, '̀', '')
	value = mw.ustring.gsub(value, 'ѐ', 'е')
	value = mw.ustring.gsub(value, 'ѝ', 'и')
	return value
end

local function fix_args(base, args)
	-- TODO: make `for` here
	if args[1] then
		args['слово'] = args[1]
	end
	if not args['слово'] then
		args['слово'] = ''
	end
	if args[2] then
		args['индекс'] = args[2]
	end
	if not args['индекс'] then
		args['индекс'] = ''
	end
	if remove_stress(args['индекс']) == base then
		local tmp = args['индекс']
		args['индекс'] = args['слово']
		args['слово'] = tmp
	end
end

-- This export function is used from testcases
function export.test(unit_name, base, args)
	local unit = load_unit(unit_name)
	-- fix_args(args)
	return unit.forms(base, args, nil)
end

-- This export function is used from templates
function export.get(frame)
	local base = u.get_base()
	local args = frame:getParent().args
	-- res = ''
	-- for i, key in pairs(args) do
		-- res = res .. i .. ','
	-- end
	-- return args[1]
	local unit_name = frame.args['unit']
	local unit = load_unit(unit_name)
	if unit == nil then
		return 'Error: Name of unit is absent'
	end

	fix_args(base, args)

    local forms = unit.forms(base, args, frame)
    local template = unit.template(base, args)

    local output = frame:expandTemplate{title=template, args=forms }

--	output = '{{' .. template .. '\n'
--	for key, value in pairs(forms) do
--		output = output .. '|' .. key .. '=' .. value .. '\n'
--		mw.log(key .. ' => ' .. type(key))
--		mw.log(value .. ' => ' .. type(value))
--	end
--	output = output .. '}}'

    if _.set(forms['error']) then
         output = output .. '\n' .. wu.div_red(forms['error'])
    end
    if _.set(forms['error_category']) then
         output = output .. '[[Категория:' .. forms['error_category'] .. ']]'
    end

--	return frame:preprocess(output)
	return output
end

return export
