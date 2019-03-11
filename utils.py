import random
import time

from filesort import infile_sort


def gen_file(filename, string_count, max_length):

    with open(filename, 'w') as f:
        for i in range(string_count):
            string_length = max_length  # random.randint(1, max_length)
            for k in range(string_length):
                f.write(chr(random.randint(65, 91)))  # символы из [A-\[]
            f.write('\n')


if __name__ == '__main__':
    for _string_count in range(2, 10):
        string_count = 2 ** _string_count
        max_length = 2 ** _string_count

        filename = '%s_%s.txt' % (string_count, max_length)

        gen_file(filename, string_count, max_length)

        with open(filename, 'r') as f:
            d_0 = sorted([l.strip('\n') for l in f]) # Осторожно!

        s = time.time()
        infile_sort(filename, string_count, max_length)
        s_f = time.time() - s

        with open(filename, 'r') as f:
            d_1 = [l.strip('\n') for l in f]

        if d_0 == d_1:
            print(string_count, max_length, 'ok!', s_f)
        else:
            print(string_count, max_length, 'not', s_f)

