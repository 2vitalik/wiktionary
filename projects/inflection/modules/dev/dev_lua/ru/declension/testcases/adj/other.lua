local dev_prefix = ''
dev_prefix = 'User:Vitalik/'  -- comment this on active version

local tests = require('Module:' .. dev_prefix .. 'inflection/ru/adj/testcases')

function tests:test_inflection()
	self:load('other')
end

return tests
