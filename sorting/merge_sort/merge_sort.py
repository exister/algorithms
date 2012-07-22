# -*- coding: utf-8 -*-
"""
Merge sort
1. Split array into two half
2. Keep splitting each part until it'll become one element
3. Merge elements keeping order
4. Merge subarrays keeping order
"""

def merge(data, start_index, middle_index, end_index, reversed=False):
    import operator
    op = operator.ge if reversed else operator.le

    #copy left half of array
    left_array = data[start_index:middle_index+1]
    #copy right half of array
    right_array = data[middle_index+1:end_index+1]

    i = 0
    j = 0

    #loop through all indexes of current subarray
    for x in xrange(start_index, end_index + 1):
        #if all indexes from left array were checked, than copy element from right array
        if i == len(left_array):
            data[x] = right_array[j]
            j += 1
        #if all indexes from right array were checked, than copy element from left array
        elif j == len(right_array):
            data[x] = left_array[i]
            i += 1
        #else compare current elements in both arrays
        elif i < len(left_array) and j < len(right_array):
            if op(left_array[i], right_array[j]):
                data[x] = left_array[i]
                i += 1
            else:
                data[x] = right_array[j]
                j += 1

def _merge_sort(data, start_index, end_index, reversed=False):
    if start_index < end_index:
        #middle of array
        middle_index = (start_index + end_index) / 2
        #recursively call _merge_sort and pass left half of array
        _merge_sort(data, start_index, middle_index, reversed=reversed)
        #recursively call _merge_sort and pass right half of array
        _merge_sort(data, middle_index + 1, end_index, reversed=reversed)
        merge(data, start_index, middle_index, end_index, reversed=reversed)

def merge_sort(data, reversed=False):
    _merge_sort(data, 0, len(data) - 1, reversed=reversed)


if __name__ == '__main__':
    data = [
        [4, 2, 3, 1],
        [2, 56, 657, -323, 36, 76, 32, 5676, -23, 6, 0],
        [3, 54, 2, 89, 32, 546, 9878, 23],
        [234, 657, 23, 89, 3]
    ]
    for i, x in enumerate(data):
        x2 = x[:]
        merge_sort(x2, reversed=i%2)
        print '{0} {1} {2}'.format(i%2, x, x2)