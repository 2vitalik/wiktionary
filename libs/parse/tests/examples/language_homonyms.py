
from libs.parse.storage_page import StoragePage

page = StoragePage('коса')

print(
    page.ru.homonyms
)

print(
    page.ru.homonyms.all()  # -> { header : HomonymSection, ... }
)

print(
    page.ru.homonyms.all().keys()  # -> [ header, ... ]
)

print(
    list(page.ru.homonyms.last_list())  # -> [ HomonymSection, ... ]
)

print(
    list(page.ru.homonyms)  # -> [ HomonymSection, ... ]
)
