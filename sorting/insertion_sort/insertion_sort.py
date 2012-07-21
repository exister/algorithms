# -*- coding: utf-8 -*-
"""
Insertion sort

1. pick a number
2. put it in the resulted array at a correct position
3. pick next number
"""

def insertion_sort(data, reversed=False):
    import operator
    op = operator.lt if reversed else operator.gt

    for i, x in enumerate(data):
        #don't do anything for first element
        if i == 0:
            continue
        #index of previous element
        j = i - 1
        #moving from previous element to the beginning of the array
        #move each greater previous element by one position to the right
        while j >= 0 and op(data[j], x):
            data[j+1] = data[j]
            j -= 1
        #don't do rewrite if indexes are equal
        if j + 1 != i:
            #set x to the right position
            #j now contains index
            data[j+1] = x
    return data

if __name__ == '__main__':
    data = [
        [1, 4, 54, 23, 53, 7, 3],
        [456, 6],
        [-23, 4, 0, -45, 56],
        [3, -1, 5, 645]
    ]
    for i, x in enumerate(data):
        print '{0} {1} {2}'.format(i%2, x, insertion_sort(x[:], i%2))