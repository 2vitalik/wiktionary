from projects.inflection.scripts.lib.upload import upload_lua


if __name__ == '__main__':
    version = '4.0.7'
    desc = 'Реализация иерархических логов (вызовы функций, отступы)'

    upload_lua(version, desc, dev=False)
