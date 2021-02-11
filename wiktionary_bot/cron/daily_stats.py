import re
import sys
from collections import defaultdict
from os.path import join

import requests
import telegram

sys.path.append('../..')

from core.conf import conf
from libs.utils.dt import dtf
from libs.utils.io import write, read, json_load, json_dump
from wiktionary_bot.cron.daily_stats_utils import langs, daily_stats_header, \
    daily_stats_messages
from wiktionary_bot.src.semantic import load_languages
from wiktionary_bot.src.slack import slack
from wiktionary_bot.src.utils import send

# yesterday = datetime.now() - timedelta(days=1)  # fixme: tmp


def html_path(lang):
    return join(conf.data_path, 'daily_stats', 'history', 'html',
                dtf('Ym/Ymd'), f'{lang}.html')


def dump_stats():
    print(dtf('Ymd'))
    for lang in langs:
        print('Dumping language:', lang)
        url = f'https://{lang}.wiktionary.org/wiki/Special:Statistics'
        r = requests.get(url)
        write(html_path(lang), r.content.decode())


def get_stats():
    new_data = {}
    for lang in langs:
        html_content = read(html_path(lang))
        # table = re.search(
        #     '<table class="wikitable mw-statistics-table">(.*?)</table>',
        #     html_content,
        #     re.DOTALL,
        # ).group(1)
        # write(f'table/{lang}.html', table)
        numbers = re.findall('<td class="mw-statistics-numbers">(.*?)</td>',
                             html_content)
        # write(f'numbers/{lang}.txt', '\n'.join(numbers))
        # print(':', ' | '.join(numbers))
        # if len(numbers) != 20:
        #     print(lang, len(numbers))
        values = []
        for index in [0, 1, 3, 5, 6]:
            value = re.sub('[^0-9]', '', numbers[index])
            if value:
                values.append(value)
        if values:
            # write(f'values/{lang}.txt', '\n'.join(values))
            new_data[lang] = {
                'goods': int(values[0]),
                'pages': int(values[1]),
                'edits': int(values[2]),
                'users': int(values[3]),
                'active': int(values[4]),
            }
        # else:
        #     print(lang)

    history_filename = join(conf.data_path, 'daily_stats', 'history', 'values',
                            f'{dtf("Ym/Ymd")}.json')
    active_filename = join(conf.data_path, 'daily_stats', 'active.json')

    old_data = json_load(active_filename)
    json_dump(history_filename, new_data)
    json_dump(active_filename, new_data)

    return old_data, new_data


def calc_diff(old_data, new_data):
    order = sorted(new_data, key=lambda lang: -new_data[lang]['goods'])
    print(order)

    diff_data = defaultdict(dict)

    for lang, new_counts in new_data.items():
        old_counts = old_data[lang]
        for key, new_value in new_counts.items():
            old_value = old_counts[key]
            if new_value != old_value:
                diff_data[key][lang] = new_value - old_value
        key = 'other'
        old_value = old_counts['pages'] - old_counts['goods']
        new_value = new_counts['pages'] - new_counts['goods']
        if new_value != old_value:
            diff_data[key][lang] = new_value - old_value

    for key, data in diff_data.items():
        diff_data[key] = dict(sorted(
            data.items(),
            key=lambda item: (-item[1], order.index(item[0]))
        ))

    history_filename = join(conf.data_path, 'daily_stats', 'history', 'diff',
                            f'{dtf("Ym/Ymd")}.json')
    active_filename = join(conf.data_path, 'daily_stats', 'diff.json')

    json_dump(history_filename, diff_data)
    json_dump(active_filename, diff_data)

    return diff_data


def diff_num(value):
    if value > 0:
        return f'+<b>{value}</b>'
    if value < 0:
        return f'-<b>{-value}</b>'
    return '+0'


def send_stats(diff_data):
    bot = telegram.Bot(conf.telegram_token)
    chat_id = conf.new_channel_id
    languages = load_languages()

    ru_only = 'TODO'  # todo
    # '▫️ {ru_only}  новых русских статей'  # todo

    ru_goods = diff_num(diff_data['goods'].get('ru', 0))
    ru_other = diff_num(diff_data['other'].get('ru', 0))
    ru_edits = diff_num(diff_data['edits'].get('ru', 0))
    ru_users = diff_num(diff_data['users'].get('ru', 0))
    ru_active = diff_num(diff_data['active'].get('ru', 0))

    main_message = f'''
{daily_stats_header}
▫️ {ru_goods}  всего новых статей
▫️ {ru_other}  других новых станиц
▫️ {ru_edits}  всего правок страниц
▫️ {ru_users}  новых пользователей
▫️ {ru_active}  активных пользователей

💬 Сравнительная статистика по другим Викисловарям доступна в коментариях ↓

#статистика
    '''
    print(main_message)
    print('-' * 100)

    categories = [
        ('goods', '➕', 'Всего новых статей',
         'wiktionary.org/wiki/Special:NewPages'),
        ('other', '➗', 'Других новых страниц',
         'wiktionary.org/wiki/Special:Statistics'),
        ('edits', '✏️', 'Всего правок страниц',
         'wiktionary.org/wiki/Special:RecentChanges'
         '?hidecategorization=1&hideWikibase=1&limit=200&days=1&urlversion=2'),
        ('users', '👤', 'Новых пользователей',
         'wiktionary.org/w/index.php'
         '?title=Special:ListUsers&limit=100&creationSort=1&desc=1'),
        ('active', '⭐️', 'Активных пользователей',
         'wiktionary.org/w/index.php?title=Special:ActiveUsers&limit=100'),
    ]

    for key, icon, title, url in categories:
        if not diff_data[key]:
            continue
        message = f'{icon} <b>{title}:</b>\n\n'
        for lang, number in list(diff_data[key].items())[:10]:
            if lang == 'simple':
                lang_text = 'Английский'
            else:
                lang_text = languages.get(lang, f'Неизвестный').capitalize()
            lang_value = f'<a href="https://{lang}.{url}">{lang_text}</a>' \
                         f' <code>{lang}</code>'
            message += f'▪️ {diff_num(number)} — {lang_value}\n'
        print(message)
        print('-' * 100)
        daily_stats_messages.append(message)

    daily_stats_messages.save()
    send(bot, chat_id, main_message)


@slack('daily_stats')
def daily_stats():
    dump_stats()
    diff_data = calc_diff(*get_stats())
    send_stats(diff_data)


if __name__ == '__main__':
    daily_stats()
