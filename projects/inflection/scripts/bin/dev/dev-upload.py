from projects.inflection.scripts.lib.upload import upload_lua


if __name__ == '__main__':
    version = '4.1.4'
    desc = 'Использование dev-шаблонов для dev-версии'

    upload_lua(version, desc, dev=True)


# todo: почистить старые неиспользуемые модули на ВС (старые имена)
# todo: разные файлы запуска для dev-версии и для prod-версии
# todo: append history changes entry to some page on wikt
