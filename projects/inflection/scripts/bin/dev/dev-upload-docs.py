from projects.inflection.scripts.bin.dev.version import version, desc
from projects.inflection.scripts.lib.upload import upload_docs


if __name__ == '__main__':
    upload_docs(version, desc, dev=True)
