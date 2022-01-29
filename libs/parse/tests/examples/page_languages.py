
from libs.parse.storage_page import StoragePage

page = StoragePage('сало')

print(
    page.languages  # -> LanguagesGrouper() object
)

print(
    page.languages.all()  # -> { lang : LanguageSection, ... }
)

print(
    page.languages.all().keys()  # -> [ lang, ... ]
)

print(
    list(page.languages.last_list())  # -> [ (path, LanguageSection), ... ]
)

print(
    list(page.languages)  # -> [ (path, LanguageSection), ... ]
)
