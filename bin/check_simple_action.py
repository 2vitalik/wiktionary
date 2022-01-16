import pywikibot


if __name__ == '__main__':
    print('checked2')
    site = pywikibot.Site('ru')
    page = pywikibot.Page(site, 'User:Vitalik/test11')
    page.put('test2', 'desc')
