import re

import pywikibot
from pywikibot.site import Namespace as BaseNamespace


class Namespace:
    ARTICLES = BaseNamespace.MAIN
    TEMPLATE = BaseNamespace.TEMPLATE
    WIKTIONARY = BaseNamespace.PROJECT
    MODULE = 828


def get_page(title):
    site = pywikibot.Site('ru')
    return pywikibot.Page(site, title)


def load_page(title, get_redirect=True):
    page = get_page(title)
    return page.get(get_redirect=get_redirect)


def load_page_with_redirect(title):
    try:
        return load_page(title, get_redirect=False), None
    except pywikibot.IsRedirectPage:
        content = load_page(title, get_redirect=True)
        m = re.search(
            '^#(перенаправление|redirect)[:\s]*\[\[(?P<redirect>[^]]+)\]\]',
            content.strip(), re.IGNORECASE)
        if m:
            title_redirected = m.group('redirect')
            return load_page_with_redirect(title_redirected), title_redirected
        raise  # never should happen


def save_page(title, content, desc, minor=True, check_changes=True):
    if check_changes:
        try:
            old_content = load_page(title)
            if old_content.strip() == content.strip():
                print("Page content hasn't changed")  # todo: log something?
                return
        except pywikibot.NoPage:
            pass
    page = get_page(title)
    page.put(content, desc, minor=minor)
    return True
