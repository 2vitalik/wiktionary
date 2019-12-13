from projects.inflection.scripts.lib.upload import upload


if __name__ == '__main__':
    version = '4.0.6'
    desc = '-'

    upload(version, desc, dev=False)
