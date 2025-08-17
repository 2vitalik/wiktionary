from main.cron_control.all_jobs import all_cron_jobs


def get_cron_list():
    cron_list = []
    for prj, cron_jobs in all_cron_jobs.items():
        for cron_job in cron_jobs:
            cron_list.append({
                'prj': prj,
                'slug': cron_job['name'],
            })
    return cron_list
