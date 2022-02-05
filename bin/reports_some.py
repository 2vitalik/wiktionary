import up  # don't remove this
from core.reports.reports.templates.tpl_multilang import MultilangTemplate
from core.reports.scripts.run import reports_some


if __name__ == '__main__':
    reports_some([MultilangTemplate])
