import os
import re
from datetime import timedelta, datetime
from os.path import join, exists

from core.conf import conf


def job_started_file(slug):
    return join(conf.ws1_jobs_path, 'jobs/started', slug)


def job_continuous_file(slug):
    return join(conf.ws1_jobs_path, 'jobs/last-action', slug)


def job_stop_file(slug):
    return join(conf.ws1_jobs_path, 'jobs/control/stops', slug)


def job_pause_file(slug):
    return join(conf.ws1_jobs_path, 'jobs/control/pauses', slug)


def job_started(slug):
    return exists(job_started_file(slug))


def job_continuous(slug):
    return exists(job_continuous_file(slug))


def job_stopped(slug):
    return exists(job_stop_file(slug))


def job_paused(slug):
    return exists(job_pause_file(slug))


def remove_file(filename):
    if not exists(filename):
        return False
    os.remove(filename)
    return True


def create_file(filename):
    if exists(filename):
        return False
    with open(filename, 'w') as f:
        f.write('')
    return True


def fix_time(time):
    return time + timedelta(hours=3)


def simplify(delta):
    return re.sub('\.\d+$', '', str(delta))


def get_modified(slug):
    mtime = datetime.fromtimestamp(os.path.getmtime(job_started_file(slug)))
    delta = datetime.now() - mtime

    modified = fix_time(mtime)
    delta_str = simplify(delta)
    reset_active = delta > timedelta(days=1)

    return modified, delta_str, reset_active


def job_reset(slug):
    if not job_started(slug):
        return None
    modified, delta_str, reset_active = get_modified(slug)
    if not reset_active:
        return None
    return remove_file(job_started_file(slug))


def job_reset_continuous(slug):
    return remove_file(job_continuous_file(slug))


def job_stop(slug):
    return create_file(job_stop_file(slug))


def job_unstop(slug):
    return remove_file(job_stop_file(slug))


def job_pause(slug):
    return create_file(job_pause_file(slug))


def job_resume(slug):
    return remove_file(job_pause_file(slug))
