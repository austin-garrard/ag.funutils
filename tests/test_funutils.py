from unittest import TestCase
import functools

from ag.funutils import fun

class TestFunutils(TestCase):

    def test_map(self):
        mapper = fun.map(lambda x: x + 1)

        result = mapper([1, 2, 3])

        self.assertEqual(list(result), [2, 3, 4])

    def test_map_with_tuples(self):
        mapper = fun.map(lambda k, v: (k, v+1))

        result = mapper([('one', 1), ('two', 2)])

        self.assertEqual(list(result), [('one', 2), ('two', 3)])

    def test_filter(self):
        filterer = fun.filter(lambda x: x > 2)

        result = filterer([1, 2, 3, 4])

        self.assertEqual(list(result), [3, 4])

    def test_filter_with_tuples(self):
        filterer = fun.filter(lambda k, v: k is 'two' and v is 2)

        result = filterer([('one', 1), ('two', 2)])

        self.assertEqual(list(result), [('two', 2)])

    def test_reduce(self):
        reducer = fun.reduce(lambda acc, x: acc + x)

        result = reducer([1, 2, 3])

        self.assertEqual(result, 6)

    def test_reduce_with_initial_value(self):
        reducer = fun.reduce(lambda acc, x: acc + x, 4)

        result = reducer([1, 2, 3])

        self.assertEqual(result, 10)

    def test_reduce_with_tuples(self):
        reducer = fun.reduce(lambda acc, k, v: acc + k + v, 0)

        result = reducer([(1, 2), (3, 4)])

        self.assertEqual(result, 10)

    def test_sort_with_defaults(self):
        sorter = fun.sort()

        result = sorter([2, 4, 3, 1])

        self.assertEqual(list(result), [1, 2, 3, 4])

    def test_sort_with_defaults_and_tuples(self):
        sorter = fun.sort()

        result = sorter([('key3', 1), ('key1', 2), ('key2', 3)])

        self.assertEqual(list(result), [('key1', 2), ('key2', 3), ('key3', 1)])

    def test_sort_in_reverse(self):
        sorter = fun.sort(reverse=True)

        result = sorter([2, 4, 3, 1])

        self.assertEqual(list(result), [4, 3, 2, 1])

    def test_sort_in_reverse_with_tuples(self):
        sorter = fun.sort(reverse=True)

        result = sorter([('key3', 1), ('key1', 2), ('key2', 3)])

        self.assertEqual(list(result), [('key3', 1), ('key2', 3), ('key1', 2)])

    def test_sort_with_key(self):
        sorter = fun.sort(lambda x: x[1])

        result = sorter([(1, "b"), (2, "a"), (3, "c")])

        self.assertEqual(list(result), [(2, "a"), (1, "b"), (3, "c")])

    def test_tap_with_list(self):
        side_effects = []
        tapper = fun.tap(lambda x: side_effects.append(x))

        result = tapper([1, 2, 3])

        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(side_effects[0].__str__(), "[1, 2, 3]")
        self.assertEqual(len(side_effects), 1)

    def test_tap_with_iterable(self):
        """In a chain, it's likely we'll receive lists as iterables.
        
        This is good for performance but bad for many tapping functions,
        most notably `print`. So, we convert it to a list.
        """
        side_effects = []
        tapper = fun.tap(lambda x: side_effects.append(x))

        result = tapper(iter([1, 2, 3]))

        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(side_effects[0].__str__(), "[1, 2, 3]")
        self.assertEqual(len(side_effects), 1)

    def test_tap_with_string(self):
        """strings are iterable, but we don't want to convert them to a list when tapping them"""
        side_effects = []
        tapper = fun.tap(lambda x: side_effects.append(x))

        result = tapper("abc")

        self.assertEqual(result, "abc")
        self.assertEqual(side_effects, ["abc"])

    def test_tap_each_with_list(self):
        side_effects = []
        tapper = fun.tap_each(lambda x: side_effects.append(x + 1))

        result = tapper([1, 2, 3])

        self.assertEqual(list(result), [1, 2, 3])
        self.assertEqual(side_effects, [2, 3, 4])

    def test_tap_each_with_string(self):
        side_effects = []
        tapper = fun.tap_each(lambda x: side_effects.append(x))

        result = tapper("abc")

        self.assertEqual(result, "abc")
        self.assertEqual(side_effects, ["abc"])

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

        side_effects = []
        save_value = fun.tap(side_effects.append)
        result = fun.chain(
            ["a", "b", "c", "d"],
            save_value, 
            *big_transform,
            save_value, 
            fun.sort(reverse=True),
            list
        )
        self.assertEqual(result, ["D1", "C1", "B1", "A1"])
        self.assertEqual(side_effects, [
            ["a", "b", "c", "d"],
            ["A1", "B1", "C1", "D1"]
        ])

        result = fun.chain(
            ["a", "b", "c", "d"],
            *big_transform,
            fun.reduce(lambda acc, x: acc + x),
        )
        self.assertEqual(result, "A1B1C1D1")

