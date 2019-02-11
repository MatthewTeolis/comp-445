import os


def get_iterator_all_files_name(path):
    for (dir_path, dir_names, filenames) in os.walk(path):
        for filename in filenames:
            yield os.path.join(dir_path, filename)


if __name__ == '__main__':
    for file in get_iterator_all_files_name('..'):
        print(file)

