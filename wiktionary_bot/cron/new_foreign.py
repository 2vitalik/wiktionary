import sys; sys.path.append('../..')
from collections import defaultdict
from datetime import datetime, timedelta
from os.path import join

import telegram

from core.conf import conf
from core.storage.main import storage
from libs.parse.sections.page import Page
from libs.utils.io import read_lines, append
from libs.utils.numbers import get_plural
from wiktionary_bot.cron.new_foreign_utils import messages
from wiktionary_bot.src.semantic import load_languages, clear_definitions, \
    get_link
from wiktionary_bot.src.slack import slack
from wiktionary_bot.src.utils import send, check_offensive


new_foreign_header = '➕ Новые статьи на др. языках <i>(за сутки)</i>'


class titles:
    filename = join(conf.data_path, 'new_foreign', 'titles.txt')

    @classmethod
    def get(cls):
        return set(read_lines(cls.filename))

    @classmethod
    def add(cls, title):
        append(cls.filename, title)


def get_new_foreign():
    old_titles = titles.get()
    new_by_lang = defaultdict(list)
    new_set = set()

    now = datetime.now()
    end_date = datetime(now.year, now.month, now.day)
    # start_date -= timedelta(days=300)  # just for debug
    start_date = end_date - timedelta(days=1)

    iterator = storage.iterate_changed_pages(start_date, silent=True)
    for log_dt, title, page in iterator:
        if log_dt > end_date:
            break

        if title in new_set:
            continue
        if title in old_titles:
            continue

        content = page.content
        if check_offensive(content):
            continue

        page = Page(title, content, silent=True)
        langs = set(page.languages.all().keys())
        langs.discard('ru')
        if not langs:
            continue

        for lang in langs:
            new_by_lang[lang].append(page)
            # print(title, lang)  # just for debugging
        new_set.add(title)

    return new_by_lang, new_set


@slack('new_foreign')
def process_new_foreign():
    bot = telegram.Bot(conf.telegram_token)
    chat_id = conf.new_channel_id
    languages = load_languages()

    new_by_lang, new_set = get_new_foreign()
    if '' in new_by_lang:
        del new_by_lang['']

    sorted_data = sorted(new_by_lang.items(), key=lambda x: (-len(x[1]), x[0]))
    if not sorted_data:
        return  # no new foreign articles

    num_langs_to_show = 7
    main_message = f'{new_foreign_header}\n\n'
    for lang, pages in sorted_data[:num_langs_to_show]:
        lang_text = languages.get(lang, f'Неизвестный').capitalize()
        lang_text += f' <code>{lang}</code>'
        count = len(pages)
        plural = get_plural(count, 'статья', 'статьи', 'статей')
        main_message += f'▪️ {lang_text} — <b>{count}</b> {plural}\n'
    if len(sorted_data) > num_langs_to_show:
        main_message += f'▪️ <i>и ещё...</i>\n'
    main_message += '\n💬 Cписки статей в комментариях ↓'

    msg_count_limit = 20
    max_count_limit = 50

    current_message = ''
    current_count = 0
    for lang, pages in sorted_data:
        pages = sorted(pages, key=lambda p: p.title)

        lang_text = languages.get(lang, f'Неизвестный').capitalize()
        lang_header = f'▪️ <b>{lang_text}</b> <code>{lang}</code>:'

        lines = []
        for page in pages[:max_count_limit]:
            link = get_link(page.title)
            prefix = f'▫️ {link} —'
            homonym = page.languages[lang].homonyms[0]
            block = homonym.blocks['Семантические свойства']
            if 'definition' not in block.keys:
                lines.append(f'{prefix} <i>значение не найдено</i>')
                continue

            definitions = \
                clear_definitions(block['Значение'].content).split('\n')
            definitions = list(map(str.strip, definitions))
            definitions = list(filter(lambda x: x != '#', definitions))

            if not definitions:
                value = '<i>значение отсутствует</i>'
            else:
                values = []
                for definition in definitions:
                    if definition.startswith('#'):
                        definition = definition[1:].strip()
                        values.append(definition)
                    elif definition:
                        values.append(definition)
                value = '; '.join(values)
            lines.append(f'{prefix} {value}')
        if len(pages) > max_count_limit:
            lines.append(f'▫️ <i>отображены только первые {max_count_limit}'
                         f' из {len(pages)}</i>')
        block = f'\n{lang_header}\n' + '\n'.join(lines) + '\n'

        if current_count + len(pages) <= msg_count_limit:
            current_count += len(pages)
            current_message += block
        else:
            if current_message:
                messages.append(current_message)
            current_count = len(pages)
            current_message = block

    if current_message:
        messages.append(current_message)

    messages.save()
    send(bot, chat_id, main_message)
    titles.add('\n'.join(new_set))


if __name__ == '__main__':
    process_new_foreign()
