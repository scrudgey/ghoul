#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_methods
----------------------------------

testing method generalization.

tests:
 ✓ test method scoping
 ✓ test method inheriting

"""

import unittest
from ghoul import Symbol

class MyObject(object):
    def f(self):
        return 'MyObject.f'

class Fruit(MyObject):
    def f(self):
        return 'Fruit.f'
    def h(self):
        return 'Fruit.h'

class Apple(Fruit):
    def f(self):
        return 'Apple.f'
    def g(self):
        return 'Apple.g'
    
class Pear(Fruit):
    def f(self):
        return 'Pear.f'
    def g(self):
        return 'Pear.g'

class TennisRacket(MyObject):
    def f(self):
        return 'TennisRacket.f'

class TestMethods(unittest.TestCase):
    def test_A(self):
        a = Symbol([Apple(), Pear(), TennisRacket()])
        # TODO: explain
        self.assertTrue(hasattr(a, 'f'))
        self.assertFalse(hasattr(a, 'h'))
        self.assertFalse(hasattr(a, 'g'))
        self.assertTrue(a.f() == 'MyObject.f')

        a.Collapse(Fruit)
        self.assertTrue(hasattr(a, 'f'))
        self.assertTrue(hasattr(a, 'h'))
        self.assertFalse(hasattr(a, 'g'))
        self.assertTrue(a.f() == 'Fruit.f')
        self.assertTrue(a.h() == 'Fruit.h')

        a.Collapse(Apple)
        self.assertTrue(hasattr(a, 'f'))
        self.assertTrue(hasattr(a, 'h'))
        self.assertTrue(hasattr(a, 'g'))
        self.assertTrue(a.f() == 'Apple.f')
        self.assertTrue(a.h() == 'Fruit.h')
        self.assertTrue(a.g() == 'Apple.g')

if __name__ == '__main__':
  unittest.main()
