import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from my_db import MyDB


class Level2Tests(unittest.TestCase):
    """
    Tests for Level 2 (find_median).

    All have the same score.
    You are not allowed to modify this file, but feel free to read the source code to better understand what is happening in every specific case.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.mydb = MyDB()

    @timeout(0.4)
    def test_level_2_case_01_empty(self):
        self.assertIsNone(self.mydb.find_median())

    @timeout(0.4)
    def test_level_2_case_02_single_value(self):
        self.mydb.set(1, 'a', 'x', 42)
        self.assertEqual(self.mydb.find_median(), 42)

    @timeout(0.4)
    def test_level_2_case_03_odd_count(self):
        self.mydb.set(1, 'a', 'x', 5)
        self.mydb.set(2, 'b', 'x', 1)
        self.mydb.set(3, 'c', 'x', 9)
        self.assertEqual(self.mydb.find_median(), 5)

    @timeout(0.4)
    def test_level_2_case_04_even_count_returns_lower_middle(self):
        self.mydb.set(1, 'a', 'x', 10)
        self.mydb.set(2, 'b', 'x', 20)
        self.mydb.set(3, 'c', 'x', 30)
        self.mydb.set(4, 'd', 'x', 40)
        self.assertEqual(self.mydb.find_median(), 20)

    @timeout(0.4)
    def test_level_2_case_05_values_across_keys_and_fields(self):
        self.mydb.set(1, 'a', 'x', 3)
        self.mydb.set(2, 'a', 'y', 100)
        self.mydb.set(3, 'b', 'x', 1)
        self.mydb.set(4, 'b', 'z', 2)
        self.mydb.set(5, 'c', 'y', 50)
        # sorted: 1, 2, 3, 50, 100
        self.assertEqual(self.mydb.find_median(), 3)

    @timeout(0.4)
    def test_level_2_case_06_overwrite_does_not_duplicate(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(2, 'a', 'x', 100)
        self.mydb.set(3, 'b', 'x', 7)
        # values are 100 and 7 -> lower middle is 7
        self.assertEqual(self.mydb.find_median(), 7)

    @timeout(0.4)
    def test_level_2_case_07_compare_and_set_changes_median(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(2, 'b', 'x', 2)
        self.mydb.set(3, 'c', 'x', 3)
        self.assertEqual(self.mydb.find_median(), 2)
        self.assertTrue(self.mydb.compare_and_set(4, 'b', 'x', 2, 10))
        # 1, 3, 10
        self.assertEqual(self.mydb.find_median(), 3)

    @timeout(0.4)
    def test_level_2_case_08_delete_changes_median(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(2, 'b', 'x', 2)
        self.mydb.set(3, 'c', 'x', 3)
        self.mydb.set(4, 'd', 'x', 4)
        self.assertEqual(self.mydb.find_median(), 2)
        self.assertTrue(self.mydb.compare_and_delete(5, 'a', 'x', 1))
        # 2, 3, 4
        self.assertEqual(self.mydb.find_median(), 3)
        self.assertTrue(self.mydb.compare_and_delete(6, 'b', 'x', 2))
        self.assertTrue(self.mydb.compare_and_delete(7, 'c', 'x', 3))
        self.assertEqual(self.mydb.find_median(), 4)
        self.assertTrue(self.mydb.compare_and_delete(8, 'd', 'x', 4))
        self.assertIsNone(self.mydb.find_median())

    @timeout(0.4)
    def test_level_2_case_09_duplicate_values_and_negatives(self):
        self.mydb.set(1, 'a', 'x', 5)
        self.mydb.set(2, 'b', 'x', 5)
        self.mydb.set(3, 'c', 'x', -3)
        self.mydb.set(4, 'd', 'x', 5)
        self.mydb.set(5, 'e', 'x', -10)
        # sorted: -10, -3, 5, 5, 5
        self.assertEqual(self.mydb.find_median(), 5)

    @timeout(0.4)
    def test_level_2_case_10_many_values(self):
        for i in range(1, 202):
            self.mydb.set(i, 'k%d' % i, 'f', i)
        self.assertEqual(self.mydb.find_median(), 101)
        self.assertTrue(self.mydb.compare_and_delete(300, 'k1', 'f', 1))
        # 200 values, 2..201 -> lower middle is the 100th = 101
        self.assertEqual(self.mydb.find_median(), 101)
