from projects.inflection.scripts.lib.upload import upload


if __name__ == '__main__':
    version = '4.1.3'
    desc = 'Ещё немного реструктуризации'

    upload(version, desc, dev=True)


# todo: почистить старые неиспользуемые модули на ВС (старые имена)
# todo: разные файлы запуска для dev-версии и для prod-версии
# todo: append history changes entry to some page on wikt
