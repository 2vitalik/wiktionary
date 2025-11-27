from main.cron_control.all_jobs import all_cron_jobs
from main.cron_control.jobs_control import job_started, get_modified


def get_cron_list():
    cron_list = []
    for prj, cron_jobs in all_cron_jobs.items():
        for cron_job in cron_jobs:
            slug = cron_job['name']
            if prj == 'ws1':
                status = job_started(slug)
                modified = ''
                delta_str = ''
                reset_active = False
                if status:
                    modified, delta_str, reset_active = get_modified(slug)
            else:
                raise
            cron_list.append({
                'prj': prj,
                'slug': slug,
                'title': slug.replace('_', ' ').title(),
                'status': status,
                'modified': modified,
                'delta_str': delta_str,
                'reset_active': reset_active,
            })
    return cron_list
