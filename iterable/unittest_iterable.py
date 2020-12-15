import unittest

from iterable.functions import Function
from iterable.iteration import Iterable


class TestIterable(unittest.TestCase):
    def setUp(self):
        self.iterable = Iterable()
        self.my_functions = Function()

    @staticmethod
    def function(first_element, second_element):
        if first_element <= second_element:
            return True
        return False

    @staticmethod
    def criteria(element):
        if element % 2 == 0:
            return True
        return False

    def test_function(self):
        self.assertEqual(self.function(0, 1), True)
        self.assertEqual(self.function(1, 0), False)

    def test_criteria(self):
        self.assertEqual(self.criteria(10), True)
        self.assertEqual(self.criteria(3), False)

    def test_iterable(self):
        self.iterable.add(1)
        self.iterable.add(2)
        self.iterable.add(3)
        for index in range(1, 4):
            self.assertEqual(self.iterable[index - 1], index)

        length = len(self.iterable)
        self.assertEqual(length, 3)
        self.assertListEqual(self.iterable.getIterable(), [1, 2, 3])

        self.iterable.add(1)
        index = 0
        for elem in self.iterable:
            elem = elem + 1
            self.iterable[index] = elem
            index += 1
        self.assertListEqual(self.iterable.getIterable(), [2, 3, 4, 2])
        index = 3
        del self.iterable[index]


class TestFunction(unittest.TestCase):
    def setUp(self):
        self.list = [7, 3, 1, 9, 2, 8, 2, 6]
        self.my_functions = Function()

    @staticmethod
    def function(first_element, second_element):
        if first_element <= second_element:
            return True
        return False

    @staticmethod
    def criteria(element, parameter):
        if element % 2 == 0:
            return True
        return False

    def test_gnome_sort(self):
        sorted_list = self.my_functions.gnome_sort(self.list, self.function)
        self.assertListEqual(sorted_list, [1, 2, 2, 3, 6, 7, 8, 9])

    def test_filter(self):
        filtered_list = self.my_functions.filter(self.list, self.criteria)
        self.assertListEqual(filtered_list, [2, 8, 2, 6])
