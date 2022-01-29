
from libs.parse.storage_page import StoragePage

page = StoragePage('коса')

print(
    page['ru']
)
print(
    page.ru
)
print(
    page.languages['ru']
)
