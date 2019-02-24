import re
from os.path import join
from urllib.parse import quote

import telegram
from pywikibot.exceptions import NoPage

from core.conf.conf import ROOT_PATH, SYNC_PATH
from core.storage.main import storage
from libs.parse.online_page import OnlinePage
from libs.utils.collection import chunks
from libs.utils.io import read, append
from libs.utils.wikibot import load_page_with_redirect
from telegram_bot.src.utils import send, edit


def clear_definitions(text):  # todo: move this to some `lib`
    # удаление лишнего:
    text = text.replace('{µ(Q)}', '')
    text = re.sub('<!--(.+?)-->', '', text)
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
    text = re.sub("''([^']+?)''", '<i>\\1</i> ', text)

    # замены шаблонов:
    text = text.replace('{as ru}', '<i>(аналогично русскому слову)</i>')

    return text.strip()


def load_languages():  # todo: move this to some `lib`
    path = join(SYNC_PATH, 'data', 'language-data.lua')
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


class ShortReply:
    def __init__(self, title):
        self.title = title
        self.title_redirected = None
        self.content = None
        self.buttons = None
        if self.is_regexp():
            self.regexp = self.title
            self.titles = self.filter_titles()
            if len(self.titles) == 1:
                self.title = self.titles[0]
            else:
                self.title = None
        if self.title:
            self.fetch_content()
            self.text = self._short_reply_text()
        elif self.regexp:
            self.text = self._regexp_text()
        else:
            # todo: log something
            raise Exception('Never should happen')

    def is_regexp(self):
        if self.title.endswith('~'):
            self.title = self.title[:-1].strip()
            return True
        if self.title.endswith(' ?'):
            self.title = self.title[:-2].strip()
            return True
        return '[' in self.title or '?' in self.title or '*' in self.title

    def filter_titles(self):
        titles = []
        for title in storage.titles:
            if re.match(f'{self.regexp}$', title):
                titles.append(title)
                if len(title) > 100:
                    break
        return titles

    def _regexp_text(self):
        text = f'🌀 <b>{self.regexp}</b>  (регулярка)\n\n'
        if self.titles:
            text += f'Статьи в Викисловаре:\n'
            text += '\n'.join([f'▫️ ' + get_link(title)
                               for title in sorted(self.titles)])
        else:
            text += '❌ Ничего не найдено'
        return text

    def load_page_with_redirect(self, title):
        try:
            self.content, self.title_redirected = load_page_with_redirect(title)
            return True
        except NoPage:
            return False

    def fetch_content(self):
        if self.load_page_with_redirect(self.title):
            return
        # пытаемся трансформировать регистр:
        titles_transformed = [self.title.lower(), self.title.upper(),
                              self.title.capitalize()]
        for title_transformed in titles_transformed:
            if self.title != title_transformed:
                if self.load_page_with_redirect(title_transformed):
                    self.title = title_transformed
                    return

    def _short_reply_text(self):
        icon = '✅' if self.content else '❌'
        if not self.title_redirected:
            url_title = get_link(self.title)
            return f'{icon} {url_title}'
        else:
            url_title = get_link(self.title, redirect=True)
            url_title_redirect = get_link(self.title_redirected)
            return f'{icon} {url_title} → {url_title_redirect}'


