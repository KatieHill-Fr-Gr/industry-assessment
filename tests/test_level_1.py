import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from my_db import MyDB


class Level1Tests(unittest.TestCase):
    """
    The test class below includes 11 tests for Level 1.

    All have the same score.
    You are not allowed to modify this file, but feel free to read the source code to better understand what is happening in every specific case.
    """

    failureException = Exception


    fixed_timestamp = 160000000

    @classmethod
    def setUp(cls):
        cls.mydb =  MyDB()

    @timeout(0.4)
    def test_level_1_case_01_simple_set_and_get_1(self):
        self.mydb.set(0, 'employee1', 'age', 20)
        self.mydb.set(1, 'employee1', 'age', 30)
        self.mydb.set(2, 'employee2', 'age', 21)
        self.assertEqual(self.mydb.get(3, 'employee1', 'age'), 30)

    @timeout(0.4)
    def test_level_1_case_02_simple_set_and_get_2(self):
        self.assertIsNone(self.mydb.get(10, 'dept4', 'floors'))
        self.assertIsNone(self.mydb.get(15, 'dept4', 'floors'))
        self.mydb.set(20, 'dept4', 'floors', 31)
        self.assertEqual(self.mydb.get(22, 'dept4', 'floors'), 31)
        self.assertEqual(self.mydb.get(23, 'dept4', 'floors'), 31)
        self.mydb.set(25, 'dept4', 'floors', 20)
        self.assertEqual(self.mydb.get(29, 'dept4', 'floors'), 20)

    @timeout(0.4)
    def test_level_1_case_03_simple_set_get_and_reset(self):
        self.mydb.set(10, 'item1', 'cost', 30)
        self.assertEqual(self.mydb.get(20, 'item1', 'cost'), 30)
        self.assertFalse(self.mydb.compare_and_set(30, 'item1', 'cost', 35, 42))
        self.assertEqual(self.mydb.get(40, 'item1', 'cost'), 30)
        self.assertTrue(self.mydb.compare_and_set(50, 'item1', 'cost', 30, 42))
        self.assertEqual(self.mydb.get(60, 'item1', 'cost'), 42)
        self.assertTrue(self.mydb.compare_and_delete(70, 'item1', 'cost', 42))
        self.assertIsNone(self.mydb.get(80, 'item1', 'cost'))

    @timeout(0.4)
    def test_level_1_case_04_multiple_objects_with_same_key(self):
        self.assertFalse(self.mydb.compare_and_set(0, 'worker1', 'experience', 0, 4))
        self.assertIsNone(self.mydb.get(1, 'worker1', 'experience'))
        self.mydb.set(2, 'worker1', 'experience', 4)
        self.mydb.set(3, 'worker1', 'age', 25)
        self.mydb.set(4, 'age', 'worker1', 2)
        self.assertEqual(self.mydb.get(5, 'worker1', 'age'), 25)
        self.assertEqual(self.mydb.get(6, 'worker1', 'experience'), 4)
        self.assertIsNone(self.mydb.get(7, 'worker1', 'height'))
        self.mydb.set(8, 'worker1', 'height', 170)
        self.mydb.set(9, 'worker1', 'height', 180)
        self.mydb.set(10, 'worker1', 'height', 190)
        self.assertEqual(self.mydb.get(11, 'worker1', 'experience'), 4)
        self.assertEqual(self.mydb.get(12, 'worker1', 'age'), 25)
        self.assertEqual(self.mydb.get(13, 'worker1', 'height'), 190)
        self.assertEqual(self.mydb.get(14, 'age', 'worker1'), 2)
        self.assertTrue(self.mydb.compare_and_set(15, 'worker1', 'age', 25, 27))
        self.assertFalse(self.mydb.compare_and_set(16, 'worker1', 'age', 25, 26))
        self.assertEqual(self.mydb.get(17, 'worker1', 'age'), 27)

    @timeout(0.4)
    def test_level_1_case_05_multiple_resets_and_deletes_1(self):
        self.mydb.set(self.fixed_timestamp, 'A', 'BC', 7)
        self.mydb.set(self.fixed_timestamp + 1, 'AB', 'C', 8)
        self.mydb.set(self.fixed_timestamp + 2, 'A', 'BC', 9)
        self.assertFalse(self.mydb.compare_and_delete(self.fixed_timestamp + 3, 'BC', 'A', 20))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 4, 'BC', 'A'))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 5, 'A', 'BC'), 9)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 6, 'AB', 'C'), 8)
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 7, 'A', 'BC', 9, 8))
        self.assertFalse(self.mydb.compare_and_delete(self.fixed_timestamp + 8, 'A', 'BC', 7))
        self.mydb.set(self.fixed_timestamp + 9, 'AB', 'C', 9)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 10, 'A', 'BC'), 8)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 11, 'AB', 'C'), 9)

    @timeout(0.4)
    def test_level_1_case_06_multiple_resets_and_deletes_2(self):
        self.mydb.set(self.fixed_timestamp + 10, 'foo', 'bar', 1)
        self.mydb.set(self.fixed_timestamp + 20, 'foo', 'two', 2)
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 30, 'foo', 'bar', 1, 3))
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 40, 'foo', 'bar', 31, 4))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 50, 'foo', 'bar'), 3)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 60, 'foo', 'two'), 2)
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 70, 'foo', 'two', 2, 50))
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 80, 'foo', 'bar', 3, 4))
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 90, 'foo', 'bar', 4, 5))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 100, 'foo', 'bar'), 5)
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 110, 'foo', 'bar', 5, 7))
        self.assertTrue(self.mydb.compare_and_delete(self.fixed_timestamp + 120, 'foo', 'bar', 7))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 130, 'foo', 'bar'))
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 140, 'foo', 'two', 5, 40))
        self.assertTrue(self.mydb.compare_and_set(self.fixed_timestamp + 150, 'foo', 'two', 50, 4))
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 160, 'foot', 'wo', 4, 7))
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 170, 'foo', 'bar', 7, 90))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 180, 'foo', 'bar'))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 190, 'foo', 'two'), 4)

    @timeout(0.4)
    def test_level_1_case_07_multiple_resets_and_deletes_3(self):
        self.mydb.set(1, 'key1', 'field1', 1)
        self.mydb.set(2, 'key1', 'field2', 2)
        self.mydb.set(3, 'key2', 'field1', 3)
        self.mydb.set(4, 'key3', 'field1', 4)
        self.mydb.set(5, 'key3', 'field2', 5)
        self.mydb.set(6, 'key3', 'field3', 6)
        self.assertTrue(self.mydb.compare_and_set(7, 'key1', 'field2', 2, 7))
        self.assertTrue(self.mydb.compare_and_set(8, 'key2', 'field1', 3, 8))
        self.assertTrue(self.mydb.compare_and_set(9, 'key3', 'field1', 4, 9))
        self.assertFalse(self.mydb.compare_and_set(10, 'key1', 'field1', 2, 3))
        self.assertFalse(self.mydb.compare_and_set(11, 'key1', 'field1', 0, 3))
        self.assertFalse(self.mydb.compare_and_set(12, 'key1', 'field1', 11, 3))
        self.assertFalse(self.mydb.compare_and_delete(13, 'key3', 'field2', 0))
        self.assertTrue(self.mydb.compare_and_delete(14, 'key2', 'field1', 8))
        self.assertFalse(self.mydb.compare_and_delete(15, 'key4', 'field1', 0))
        self.assertEqual(self.mydb.get(16, 'key1', 'field1'), 1)
        self.assertEqual(self.mydb.get(17, 'key1', 'field2'), 7)
        self.assertIsNone(self.mydb.get(18, 'key2', 'field1'))
        self.assertIsNone(self.mydb.get(19, 'key2', 'field2'))
        self.assertEqual(self.mydb.get(20, 'key3', 'field1'), 9)
        self.assertEqual(self.mydb.get(21, 'key3', 'field2'), 5)
        self.assertEqual(self.mydb.get(22, 'key3', 'field3'), 6)
        self.assertIsNone(self.mydb.get(23, 'key4', 'field1'))

    @timeout(0.4)
    def test_level_1_case_08_random_ordered_operations(self):
        self.assertFalse(self.mydb.compare_and_set(0, 'key', 'key', 0, 6))
        self.assertFalse(self.mydb.compare_and_delete(1, 'key', 'key2', 0))
        self.assertIsNone(self.mydb.get(2, 'key', 'key'))
        self.assertIsNone(self.mydb.get(3, 'key', 'key2'))
        self.mydb.set(4, 'key', 'key', 5)
        self.mydb.set(5, 'foo', 'bar', 1)
        self.mydb.set(6, 'key', 'key', 7)
        self.assertFalse(self.mydb.compare_and_delete(7, 'key', 'bar', 1))
        self.assertIsNone(self.mydb.get(8, 'key', 'key2'))
        self.assertEqual(self.mydb.get(9, 'key', 'key'), 7)
        self.assertIsNone(self.mydb.get(10, 'k', 'eykey'))
        self.assertFalse(self.mydb.compare_and_set(11, 'key', 'key', 5, 9))
        self.assertEqual(self.mydb.get(12, 'key', 'key'), 7)

    @timeout(0.4)
    def test_level_1_case_09_mixed_multiple_operations_1(self):
        self.mydb.set(self.fixed_timestamp, 'a', 'b', 1)
        self.mydb.set(self.fixed_timestamp + 1, 'a', 'c', 2)
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 2, 'c', 'a'))
        self.mydb.set(self.fixed_timestamp + 3, 'a', 'd', 3)
        self.assertFalse(self.mydb.compare_and_delete(self.fixed_timestamp + 4, 'a', 'c', 3))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 5, 'a', 'c'), 2)
        self.assertTrue(self.mydb.compare_and_delete(self.fixed_timestamp + 6, 'a', 'c', 2))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 7, 'a', 'c'))
        self.mydb.set(self.fixed_timestamp + 8, 'a', 'e', 4)
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 9, 'a', 'c', 0, 5))
        self.assertFalse(self.mydb.compare_and_set(self.fixed_timestamp + 10, 'a', 'c', 2, 5))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 11, 'a', 'c'))
        self.mydb.set(self.fixed_timestamp + 12, 'a', 'b', 4)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 13, 'a', 'b'), 4)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 14, 'a', 'd'), 3)

    @timeout(0.4)
    def test_level_1_case_10_mixed_multiple_operations_2(self):
        self.mydb.set(self.fixed_timestamp, 'a', 'a', 1)
        self.mydb.set(self.fixed_timestamp + 1, 'a', 'A', 2)
        # print(self.mydb.db)
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 2, 'a', 'a'), 1)
        self.assertFalse(self.mydb.compare_and_delete(self.fixed_timestamp + 3, 'a', 'a', 0))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 4, 'a', 'a'), 1)
        self.assertTrue(self.mydb.compare_and_delete(self.fixed_timestamp + 5, 'a', 'a', 1))
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 6, 'a', 'a'))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 7, 'a', 'A'), 2)
        self.assertTrue(self.mydb.compare_and_delete(self.fixed_timestamp + 8, 'a', 'A', 2))
        self.mydb.set(self.fixed_timestamp + 9, 'a', 'A', 7)
        self.mydb.set(self.fixed_timestamp + 10, 'a', 'A', 9)
        self.assertIsNone(self.mydb.get(self.fixed_timestamp + 11, 'a', 'a'))
        self.assertEqual(self.mydb.get(self.fixed_timestamp + 12, 'a', 'A'), 9)

    @timeout(0.4)
    def test_level_1_case_11_median(self):
        self.assertEqual(self.mydb.find_median(), None)
        self.mydb.set(self.fixed_timestamp + 1, 'a', 'A', 20)
        print(self.mydb.db)
        self.assertEqual(self.mydb.find_median(), 20)
