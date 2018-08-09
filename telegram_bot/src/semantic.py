import re
from os.path import join
from urllib.parse import quote_plus

import telegram
from pywikibot.exceptions import NoPage

from core.conf.conf import ROOT_PATH
from lib.parse.online_page import OnlinePage
from lib.utils.collection import chunks
from lib.utils.io import read, append
from lib.utils.wikibot import load_page_with_redirect
from telegram_bot.src.utils import send


def clear_definitions(text):  # todo: move this to some `lib`
    # удаление лишнего:
    text = text.replace('{µ(Q)}', '')
    text = re.sub('<math>[^<>]+</math>', '', text)
    text = re.sub('{{пример({{[^}]+\}\}|[^\}])*\}\}', '', text)
    text = re.sub('{{семантика({{[^}]+\}\}|[^\}])+\}\}', '', text)
    text = re.sub('{{списки семантических связей\}\}', '', text)

    text = re.sub('^\s*{{прото\|([^}]+)\}\}',
                  'общее прототипическое значение: \\1', text)

    text = text.replace('<sub>2</sub>', '₂')
    text = text.replace('<sub>3</sub>', '₃')
    text = text.replace('<sub>4</sub>', '₄')

    # замена шаблонов:
    text = re.sub('{{помета\|([^|{}]+)', '{{\\1', text)
    text = re.sub('{{итп\}\}', 'и т.п.', text)
    text = re.sub('{{итд\}\}', 'и т.д.', text)
    text = re.sub('\|[a-z_]+\}\}', '}}', text)

    # замена всех шаблонов {{...}} на {...}:
    text = text.replace('{{', '{').replace('}}', '}')

    # замены шаблонов:
    text = re.sub('{=\|([^|}]+)\}', 'то же, что \\1', text)
    text = re.sub('{=\|([^|}]+)\|([^|}]+)\}', 'то же, что \\1; \\2', text)
    text = re.sub('\s*{-\}\s*', ' — ', text)

    # ссылки [[...|...]] и [[...]]:
    text = re.sub('\[\[[^][]*\|([^][]*)\]\]', '\\1', text)
    text = re.sub('\[\[([^][]*)\]\]', '\\1', text)

    text = text.replace('<', '&lt;').replace('>', '&gt;')

    # пометы:
    text = text.replace('{п.}', '{перен.}')

    # пометы курсивом:
    text = re.sub('{([\w-]+\.)\},?', '<i>\\1</i> ', text)

    # замены шаблонов:
    text = text.replace('{as ru}', '<i>(аналогично русскому слову)</i>')

    return text.strip()


def load_languages():  # todo: move this to some `lib`
    path = join(ROOT_PATH, 'storage', 'sync', 'data', 'language-data.lua')
    content = read(path)
    languages = dict()
    """
    m["en"] = {
        name = "Английск{ий} [язык]",
        ...
    }   
    """
    entries = re.findall('m\["([^"]+)"\] *= *{\s*name *= *"([^"]+)"', content)
    for lang, name in entries:
        name = re.sub(r'\[[^]]+\]', '', name)  # removes: [язык]
        name = re.sub(r'[{}]', '', name)       # removes: {ий}
        name = re.sub(r"'[^']+'", '', name)    # removes: '...'
        languages[lang] = name.strip().lower()
    """
    m["rus"] = table.copy(m["ru"])
    """
    entries = re.findall('m\["([^"]+)"\] *= *table\.copy\(m\["([^"]+)"\]\)"',
                         content)
    for lang1, lang2 in entries:
        languages[lang1] = languages[lang2]
    return languages


languages = load_languages()


def get_content(title):
    try:
        content, title_redirect = load_page_with_redirect(title)
        return title, content, title_redirect
    except NoPage:
        # try lower case (if originally typed via mobile phone)
        lower_title = title.lower()
        if lower_title == title:  # title was already in a lower case
            return title, None, None
        lower_title, content, title_redirect = get_content(lower_title)
        if not content:
            return title, None, None
        return lower_title, content, title_redirect
        # todo: capitalize and upper cases?


def get_homonym(title):
    homonym = 1
    p = re.compile(r'\s+[\\/](?P<homonym>\d+)')
    m = p.search(title)
    if m:
        homonym = int(m.group('homonym'))
        title = p.sub('', title)
    return homonym, title


def get_lang(title):
    lang = ''
    p = re.compile(r'\s+[\\/](?P<lang>\w{2,})')
    m = p.search(title)
    if m:
        lang = m.group('lang')
        title = p.sub('', title)
    return lang, title


def get_link(title, redirect=False):
    title_encoded = quote_plus(title)
    if not redirect:
        href = f'https://ru.wiktionary.org/wiki/{title_encoded}'
    else:
        href = f'https://ru.wiktionary.org/w/index.php?title={title_encoded}' \
               f'&redirect=no'
    return f'<a href="{href}">{title}</a>'


