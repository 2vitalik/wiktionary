

def read(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()


def write(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
