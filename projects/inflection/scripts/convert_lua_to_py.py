from projects.inflection.scripts.lib.convert_dir import convert_dir


if __name__ == '__main__':
    # unit = 'noun'
    unit = 'adj'

    convert_dir(unit, 'lua', 'py')
