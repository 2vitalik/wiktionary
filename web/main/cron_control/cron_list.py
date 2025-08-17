import os
import re
from datetime import datetime, timedelta

from main.cron_control.all_jobs import all_cron_jobs
from main.cron_control.jobs_control import job_started, job_started_file



def fix_time(time):
    return time + timedelta(hours=3)


def simplify(delta):
    return re.sub('\.\d+$', '', str(delta))


def get_cron_list():
    cron_list = []
    for prj, cron_jobs in all_cron_jobs.items():
        for cron_job in cron_jobs:
            slug = cron_job['name']
            if prj == 'ws1':
                status = job_started(slug)
                modified = ''
                delta = ''
                delta_str = ''
                reset_active = False
                if status:
                    mtime = datetime.fromtimestamp(os.path.getmtime(job_started_file(slug)))
                    modified = fix_time(mtime)
                    delta = datetime.now() - mtime
                    delta_str = simplify(delta)
                    reset_active = delta > timedelta(days=1)
            else:
                status = '?'
                raise
            cron_list.append({
                'prj': prj,
                'slug': slug,
                'status': status,
                'modified': modified,
                'delta': delta,
                'delta_str': delta_str,
                'reset_active': reset_active,
            })
    return cron_list
