from projects.inflection.scripts.lib.convert_dir import convert_dir


if __name__ == '__main__':
    # dev = False
    dev = True

    convert_dir(dev, 'lua', 'py')
