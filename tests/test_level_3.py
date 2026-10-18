import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from my_db import MyDB


class Level3Tests(unittest.TestCase):
    """
    Tests for Level 3 (TTL).

    All have the same score.
    You are not allowed to modify this file, but feel free to read the source code to better understand what is happening in every specific case.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.mydb = MyDB()

    @timeout(0.4)
    def test_level_3_case_01_no_ttl_lives_forever(self):
        self.mydb.set(0, 'a', 'x', 1)
        self.assertEqual(self.mydb.get(10 ** 9, 'a', 'x'), 1)

    @timeout(0.4)
    def test_level_3_case_02_ttl_boundaries(self):
        self.mydb.set(10, 'a', 'x', 1, 5)
        self.assertEqual(self.mydb.get(10, 'a', 'x'), 1)
        self.assertEqual(self.mydb.get(14, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(15, 'a', 'x'))
        self.assertIsNone(self.mydb.get(100, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_03_ttl_as_keyword(self):
        self.mydb.set(0, 'a', 'x', 1, ttl=3)
        self.assertEqual(self.mydb.get(2, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(3, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_04_overwrite_replaces_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.mydb.set(3, 'a', 'x', 2, 10)
        # old ttl would have expired at 5, new one runs until 13
        self.assertEqual(self.mydb.get(5, 'a', 'x'), 2)
        self.assertEqual(self.mydb.get(12, 'a', 'x'), 2)
        self.assertIsNone(self.mydb.get(13, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_05_overwrite_without_ttl_makes_infinite(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.mydb.set(3, 'a', 'x', 2)
        self.assertEqual(self.mydb.get(1000, 'a', 'x'), 2)

    @timeout(0.4)
    def test_level_3_case_06_set_after_expiry_recreates_field(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.assertIsNone(self.mydb.get(6, 'a', 'x'))
        self.mydb.set(7, 'a', 'x', 9, 5)
        self.assertEqual(self.mydb.get(8, 'a', 'x'), 9)
        self.assertEqual(self.mydb.get(11, 'a', 'x'), 9)
        self.assertIsNone(self.mydb.get(12, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_07_ttl_is_per_field(self):
        self.mydb.set(0, 'a', 'short', 1, 5)
        self.mydb.set(0, 'a', 'long', 2, 50)
        self.mydb.set(0, 'a', 'forever', 3)
        self.assertIsNone(self.mydb.get(5, 'a', 'short'))
        self.assertEqual(self.mydb.get(5, 'a', 'long'), 2)
        self.assertEqual(self.mydb.get(5, 'a', 'forever'), 3)
        self.assertIsNone(self.mydb.get(50, 'a', 'long'))
        self.assertEqual(self.mydb.get(50, 'a', 'forever'), 3)

    @timeout(0.4)
    def test_level_3_case_08_compare_and_set_on_expired_fails(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.assertTrue(self.mydb.compare_and_set(4, 'a', 'x', 1, 2))
        # the successful CAS at t=4 had no ttl -> now infinite
        self.assertEqual(self.mydb.get(100, 'a', 'x'), 2)

        self.mydb.set(10, 'b', 'x', 1, 5)
        self.assertFalse(self.mydb.compare_and_set(15, 'b', 'x', 1, 2))
        self.assertIsNone(self.mydb.get(15, 'b', 'x'))

    @timeout(0.4)
    def test_level_3_case_09_compare_and_set_resets_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 10)
        self.assertTrue(self.mydb.compare_and_set(5, 'a', 'x', 1, 2, 10))
        self.assertEqual(self.mydb.get(14, 'a', 'x'), 2)
        self.assertEqual(self.mydb.get(14, 'a', 'x'), 2)
        self.assertIsNone(self.mydb.get(15, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_10_failed_compare_and_set_keeps_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 10)
        self.assertFalse(self.mydb.compare_and_set(5, 'a', 'x', 99, 2, 100))
        self.assertEqual(self.mydb.get(9, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(10, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_11_compare_and_delete_respects_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.assertTrue(self.mydb.compare_and_delete(4, 'a', 'x', 1))
        self.mydb.set(10, 'a', 'x', 1, 5)
        self.assertFalse(self.mydb.compare_and_delete(15, 'a', 'x', 1))
        self.assertIsNone(self.mydb.get(15, 'a', 'x'))

    @timeout(0.4)
    def test_level_3_case_12_find_median_ignores_expired(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.mydb.set(0, 'b', 'x', 2)
        self.mydb.set(0, 'c', 'x', 3)
        self.assertEqual(self.mydb.find_median(0), 2)
        self.assertEqual(self.mydb.find_median(4), 2)
        # at t=5 the value 1 is gone: values 2, 3 -> lower middle 2
        self.assertEqual(self.mydb.find_median(5), 2)

    @timeout(0.4)
    def test_level_3_case_13_find_median_all_expired(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.mydb.set(0, 'b', 'x', 2, 6)
        self.assertEqual(self.mydb.find_median(5), 2)
        self.assertIsNone(self.mydb.find_median(6))

    @timeout(0.4)
    def test_level_3_case_14_find_median_without_timestamp_ignores_ttl(self):
        self.mydb.set(0, 'a', 'x', 10, 1)
        self.mydb.set(0, 'b', 'x', 20, 1)
        self.mydb.set(0, 'c', 'x', 30, 1)
        self.assertEqual(self.mydb.find_median(), 20)
