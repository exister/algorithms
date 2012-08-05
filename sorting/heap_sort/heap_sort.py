# -*- coding: utf-8 -*-

class Heap(object):
    def __init__(self, data):
        super(Heap, self).__init__()
        self.data = data
        self.heap_size = len(data)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def __iter__(self):
        return self.data

    def __repr__(self):
        return self.data.__repr__()

    def parent(self, i):
        if i > 0:
            return (i - 1) >> 1 if i % 2 else (i - 2) >> 1

    def right(self, i):
        return (i << 1) + 2 # 2 * i + 1

    def left(self, i):
        return (i << 1) + 1 # 2 * i

    def max_heapify(self, i):
        l = self.left(i)
        r = self.right(i)

        if l < self.heap_size and self.data[l] > self.data[i]:
            largest = l
        else:
            largest = i

        if r < self.heap_size and self.data[r] > self.data[largest]:
            largest = r

        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.max_heapify(largest)

    def build_max_heap(self):
        for i in range(len(self.data) / 2, -1, -1):
            self.max_heapify(i)

    def heap_sort(self):
        self.build_max_heap()
        for i in range(len(self.data) - 1, 0, -1):
            self.data[0], self.data[i] = self.data[i], self.data[0]
            self.heap_size -= 1
            self.max_heapify(0)


if __name__ == '__main__':
    a = Heap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
    a.heap_sort()
    print a

    b = Heap([23, 3, 6, 34, 567, 2, 423, 654, 2, 4, -1])
    b.heap_sort()
    print b