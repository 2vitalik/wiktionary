import copy
import re


def log(value):
    print(value)


def clone(value):
    if type(value) == dict:
        return copy.deepcopy(value)
    return value.copy()


def fix_re(value):
    return value.replace('%', '\\')


class text:
    @staticmethod
    def trim(value):
        return value.strip()

    @staticmethod
    def split(string, delimiter):
        return re.split(fix_re(delimiter), string)


class ustring:
    @staticmethod
    def sub(str, index1, index2):
        pass

    @staticmethod
    def gsub(string, pattern, replace_to):
        return re.sub(fix_re(pattern), fix_re(replace_to), string)

    @staticmethod
    def match(string, pattern):
        m = re.search(fix_re(pattern), string)
        if not m:
            return
        try:
            return m.group(1)
        except IndexError:
            pass
        return m
