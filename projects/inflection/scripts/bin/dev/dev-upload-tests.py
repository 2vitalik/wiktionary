from projects.inflection.scripts.bin.dev.version import version, desc
from projects.inflection.scripts.lib.upload import upload_lua


if __name__ == '__main__':
    upload_lua(version, desc, dev=True, testcases=True)
