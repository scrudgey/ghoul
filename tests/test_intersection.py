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

class TestListIntersection(unittest.TestCase):
    def test_list(self):
        a = [1, 2, 3]
        b = [1, 2, 3]
        self.assertTrue(Intersection(a, b) == a)

if __name__ == '__main__':
  unittest.main()