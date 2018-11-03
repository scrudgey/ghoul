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
from itertools import combinations

# lists of lists?
# symbols?
VALUE_SETS = [
    [1, 2, 3, 4, 5, 6],
    ['a', 'b', 'c', 'd', 'e', 'f'],
    [1, 'a', 2, 'b', 3, 'c', 4]
]

class TestValues(unittest.TestCase):
    def test_values(self):
        def _case_identical(*a):
            self.assertTrue(Intersection(a[0], a[0]) == a[0])
        def _case_nonidentical(*a):
            self.assertIsNone(Intersection(a[0], a[1]))

        cases = [_case_identical, _case_nonidentical]
        for values in VALUE_SETS:
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
    
        cases = [_case1, _case2, _case3, _case4, _case5, _case6, _case7]
        for values in VALUE_SETS:
            for case in cases:
                case(*values)
    

class TestSetAlgebra(unittest.TestCase):
    def test_algebra(self):

        def _commutative(*a):
            # A ∩ B = B ∩ A
            self.assertTrue(Intersection(a[0], a[1]) == Intersection(a[1], a[0]))

        def _associative(*a):
            # (A ∩ B) ∩ C = A ∩ (B ∩ C)
            A = [a[0], a[1], a[2]]
            B = [a[1], a[2], a[3]]
            C = [a[4], a[2], a[1]]
            self.assertTrue(Intersection(Intersection(A, B), C) == Intersection(A, Intersection(B, C)))
        
        def _identity(*a):
            # A ∩ A = A
            for i in a:
                self.assertTrue(Intersection(i, i) == i)
        
        def _law_of_U(*a):
            # U ∩ A = A
            a = list(a)
            for n in range(2, len(a)-1):
                for subset in combinations(a, n):
                    subset = list(subset)
                    self.assertTrue(Intersection(a, subset) == subset)

        cases = [_commutative, _associative, _identity, _law_of_U]
        for values in VALUE_SETS:
            for case in cases:
                case(*values)


class TestSpecificBehavior(unittest.TestCase):
    def test_classes(self):
        pass

if __name__ == '__main__':
  unittest.main()