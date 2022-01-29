from libs.parse.storage_page import StoragePage

page = StoragePage('сало')

print(f'page.title: "{page.title}"')
print(f'page.is_redirect: "{page.is_redirect}"')
print(f'page.is_category: "{page.is_category}"')
print(f'page.is_template: "{page.is_template}"')

# print()
# print(f'page.content:\n{page.content}')
