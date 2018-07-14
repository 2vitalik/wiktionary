import re

import pywikibot


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


def save_page(title, content, desc, minor=True):
    page = get_page(title)
    try:
        old_content = load_page(page)
        if old_content.strip() == content.strip():
            # todo: print or log something?
            return
    except pywikibot.NoPage:
        pass
    page.put(content, desc, minor=minor)
