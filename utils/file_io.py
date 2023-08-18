

def read_file_and_return_per_line(path):
    with open(path, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        return lines


def write_file(path, content):
    with open(path, 'w', encoding='utf-16') as f:
        # print(path, content)
        f.writelines(content)