from libs.parse.storage_page import StoragePage

page = StoragePage('коса')

print(
    page.homonyms
)

print(
    page.homonyms.all()  # -> { path : HomonymSection, ... }
)

print(
    list(page.homonyms.all().keys())  # -> [ path, ... ]
)

print(
    list(page.homonyms.all().values())  # -> [ HomonymSection, ... ]
)

print(
    list(page.homonyms.last_list())  # -> [ HomonymSection, ... ]
)

print(
    list(page.homonyms)  # -> [ HomonymSection, ... ]
)

print([
    homonym.path
    for homonym in list(page.homonyms)  # -> [ path, ... ]
])
