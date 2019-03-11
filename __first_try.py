import math

def eval_left_bound(n):
    d, m = divmod(n+1,2)
    return d-1

def eval_swap_bound(n):
    d, m = divmod(n+1,2)
    return d+1


class SortableFile():

    def __init__(self, array, string_count, max_length):
        self.array = array
        self.string_count = string_count
        self.max_length = max_length
        self.sort_depth = int(math.log2(self.string_count))

    def merge(self, left_idx, right_idx):

        (b_i, b_l), (c_i, c_l) = left_idx, right_idx

        result = []
        while b_i < b_l and c_i < c_l:

            if self.array[b_i] < self.array[c_i]:
                result.append(self.array[b_i])
                b_i += 1
            else:
                result.append(self.array[c_i])
                c_i += 1

        if b_i < b_l:
            result.extend(self.array[b_i:b_l])
        if c_i < c_l:
            result.extend(self.array[c_i:c_l])

        self.array[left_idx[0]: right_idx[1]] = result

    def merge_sort(self):
        for i in range(0, self.sort_depth):
            size = 2 ** i
            for j in range(0, self.string_count, 2 ** (i + 1)):
                self.merge(
                    (j, min(self.string_count, j + size)),
                    (j + size, min(self.string_count, j + 2 * size))
                )

    def inplace_merge(self, left_idx, right_idx, swap_idx):
        (b_i, b_l), (c_i, c_l) = left_idx, right_idx
        (sw_i, sw_l) = swap_idx
        _sw_i = sw_i
        result = self.array  # self.array[sw_i:sw_l]

        while b_i < b_l and c_i < c_l:

            if self.array[b_i] < self.array[c_i]:
                result[sw_i], self.array[b_i] = self.array[b_i], result[sw_i]
                b_i += 1
            else:
                result[sw_i], self.array[c_i] = self.array[c_i], result[sw_i]
                c_i += 1

            sw_i += 1

        if b_i < b_l:
            self.array[b_i:b_l], result[sw_i:sw_i + b_l - b_i] = result[sw_i:sw_i + b_l - b_i], self.array[b_i:b_l]
        if c_i < c_l:
            self.array[c_i:c_l], result[sw_i:sw_i + c_l - c_i] = result[sw_i:sw_i + c_l - c_i], self.array[c_i:c_l]

        (
            self.array[_sw_i:_sw_i + right_idx[1] - left_idx[0]],
            self.array[left_idx[0]: right_idx[1]]
        ) = (
            self.array[left_idx[0]: right_idx[1]],
            self.array[_sw_i:_sw_i + right_idx[1] - left_idx[0]]
        )

    def inplace_merge_overclap(self, left_idx, right_idx, swap_idx):
        b_i, b_l = left_idx
        c_i, c_l = right_idx
        s_i, s_l = swap_idx

        while b_i <= b_l and c_i <= c_l:
            if ((left_idx, right_idx, swap_idx) == ((0, 2), (4, 39), [3, 39])):
                print('#', self.array[b_i], self.array[c_i])
            if self.array[b_i] < self.array[c_i]:
                self.array[b_i], self.array[s_i] = self.array[s_i], self.array[b_i]
                b_i += 1
            else:
                self.array[c_i], self.array[s_i] = self.array[s_i], self.array[c_i]
                c_i += 1
            s_i += 1

        while b_i <= b_l:
            self.array[b_i], self.array[s_i] = self.array[s_i], self.array[b_i]
            b_i += 1
            s_i += 1

        while c_i <= c_l:
            self.array[c_i], self.array[s_i] = self.array[s_i], self.array[c_i]
            c_i += 1
            s_i += 1

    def sort_right_part(self):
        last_idx = self.string_count - 1
        first_idx = (last_idx // 2) + 1
        swap_first = 0
        swap_last = swap_first + (last_idx - first_idx)

        for i in range(self.sort_depth + 1):
            size = 2 ** i
            for j in range(first_idx, last_idx + 1, size * 2):
                first_right_bound = min(j + 2 * size, self.string_count)
                second_right_bound = min(j + 2 * size, self.string_count)
                if j + size > second_right_bound:
                    break
                self.inplace_merge(
                    (j, min(j + size, self.string_count)),
                    (j + size, second_right_bound),
                    (swap_first, swap_last)
                )

    def sort_left_part(self, last_unsorted_idx):
        last_idx = self.string_count - 1
        #         last_unsorted_idx = (last_idx//2)
        last_left_idx = eval_left_bound(last_unsorted_idx)  # //2)
        swap_first = last_left_idx + 1
        swap_last = last_unsorted_idx
        first_idx = 0

        for i in range(self.sort_depth):
            size = 2 ** i
            for j in range(first_idx, last_idx + 1, size * 2):
                first_right_bound = min(j + 2 * size, last_left_idx + 1)
                second_rgiht_bound = min(j + 2 * size, last_left_idx + 1)
                if j + size > second_rgiht_bound:
                    break
                self.inplace_merge(
                    (j, min(j + size, self.string_count)),
                    (j + size, second_rgiht_bound),
                    (swap_first, swap_last)
                )

    def insert_last_element(self):
        pass

    def inplace_merge_sort(self):

        self.sort_right_part()
        last_unsorted_idx = (self.string_count - 1) // 2
        self.sort_left_part(last_unsorted_idx=last_unsorted_idx)

        # left
        last_idx = self.string_count - 1
        last_unsorted_idx = (last_idx // 2)
        last_left_idx = eval_left_bound(last_unsorted_idx)  # //2)
        # right
        first_right_idx = (last_idx // 2) + 1

        swap_first = first_right_idx - (1 + last_left_idx)  # eval_swap_bound(last_unsorted_idx)
        swap_last = self.string_count - 1

        self.inplace_merge_overclap(
            [0, last_left_idx],
            [first_right_idx, self.string_count - 1],
            [swap_first, swap_last]
        )

        while swap_first - last_left_idx >= 1 and last_left_idx >= 0:
            first_right_idx = swap_first
            last_unsorted_idx = swap_first - 1
            self.sort_left_part(last_unsorted_idx=last_unsorted_idx)
            last_left_idx = eval_left_bound(last_unsorted_idx)
            swap_first = first_right_idx - (1 + last_left_idx)
            self.inplace_merge_overclap(
                [0, last_left_idx],
                [first_right_idx, self.string_count - 1],
                [swap_first, swap_last]
            )

        left_border = 1
        right_border = self.string_count - 1
        m = (right_border + left_border) // 2
        insert_index = 0
        flag = False
        while right_border - left_border > 1:
            m = (right_border + left_border) // 2
            #             print(left_border, m, right_border)

            if self.array[0] > self.array[m]:
                left_border = m
            elif self.array[0] < self.array[m]:
                right_border = m
            else:
                insert_index = m
                flag = True
                break

        if not flag:
            if self.array[0] > self.array[right_border]:
                insert_index = right_border
            if self.array[left_border] < self.array[0] <= self.array[right_border]:
                insert_index = left_border

        s = self.array[0]
        for i in range(insert_index):
            self.array[i] = self.array[i + 1]
        self.array[insert_index] = s

    def __repr__(self):
        return ' '.join(map(lambda x: '%2i' % x, self.array))


if __name__ == '__main__':
    a = sorted(list(range(31)), key= lambda x: -x)
    string_count = len(a)

    sf = SortableFile(array=a, string_count=string_count, max_length=2)
    print(sf)
    sf.inplace_merge_sort()
    print(sf)

