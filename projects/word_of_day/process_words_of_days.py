import json
import re
import urllib.parse
from datetime import datetime
from os.path import exists

from pywikibot import NoPage
from shared_utils.io.io import read, write
from telegram import Bot, ParseMode

from core.conf import conf
from libs.utils.wikibot import load_page, save_page

debug = False
bot = Bot(conf.telegram_token)
path = f'{conf.data_path}/word_of_day'


def send(message):
    bot.sendMessage(conf.main_group_id, message,
                    parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def get_month_name(month):
    months = [
        u'',
        u'января',
        u'февраля',
        u'марта',
        u'апреля',
        u'мая',
        u'июня',
        u'июля',
        u'августа',
        u'сентября',
        u'октября',
        u'ноября',
        u'декабря',
    ]
    return months[int(month)]


def get_title_link(title):
    title_url = urllib.parse.quote_plus(title)
    url = f'https://ru.wiktionary.org/wiki/{title_url}'
    return f'<a href="{url}">{title}</a>'


def process_words_of_days():
    current_year = datetime.now().year
    content = load_page('Викисловарь:Слово_дня')
    content = \
        re.search('== Кандидаты ==\n(.*?)\n== ', content, re.DOTALL).group(1)

    processed = False
    for title in re.findall('\[\[(Викисловарь:Слово дня/[^]]+)]]', content):
        title = title.replace('{{#expr: - 1 + {{CURRENTYEAR}} }}',
                              f'{current_year - 1}')
        title = title.replace('{{#expr: + 1 + {{CURRENTYEAR}} }}',
                              f'{current_year + 1}')
        title = title.replace('{{CURRENTYEAR}}', f'{current_year}')
        print('@', title)
        if process_list(title):
            processed = True

    if processed:
        send('✔️ Бот завершил работу')


def get_new_data(title):
    content = load_page(title, skip_absent=True)
    if not content:
        return {}
    data = {}
    for day, title in re.findall('\|\s*(\d+)\s*=\s*\[\[([^]]+)]]', content):
        print('*', day, '-', title)
        data[day] = title
    return data


def process_list(title):
    m = re.fullmatch('Викисловарь:Слово дня/(\d\d)/(\d{4})', title)
    month, year = m.groups()

    new_data = get_new_data(title)
    new_content = json.dumps(new_data, indent=4, ensure_ascii=False)

    latest_path = f'{path}/{year}/{month}/latest.json'
    old_content = read(latest_path) if exists(latest_path) else '{}'
    old_data = json.loads(old_content)

    processed = False

    if old_content != new_content:
        title_url = urllib.parse.quote_plus(title)
        url = f'https://ru.wiktionary.org/w/index.php' \
              f'?title={title_url}&action=history'
        send(f'🤖 Страница со <b>словами дня</b> за '
             f'<a href="{url}">{month}.{year}</a> '
             f'была изменена, обрабатываю...')

        # save new version
        dt = datetime.now().strftime("%Y-%m-%d__%H-%M-%S")
        dtf = datetime.now().strftime("%Y-%m-%d")
        filename = f"{path}/{year}/{month}/{dtf}/{dt}.json"
        write(filename, new_content)

        if debug and month == '02':
            new_data = {
                "1": "эктогенез",
                "2": "неэтичность",
                "3": "беляшная",
                "4": "Даурия",
                "5": "фавипиравир",
                "6": "привет",  # changed
                "7": "главк",
                "8": "окснар",
                "9": "спенсер",
                "10": "медницкий",
                "11": "пуржить",
                "12": "неспроста",
                # "13": "закавыка",  # removed
                "14": "дерёвня",
                "15": "недельный",
                "16": "туалетка",
                "17": "скаженный",
                "18": "кринж",
                "20": "полемизирующий",  # added
                "22": "словолитня",
                "23": "камчатный",
                "24": "гуашь",
                "25": "Потебня",
                "26": "фильтрационный",
                "27": "серебряник"
            }

        # main function
        process_changes(old_data, new_data, month, year)
        processed = True

        # update latest version
        write(latest_path, new_content)

    return processed


def process_changes(old_data, new_data, month, year):
    processed = False
    month = int(month)
    month_name = get_month_name(month)
    date_suffix = f'{month_name} {year}'

    for day, old_title in old_data.items():
        if day not in new_data:
            old_link = get_title_link(old_title)
            send(f'🌀 Удаление за <b>{day} {date_suffix}</b>:\n'
                 f'➖ {old_link}')
            remove_template(old_title, day, month, year)
            processed = True

    for day, new_title in new_data.items():
        old_title = old_data.get(day)
        if old_title == new_title:
            content, template = prepare_template(new_title, day, month, year)
            link = get_title_link(new_title)
            if content and template not in content:
                send(f'❌ <b>Ошибка:</b> Нет шаблона в {link}')
            continue
        new_link = get_title_link(new_title)
        if old_title:
            old_link = get_title_link(old_title)
            send(f'🌀 Изменение за <b>{day} {date_suffix}</b>:\n'
                 f'➗ {old_link} → {new_link}')
            remove_template(old_title, day, month, year)
        else:
            send(f'🌀 Добавление за <b>{day} {date_suffix}</b>:\n'
                 f'➕ {new_link}')
        add_template(new_title, day, month, year)
        processed = True

    if not processed:
        send('🤷🏻‍♂️ Странно, похоже никаких значимых изменений не было')
    return processed


def prepare_template(title, day, month, year):
    try:
        content = load_page(title)
    except NoPage:
        link = get_title_link(title)
        send(f'⛔️ Страница не найдена: {link}')
        return None, None
    template = '{{слово дня|' + f'{day}|{month}|{year}' + '}}'
    return content, template


def add_template(title, day, month, year):
    content, template = prepare_template(title, day, month, year)
    if not content:
        return
    link = get_title_link(title)
    if template in content:
        send(f'❌ <b>Ошибка:</b> Шаблон уже есть в {link}')
        return
    if '{{слово дня|' in content:
        send(f'❌ <b>Ошибка:</b> Другой шаблон в {link}')
        return
    content = f'{template}\n\n{content}'
    if not debug:
        save_page(title, content, 'Добавление шаблона {{слово дня}}')


def remove_template(title, day, month, year):
    content, template = prepare_template(title, day, month, year)
    if not content:
        return
    link = get_title_link(title)
    if template not in content:
        send(f'❌ <b>Ошибка:</b> Нет шаблона в {link}')
        return
    content = content.replace(f'{template}\n', '')
    content = content.replace(f'{template}', '')
    if not debug:
        save_page(title, content, 'Удаление шаблона {{слово дня}}')


if __name__ == '__main__':
    process_words_of_days()
