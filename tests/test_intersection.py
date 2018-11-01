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

class TestValues(unittest.TestCase):
    def test_values(self):
        def _case_identical(*a):
            self.assertTrue(Intersection(a[0], a[0]) == a[0])
        def _case_nonidentical(*a):
            self.assertIsNone(Intersection(a[0], a[1]))

        value_sets = [
            [1, 2],
            ['a', 'b']
        ]
        cases = [_case_identical, _case_nonidentical]
        for values in value_sets:
            for case in cases:
                case(*values)


class TestLists(unittest.TestCase):

    def test(self):
        def _case1(*a):
            # A ∩ A == A
            self.assertTrue(Intersection([a[0], a[1], a[2]], [a[0], a[1], a[2]]) == [a[0], a[1], a[2]])
        def _case2(*a):
            # A ∩ B == B
            self.assertTrue(Intersection([a[0], a[1], a[2]], [a[0], a[1]]) == [a[0], a[1]])
        def _case3(*a):
            # A ∩ B == A
            self.assertTrue(Intersection([a[0], a[1]], [a[0], a[1], a[2]]) == [a[0], a[1]])
        def _case4(*a):
            # A ∩ B ⊂ A and A ∩ B ⊂ B
            self.assertTrue(Intersection([a[0], a[1], a[2]], [a[1], a[2], a[3]]) == [a[1], a[2]])
        def _case5(*a):
            # A ∩ B == ∅
            self.assertIsNone(Intersection([a[0], a[1], a[2]], [a[3], a[4], a[5]]))
        def _case6(*a):
            # len(A ∩ B) == 1
            self.assertTrue(Intersection([a[0], a[1], a[2]], [a[2]]) == a[2])
        def _case7(*a):
            # duplicates
            self.assertTrue(Intersection([a[0], a[0], a[1]], [a[0]]) == [a[0], a[0]])
            self.assertTrue(Intersection([a[0]], [a[0], a[0], a[1]]) == [a[0], a[0]])
    
        value_sets = [
            [1, 2, 3, 4, 5, 6],
            ['a', 'b', 'c', 'd', 'e', 'f']
        ]
        cases = [_case1, _case2, _case3, _case4, _case5, _case6, _case7]
        for values in value_sets:
            for case in cases:
                case(*values)
    

class TestSetAlgebra(unittest.TestCase):
    # commutative
    # A ∩ B = B ∩ A
    def _commutation(*a):
        self.assertTrue(Intersection(a[0], a[1]) == Intersection(a[1], a[0]))

    # associative
    # (A ∩ B) ∩ C = A ∩ (B ∩ C)

    # law of identity
    # A ∩ A = A

    # idempotent law
    

    # law of U
    # U ∩ A = A

    # distributive law
    # A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C)
    pass

if __name__ == '__main__':
  unittest.main()