from unittest import TestCase
import functools

import ag.funutils as fun

class TestFunutils(TestCase):

    def test_map(self):
        mapper = fun.map(lambda x: x + 1)

        result = mapper([1, 2, 3])

        self.assertEqual(list(result), [2, 3, 4])

    def test_filter(self):
        mapper = fun.filter(lambda x: x > 2)

        result = mapper([1, 2, 3, 4])

        self.assertEqual(list(result), [3, 4])

    def test_reduce(self):
        mapper = fun.reduce(lambda acc, x: acc + x)

        result = mapper([1, 2, 3])

        self.assertEqual(result, 6)

    def test_reduce_with_initial_value(self):
        mapper = fun.reduce(lambda acc, x: acc + x, 4)

        result = mapper([1, 2, 3])

        self.assertEqual(result, 10)

    def test_sort_with_defaults(self):
        sorter = fun.sort()

        result = sorter([2, 4, 3, 1])

        self.assertEqual(list(result), [1, 2, 3, 4])

    def test_sort_in_reverse(self):
        sorter = fun.sort(reverse=True)

        result = sorter([2, 4, 3, 1])

        self.assertEqual(list(result), [4, 3, 2, 1])

    def test_sort_with_key(self):
        sorter = fun.sort(lambda x: x[1])

        result = sorter([(1, "b"), (2, "a"), (3, "c")])

        self.assertEqual(list(result), [(2, "a"), (1, "b"), (3, "c")])

    def test_chain(self):
        add_one = fun.map(lambda x: x + "1")
        upper = fun.map(str.upper)

        result = fun.chain(
            ["a", "b", "c", "d"],
            add_one,
            upper,
            list
        )
        self.assertEqual(result, ["A1", "B1", "C1", "D1"])

        big_transform = [add_one, upper]

        result = fun.chain(
            ["a", "b", "c", "d"],
            *big_transform,
            list
        )
        self.assertEqual(result, ["A1", "B1", "C1", "D1"])

        result = fun.chain(
            ["a", "b", "c", "d"],
            *big_transform,
            fun.filter(lambda x: x < "C1"),
            list
        )
        self.assertEqual(result, ["A1", "B1"])

        result = fun.chain(
            ["a", "b", "c", "d"],
            *big_transform,
            fun.sort(reverse=True),
            list
        )
        self.assertEqual(result, ["D1", "C1", "B1", "A1"])

