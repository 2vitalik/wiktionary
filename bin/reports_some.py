import up  # don't remove this
from core.reports.reports.templates.tpl_length import WrongLength
from core.reports.scripts.run import reports_some


if __name__ == '__main__':
    reports_some([WrongLength])
