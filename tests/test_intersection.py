#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_intersection
----------------------------------
test Intersection functionality.

TODO: design test.
"""

import unittest
from ghoul import Intersection

class TestLists(unittest.TestCase):
    def test_ints(self):
        # 1 ∩ 1 == 1
        self.assertTrue(Intersection([1, 2, 3], [1, 2, 3]) == [1, 2, 3])
        # 1 ∩ 2 == 2
        self.assertTrue(Intersection([1, 2, 3], [1, 2]) == [1, 2])
        # 1 ∩ 2 == 1
        self.assertTrue(Intersection([1, 2], [1, 2, 3]) == [1, 2])
        # 1 ∩ 2 < 1 and 1 ∩ 2 < 2
        self.assertTrue(Intersection([1, 2, 3], [2, 3, 4]) == [2, 3])
        # 1 ∩ 2 == ∅
        self.assertIsNone(Intersection([1, 2, 3], [6, 7, 8]))
        # len(1 ∩ 2) == 1
        self.assertTrue(Intersection([1, 2, 3], [3]) == 3)
    def test_str(self):
        # 1 ∩ 1 == 1
        self.assertTrue(Intersection(['a', 'b', 'c'], ['a', 'b', 'c']) == ['a', 'b', 'c'])
        # 1 ∩ 2 == 2
        self.assertTrue(Intersection(['a', 'b', 'c'], ['b', 'c']) == ['b', 'c'])
        # 1 ∩ 2 == 1
        self.assertTrue(Intersection(['a', 'b'], ['a', 'b', 'c']) == ['a', 'b'])
        # 1 ∩ 2 < 1 and 1 ∩ 2 < 2
        self.assertTrue(Intersection(['a', 'b', 'c'], ['b', 'c', 'd']) == ['b', 'c'])
        # 1 ∩ 2 == ∅
        self.assertIsNone(Intersection(['a', 'b', 'c'], ['d', 'e', 'f']))
        # len(1 ∩ 2) == 1
        self.assertTrue(Intersection(['a', 'b', 'c'], ['a']) == 'a')
    # duplicates

class TestValues(unittest.TestCase):
    def test_ints(self):
        self.assertTrue(Intersection(1, 1) == 1)
        self.assertIsNone(Intersection(1, 2))
    def test_str(self):
        self.assertTrue(Intersection('a', 'a') == 'a')
        self.assertIsNone(Intersection('a', 'b'))

class TestAlgebraicProperties(unittest.TestCase):
    pass

if __name__ == '__main__':
  unittest.main()