def get_response_data(title, title_redirect, lang, homonym_index, content):
    if not content:
        return f'▪<b>{title}</b>\n\n' \
               f'❌ Слово не найдено\n', [], 0, ''

    page = OnlinePage(title, silent=True)
    reply_text = f'▪<b>{title}</b>'

    if title_redirect:
        reply_text += f' → <b>{title_redirect}</b>'

    if not lang:
        lang = page.languages.keys[0]
    lang_text = languages.get(lang, lang)
    reply_text += f'  ({lang_text})\n\n'

    other_langs = page.languages.keys if len(page.languages) > 1 else []
    if lang not in page.languages.keys:
        reply_text += f'⛔ Язык "<b>{lang}</b>" не найден\n'
        return reply_text, other_langs, 0, ''

    lang_obj = page.languages[lang]
    homonyms = lang_obj.homonyms.keys
    other_homonyms = len(homonyms) if len(homonyms) > 1 else 0

    if homonym_index != 1 and homonym_index - 1 >= len(homonyms):  # "-1" т.к. нумеруем с 1
        reply_text += f'⛔ <b>{homonym_index}-й</b> омоним не найден\n'
        return reply_text, other_langs, other_homonyms, lang

    homonym_obj = lang_obj.homonyms[homonym_index - 1]
    if 'semantic' not in homonym_obj.keys:  # todo: fix to be able to check by header "Семантические свойства"
        reply_text += '🔻 Секция «Семантические свойства» не найдена\n'
        return reply_text, other_langs, other_homonyms, lang

    block_obj = homonym_obj.blocks['Семантические свойства']
    if 'definition' in block_obj.keys:  # todo: fix to be able to check by header "Значение"
        sub_block_content = block_obj['Значение'].content
        definitions = clear_definitions(sub_block_content).split('\n')
        definitions = map(str.strip, definitions)
        definitions = filter(lambda x: x != '#', definitions)

        if not definitions:
            reply_text += '🔺 Значение отсутствует\n'
            return reply_text, other_langs, other_homonyms, lang

        for definition in definitions:
            if definition.startswith('#'):
                definition = definition[1:].strip()
                reply_text += f'🔹{definition}\n'
            else:
                reply_text += f'🔻{definition}\n'
        return reply_text, other_langs, other_homonyms, lang
    else:
        p = re.compile(
            '# *{{значение.*?\| *определение *= *(.*?)\s*\| *пометы *= *(.*?)\|',
            flags=re.UNICODE | re.DOTALL)
        definition_parts = p.findall(block_obj.content)
        if not definition_parts:
            reply_text += '🔻 Секция «Значение» не найдена\n'
            return reply_text, other_langs, other_homonyms, lang

        definitions = list()
        for parts in definition_parts:
            definition = clear_definitions(parts[0])
            labels = clear_definitions(parts[1])
            if labels:
                definition = (labels + ' ' + definition).strip()
            if definition:
                definitions.append(definition)
        if not definitions:
            reply_text += '🔺 Значение отсутствует\n'
            return reply_text, other_langs, other_homonyms, lang

        for definition in definitions:
            reply_text += '🔹%s\n' % definition.strip()
        return reply_text, other_langs, other_homonyms, lang


def get_response(title, lang, homonym):
    homonym = int(homonym)
    title, content, title_redirect = get_content(title)

    reply_text, other_langs, other_homonyms, lang = \
        get_response_data(title, title_redirect, lang, homonym, content)
    reply_text += '\n🔎 <a href="https://ru.wiktionary.org/wiki/{0}">' \
                  'Викисловарь</a>'.format(quote_plus(title))

    buttons = []
    if other_langs:
        values = [
            (f'{value}' if value != lang else f'• {value}',
             f'{title}|{value}|1')
            for value in other_langs
        ]
        for chunk in chunks(values, 4):
            buttons.append([
                telegram.InlineKeyboardButton(text, callback_data=data)
                for text, data in chunk
            ])
    if other_homonyms:
        values = [
            (f'{i}' if i != homonym else f'• {i}',
             f'{title}|{lang}|{i}')
            for i in range(1, other_homonyms + 1)
        ]
        for chunk in chunks(values, 6):
            buttons.append([
                telegram.InlineKeyboardButton(text, callback_data=data)
                for text, data in chunk
            ])
    reply_markup = telegram.InlineKeyboardMarkup(buttons)
    return reply_text, reply_markup


def save_log(message, title):  # todo: move it to some `utils`
    user = message.from_user
    name = f'{user.first_name} {user.last_name}'.strip()
    path = join(ROOT_PATH, 'telegram_bot', 'logs', 'titles.txt')
    append(path, f'[{message.date}] @{user.username} ({name}) #{user.id}\n'
                 f'{title}\n')


def process_message(bot, update):
    chat_id = update.message.chat_id
    title = update.message.text.strip()

    if '\n' in title:
        return

    if update.message.chat_id < 0:  # if we are in a group chat
        if not title.endswith('='):
            return

    # bot is typing:
    bot.sendChatAction(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    skip_content = title.endswith('==')

    title = re.sub(r'\s*=+$', '', title)
    homonym, title = get_homonym(title)
    lang, title = get_lang(title)
    title = title.strip()
    save_log(update.message, title)

    if skip_content:
        title, content, title_redirect = get_content(title)
        icon = '✅' if content else '❌'
        if not title_redirect:
            url_title = get_link(title)
            response = f'{icon} {url_title}'
        else:
            url_title = get_link(title, redirect=True)
            url_title_redirect = get_link(title_redirect)
            response = f'{icon} {url_title} → {url_title_redirect}'
        send(bot, chat_id, response)
        return

    response, reply_markup = get_response(title, lang, homonym)
    send(bot, chat_id, response, reply_markup)


def process_callback(bot, update):
    callback_query = update.callback_query
    query_data = callback_query.data
    title, lang, homonym = query_data.split('|')
    response, reply_markup = get_response(title, lang, homonym)
    callback_query.edit_message_text(response, reply_markup=reply_markup,
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)


# todo: catch any exception and send them to me!
# todo: check if message was edited?
# todo: справку по использованию (=, ==, /2, /en)
