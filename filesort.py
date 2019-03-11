

def get_previous_line(f):
    seek, s = None, b''
    f.seek(-1, 1)
    while seek != 0 and s != b'\n':
        seek = f.seek(-1, 1)
        s = f.read(1)
        if s == b'\n':
            break
        f.seek(-1, 1)
    return seek


def infile_sort(filename, string_count, max_length):
    with open(filename, 'rb+') as f:
        last_base_offset = len(f.readline())
        f.seek(0)

        for j in range(1, string_count):
            f.seek(last_base_offset)
            k = f.readline()
            last_base_offset += len(k)
            f.seek(-len(k), 1)  # откатились в начало k
            get_previous_line(f)  # откатились к строке перед k

            a_i = f.readline()  # сравнение можно улучшить
            while a_i > k:

                f.seek(-len(a_i), 1)
                f.write(k + a_i)
                seek = f.seek(-(len(k) + len(a_i)), 1)
                if seek == 0:
                    break

                get_previous_line(f)
                a_i = f.readline()
