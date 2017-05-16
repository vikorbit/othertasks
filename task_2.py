#!/usr/bin/python

import sys

import unittest


def get_split_index(n, m):
    if type(n) is not int:
        raise ValueError('type(n) is not int')

    if type(m) is not int:
        raise ValueError('type(m) is not int')

    if n <= 0:
        raise ValueError('n can not to be less or equal 0 (n={})'.format(n))

    if m <= 0:
        raise ValueError('m can not to be less or equal 0 (m={})'.format(m))

    if m > n:
        raise ValueError('m can not to more than n (n={}, m={})'.format(n, m))

    index = []

    k = (n - n % m) / m
    i = (n - k * m) / 2
    end = i + k * m
    while i < end:
        index.append([i, i + k - 1])
        i += k

    return index


class TestSpliter(unittest.TestCase):
    """tests for function get_split_index"""

    def test(self):

        with self.assertRaises(ValueError):
            get_split_index('test', 1)

        with self.assertRaises(ValueError):
            get_split_index(10, 'test')

        with self.assertRaises(ValueError):
            get_split_index(0, 1)

        with self.assertRaises(ValueError):
            get_split_index(-10, 1)

        with self.assertRaises(ValueError):
            get_split_index(10, -1)

        with self.assertRaises(ValueError):
            get_split_index(10, 0)

        with self.assertRaises(ValueError):
            get_split_index(10, 11)

        self.assertEqual(get_split_index(10, 1), [[0, 9]])
        self.assertEqual(get_split_index(10, 2), [[0, 4], [5, 9]])
        self.assertEqual(get_split_index(10, 3), [[0, 2], [3, 5], [6, 8]])
        self.assertEqual(get_split_index(10, 4), [
                         [1, 2], [3, 4], [5, 6], [7, 8]])
        self.assertEqual(get_split_index(10, 5), [
                         [0, 1], [2, 3], [4, 5], [6, 7], [8, 9]])
        self.assertEqual(get_split_index(10, 6), [
                         [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
        self.assertEqual(get_split_index(10, 7), [[1, 1], [2, 2], [
                         3, 3], [4, 4], [5, 5], [6, 6], [7, 7]])
        self.assertEqual(get_split_index(10, 8), [[1, 1], [2, 2], [
                         3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8]])
        self.assertEqual(get_split_index(10, 9), [[0, 0], [1, 1], [2, 2], [
                         3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8]])
        self.assertEqual(get_split_index(10, 10), [[0, 0], [1, 1], [2, 2], [
                         3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]])


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSpliter)
    unittest.TextTestRunner().run(suite)
