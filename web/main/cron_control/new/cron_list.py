import os
from datetime import datetime, timedelta
from os.path import join, exists

from core.conf import conf
from main.cron_control.jobs_control import fix_time, simplify

prj = 'ws0'

cron_filenames = {
    'recent': join(conf.ws0_storage_path, 'main', 'sys', 'lock_recent'),
    'reports_recent': join(conf.ws0_storage_path, 'reports', 'sys', 'latest_updated'),
    'new_articles': join(conf.data_path, 'new_articles', 'latest_processed.txt'),
    'forum_news': join(conf.data_path, 'forum_news', 'forums.json'),
}
status_type = {
    'recent': 'exist',
    'reports_recent': 'empty',
    'new_articles': 'empty',
    'forum_news': 'empty',
}


def get_cron_job(slug):
    filename = cron_filenames[slug]
    modified = ''
    delta_str = ''
    reset_active = False

    if slug not in status_type:
        raise Exception(f'Unknown slug: {slug}')

    if status_type[slug] == 'exist':
        status = exists(filename)
    elif status_type[slug] == 'empty':
        status = not exists(filename) or os.path.getsize(filename) == 0
    else:
        raise Exception(f'Unknown status type: {status_type[slug]}')

    if status:
        if exists(filename):
            mtime = datetime.fromtimestamp(os.path.getmtime(filename))
            modified = fix_time(mtime)
            delta = datetime.now() - mtime
            delta_str = simplify(delta)

            reset_active = delta > timedelta(days=1)
            # reset_active = delta > timedelta(minutes=1)  # fixme: for debugging...
            reset_active = False
        else:
            reset_active = True

    return {
        'prj': prj,
        'slug': slug,
        'title': slug.replace('_', ' ').title(),
        'status': status,
        'modified': modified,
        'delta_str': delta_str,
        'reset_active': reset_active,
    }


def get_new_cron_list():
    return [
        get_cron_job(slug)
        for slug in cron_filenames
    ]
