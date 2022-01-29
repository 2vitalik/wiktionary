import up  # don't remove this
from core.storage.postponed.shortcuts import update_recent


if __name__ == '__main__':
    update_recent('authors')  # todo: process slack errors
