

def read(filename):
    return open(filename, encoding='utf-8').read()


def write(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