class Reply(ShortReply):
    languages = load_languages()

    def __init__(self, title, lang_key='', homonym_index=0):
        super().__init__(title)

        if self.title:
            self.lang_key = lang_key
            self.homonym_index = int(homonym_index)

            self.title_stressed = self.active_title
            self.lang_keys = []
            self.homonyms_count = 0
            self.text = self._reply_text()
            self.buttons = self._reply_buttons()

    @property
    def active_title(self):
        if self.title_redirected:
            return self.title_redirected
        return self.title

    @property
    def _reply_title(self):
        if self.title_redirected:
            result = f'▪ <b>{self.title}</b> → <b>{self.title_stressed}</b>'
        else:
            result = f'▪ <b>{self.title_stressed}</b>'
        lang_text = self.languages.get(self.lang_key, self.lang_key)
        if lang_text:
            result += f'   <i>// {lang_text}</i>'
        return result

    @property
    def _reply_body(self):
        if not self.content:
            self.lang_key = ''
            return '❌ Слово не найдено'

        page = OnlinePage(self.active_title, silent=True)
        self.lang_keys = page.languages.keys
        if not self.lang_key:
            self.lang_key = self.lang_keys[0]

        if self.lang_key not in self.lang_keys:
            return f'⛔ Язык "<b>{self.lang_key}</b>" не найден'

        lang_obj = page.languages[self.lang_key]
        homonyms_keys = lang_obj.homonyms.keys
        self.homonyms_count = len(homonyms_keys)

        if self.homonym_index >= self.homonyms_count:
            return f'⛔ <b>{self.homonym_index+1}-й</b> омоним не найден'

        homonym_obj = lang_obj.homonyms[self.homonym_index]

        stresses = set()  # todo: several stresses feature
        for tpl in homonym_obj.templates('по-слогам', 'по слогам').last_list():
            value = tpl.params.replace('|', '').replace('.', '')
            if not value:
                continue
            if value.replace('́', '') != self.active_title:
                continue
            # stresses.add(value.index('́'))  # todo: several stresses feature
            self.title_stressed = value

        if 'semantic' not in homonym_obj.keys:  # todo: fix to be able to check by header "Семантические свойства"
            return '🔻 Секция «Семантические свойства» не найдена'

        block_obj = homonym_obj.blocks['Семантические свойства']
        if 'definition' in block_obj.keys:  # todo: fix to be able to check by header "Значение"
            definitions = \
                clear_definitions(block_obj['Значение'].content).split('\n')
            definitions = map(str.strip, definitions)
            definitions = filter(lambda x: x != '#', definitions)

            if not definitions:
                return '🔺 Значение отсутствует'

            reply = ''
            for definition in definitions:
                if definition.startswith('#'):
                    definition = definition[1:].strip()
                    reply += f'🔹 {definition}\n'
                elif definition:
                    reply += f'🔻 {definition}\n'
            return reply
        else:
            p = re.compile(
                '# *{{значение.*?\| *определение *= *(.*?)\s*\| *пометы *= *(.*?)\|',
                flags=re.UNICODE | re.DOTALL)
            definition_parts = p.findall(block_obj.content)
            if not definition_parts:
                return '🔻 Секция «Значение» не найдена'

            definitions = list()
            for parts in definition_parts:
                definition = clear_definitions(parts[0])
                labels = clear_definitions(parts[1])
                if labels:
                    definition = (labels + ' ' + definition).strip()
                if definition:
                    definitions.append(definition)
            if not definitions:
                return '🔺 Значение отсутствует'

            reply = ''
            for definition in definitions:
                reply += '🔹%s\n' % definition.strip()
            return reply

    def _reply_text(self):
        link = get_link(self.title, f'{self.title} в Викисловаре')
        body = self._reply_body.strip()
        return f'{self._reply_title}\n\n{body}\n\n🔎 {link}'

    def _reply_buttons(self):
        buttons = []
        if len(self.lang_keys) > 1:
            values = [
                (f'{value}' if value != self.lang_key else f'• {value}',
                 f'{self.title}|{value}|0')
                for value in self.lang_keys
            ]
            for chunk in chunks(values, 4):
                buttons.append([
                    telegram.InlineKeyboardButton(text, callback_data=data)
                    for text, data in chunk
                ])
        if self.homonyms_count > 1:
            values = [
                (f'{i+1}' if i != self.homonym_index else f'• {i+1}',
                 f'{self.title}|{self.lang_key}|{i}')
                for i in range(self.homonyms_count)
            ]
            for chunk in chunks(values, 6):
                buttons.append([
                    telegram.InlineKeyboardButton(text, callback_data=data)
                    for text, data in chunk
                ])
        return telegram.InlineKeyboardMarkup(buttons)


def save_log(message, title):  # todo: move it to some `utils`
    user = message.from_user
    name = f'{user.first_name} {user.last_name}'.strip()
    path = join(ROOT_PATH, 'telegram_bot', 'logs', 'titles.txt')
    append(path, f'[{message.date}] @{user.username} ({name}) #{user.id}\n'
                 f'{title}\n')


def get_homonym(title):
    homonym = 0
    p = re.compile(r'\s+[\\/](?P<homonym>\d+)')
    m = p.search(title)
    if m:
        homonym = int(m.group('homonym')) - 1
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


def get_link(title, text=None, redirect=False):
    # todo: и сюда ударение?
    if not text:
        text = title
    if not redirect:
        href = f'https://ru.wiktionary.org/wiki/{quote(title)}'
    else:
        href = f'https://ru.wiktionary.org/w/index.php?title={quote(title)}' \
               f'&redirect=no'
    return f'<a href="{href}">{text}</a>'


def process_message(bot, update):
    chat_id = update.message.chat_id
    title = update.message.text.strip()

    if '\n' in title:
        return

    if update.message.chat_id < 0:  # if we are in a group chat
        if not title.endswith(('=', '~', ' ?')):
            return

    # bot is typing:
    bot.send_chat_action(chat_id=chat_id, action=telegram.ChatAction.TYPING)

    skip_content = title.endswith('==')

    title = re.sub(r'\s*=+$', '', title)
    homonym, title = get_homonym(title)
    lang, title = get_lang(title)
    title = title.strip()
    save_log(update.message, title)

    msg = send(bot, chat_id, '🔎 <i>Делаю запрос в Викисловарь...</i>')

    if skip_content:
        reply = ShortReply(title)
    else:
        reply = Reply(title, lang, homonym)

    edit(bot, chat_id, msg.message_id, reply.text, reply.buttons)


def process_callback(bot, update):
    callback_query = update.callback_query
    query_data = callback_query.data
    title, lang, homonym = query_data.split('|')
    reply = Reply(title, lang, homonym)
    callback_query.edit_message_text(reply.text, reply_markup=reply.buttons,
                                     parse_mode=telegram.ParseMode.HTML,
                                     disable_web_page_preview=True)


# todo: catch any exception and send them to me!
# todo: check if message was edited?
# todo: справку по использованию (=, ==, /2, /en)
