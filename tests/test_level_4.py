import inspect, os, sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from timeout_decorator import timeout
import unittest
from my_db import MyDB


class Level4Tests(unittest.TestCase):
    """
    Tests for Level 4 (rollback).

    All have the same score.
    You are not allowed to modify this file, but feel free to read the source code to better understand what is happening in every specific case.
    """

    failureException = Exception

    @classmethod
    def setUp(cls):
        cls.mydb = MyDB()

    @timeout(0.4)
    def test_level_4_case_01_rollback_undoes_set(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(5, 'a', 'x', 2)
        self.mydb.rollback(3)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 1)

    @timeout(0.4)
    def test_level_4_case_02_operation_at_rollback_timestamp_is_kept(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(5, 'a', 'x', 2)
        self.mydb.rollback(5)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 2)

    @timeout(0.4)
    def test_level_4_case_03_rollback_removes_later_fields(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(5, 'b', 'y', 2)
        self.mydb.rollback(4)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(6, 'b', 'y'))
        self.assertEqual(self.mydb.find_median(), 1)

    @timeout(0.4)
    def test_level_4_case_04_rollback_restores_deleted_field(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.assertTrue(self.mydb.compare_and_delete(5, 'a', 'x', 1))
        self.assertIsNone(self.mydb.get(6, 'a', 'x'))
        self.mydb.rollback(4)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 1)

    @timeout(0.4)
    def test_level_4_case_05_rollback_undoes_compare_and_set(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.assertTrue(self.mydb.compare_and_set(5, 'a', 'x', 1, 2))
        self.assertTrue(self.mydb.compare_and_set(7, 'a', 'x', 2, 3))
        self.mydb.rollback(6)
        self.assertEqual(self.mydb.get(8, 'a', 'x'), 2)
        self.assertTrue(self.mydb.compare_and_set(9, 'a', 'x', 2, 4))
        self.assertEqual(self.mydb.get(10, 'a', 'x'), 4)

    @timeout(0.4)
    def test_level_4_case_06_rollback_before_everything_gives_empty_db(self):
        self.mydb.set(5, 'a', 'x', 1)
        self.mydb.set(6, 'b', 'y', 2)
        self.mydb.rollback(4)
        self.assertIsNone(self.mydb.get(7, 'a', 'x'))
        self.assertIsNone(self.mydb.get(7, 'b', 'y'))
        self.assertIsNone(self.mydb.find_median())

    @timeout(0.4)
    def test_level_4_case_07_rollback_keeps_remaining_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 10)
        self.mydb.set(5, 'b', 'y', 2)
        self.mydb.rollback(4)
        # a.x was set at t=0 with ttl 10, so it still expires at t=10
        self.assertEqual(self.mydb.get(9, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(10, 'a', 'x'))

    @timeout(0.4)
    def test_level_4_case_08_rollback_restores_old_ttl(self):
        self.mydb.set(0, 'a', 'x', 1, 10)
        self.mydb.set(5, 'a', 'x', 2, 100)
        self.assertEqual(self.mydb.get(50, 'a', 'x'), 2)
        self.mydb.rollback(6)
        self.assertEqual(self.mydb.get(50, 'a', 'x'), 2)
        self.mydb.rollback(4)
        # back to value 1 with the original ttl: alive until t=10
        self.assertEqual(self.mydb.get(9, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(10, 'a', 'x'))

    @timeout(0.4)
    def test_level_4_case_09_field_expired_at_rollback_time_is_gone(self):
        self.mydb.set(0, 'a', 'x', 1, 5)
        self.mydb.set(20, 'b', 'y', 2)
        self.mydb.rollback(10)
        self.assertIsNone(self.mydb.get(10, 'a', 'x'))
        self.assertIsNone(self.mydb.get(11, 'b', 'y'))

    @timeout(0.4)
    def test_level_4_case_10_rollback_resurrects_overwritten_expired_field(self):
        self.mydb.set(0, 'a', 'x', 1, 100)
        self.mydb.set(10, 'a', 'x', 2, 5)
        self.assertIsNone(self.mydb.get(15, 'a', 'x'))
        self.mydb.rollback(9)
        # the overwrite is discarded, so the original (ttl 100) is back
        self.assertEqual(self.mydb.get(15, 'a', 'x'), 1)
        self.assertEqual(self.mydb.get(99, 'a', 'x'), 1)
        self.assertIsNone(self.mydb.get(100, 'a', 'x'))

    @timeout(0.4)
    def test_level_4_case_11_operations_after_rollback_work(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(5, 'a', 'x', 2)
        self.mydb.rollback(3)
        self.mydb.set(4, 'a', 'y', 7)
        self.assertEqual(self.mydb.get(5, 'a', 'x'), 1)
        self.assertEqual(self.mydb.get(5, 'a', 'y'), 7)

    @timeout(0.4)
    def test_level_4_case_12_discarded_operations_stay_discarded(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(5, 'a', 'x', 2)
        self.mydb.rollback(3)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 1)
        # rolling "forward" does not bring the discarded set back
        self.mydb.rollback(10)
        self.assertEqual(self.mydb.get(11, 'a', 'x'), 1)

    @timeout(0.4)
    def test_level_4_case_13_multiple_rollbacks(self):
        self.mydb.set(1, 'a', 'x', 1)
        self.mydb.set(2, 'a', 'x', 2)
        self.mydb.set(3, 'a', 'x', 3)
        self.mydb.set(4, 'a', 'x', 4)
        self.mydb.rollback(3)
        self.assertEqual(self.mydb.get(5, 'a', 'x'), 3)
        self.mydb.rollback(2)
        self.assertEqual(self.mydb.get(6, 'a', 'x'), 2)
        self.mydb.rollback(1)
        self.assertEqual(self.mydb.get(7, 'a', 'x'), 1)

    @timeout(0.4)
    def test_level_4_case_14_rollback_with_median_and_ttl(self):
        self.mydb.set(0, 'a', 'x', 10, 20)
        self.mydb.set(1, 'b', 'x', 20)
        self.mydb.set(2, 'c', 'x', 30)
        self.mydb.set(30, 'd', 'x', 40)
        self.mydb.rollback(15)
        self.assertEqual(self.mydb.find_median(15), 20)
        # a.x expires at t=20, d.x was discarded -> values 20, 30
        self.assertEqual(self.mydb.find_median(20), 20)
        self.assertEqual(self.mydb.find_median(25), 20)
        self.assertIsNone(self.mydb.get(30, 'd', 'x'))
