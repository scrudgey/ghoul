#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_collapse
----------------------------------

Basic tests for `ghoul` module.

test framework
   different object trees / minimal test tree
   notebook vs standalone

 ✓ test collapse
 ✓ test selective collapse
 ✓ test collapsing to multiple values
 ✓ test collapsing simultaneous
 test collapsing to subclass
 test improper collapse catching

 ✓ test attribute removal
 ✓ test attribute adoption
"""

import unittest
from ghoul import Symbol
from ghoul import symbol_includes, symbol_includes_all, symbol_includes_any

class A(object):
    def __init__(self):
        self.P = Symbol(P)
        
class P(object):
    pass

class P1(P):
    pass

class SubP(P):
    pass

class P2(SubP):
    def __init__(self):
        self.attr = 'test2'
    pass

class P3(SubP):
    def __init__(self):
        self.attr = 'test3'

class SubclassTest(unittest.TestCase):
    def runTest(self):
        self.A = Symbol(A)
        self.assertTrue('attr' in dir(self.A.P))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P2]))
        self.A.P.Collapse(P1)
        self.assertTrue('attr' not in dir(self.A.P))

if __name__ == '__main__':
  unittest.main()


# interpret
# interpret parse=False
# parse
# nested parse
