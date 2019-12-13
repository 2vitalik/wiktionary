from projects.inflection.modules.dev.dev_py import mw


# ...


def escape(value):
    # Prefix every non-alphanumeric character (%W) with a % escape character,
    # where %% is the % escape, and %1 is original character
    return mw.ustring.gsub(value, "(%W)", "%%%1")


# ...
