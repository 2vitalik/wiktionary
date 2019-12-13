from projects.inflection.scripts.lib.upload import upload


if __name__ == '__main__':
    # inflection_version = '2.4'

    dev = False
    # dev = True

    version = '4.0.5'
    desc = 'Bug-fix для крестика в квадратике (регулярка)'

    print(f'v{version}: {desc}')
    upload(dev, version, desc)


# todo: почистить старые неиспользуемые модули на ВС (старые имена)
# todo: разные файлы запуска для dev-версии и для prod-версии
