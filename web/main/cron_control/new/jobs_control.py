from datetime import datetime, timedelta

from main.cron_control.jobs_control import remove_file
from main.cron_control.new.cron_list import cron_filenames


def new_job_reset(slug):
    if slug == 'recent':
        return remove_file(cron_filenames['recent'])

    if slug == 'reports_recent':
        with open(cron_filenames['reports_recent'], 'w') as f:
            f.write(datetime.now().replace(hour=0, minute=0, second=0).strftime('%Y-%m-%d %H:%M:%S'))
        return True

    if slug == 'new_articles':
        with open(cron_filenames['new_articles'], 'w') as f:
            date = datetime.now().replace(hour=0, minute=0, second=0) - timedelta(days=1)
            f.write(date.strftime('%Y-%m-%d %H:%M:%S'))
        return True

    if slug == 'forum_news':
        with open(cron_filenames['forum_news'], 'w') as f:
            f.write('{}')
        return True

    return False
