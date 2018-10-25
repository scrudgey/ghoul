#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_collapse
----------------------------------

testing of basic collapsing features for `ghouls` module.

tests:
 ✓ test collapse
 ✓ test selective collapse
 ✓ test collapsing to multiple values
 ✓ test collapsing simultaneous
 test improper collapse catching

"""

import unittest
from ghoul import Symbol
from ghoul import symbol_includes, symbol_includes_all, symbol_includes_any

class Q(object):
    pass
class Q1(Q):
    pass
class Q2(Q):
    pass
class Q3(Q):
    pass

class P(object):
    pass
class P1(P):
    def __init__(self):
        self.Q = Q1()
class P2(P):
    def __init__(self):
        self.Q = Symbol([Q1(), Q2()])
class P3(P):
    def __init__(self):
        self.Q = Symbol([Q2(), Q3()])


class A(object):
    pass
class A1(A):
    def __init__(self):
        self.P = P1()
class A2(A):
    def __init__(self):
        self.P = Symbol([P1(), P2()])
class A3(A):
    def __init__(self):
        self.P = P3()


class SymbolTest(unittest.TestCase):
    def setUp(self):
        self.A = Symbol(A)
        
    def collapse(self, symbol, val):
        self.setUp()
        symbol.Collapse(val)
        if val is type:
            self.assertTrue(symbol_includes(symbol, val))
        if val is list:
            self.assertTrue(symbol_includes_all(symbol, val))
    def collapse_Q(self, q):
        self.setUp()
        self.A.P.Q.Collapse(q)
        if q is type:
            self.assertTrue(symbol_includes(self.A.P.Q, q))
        if q is list:
            self.assertTrue(symbol_includes_all(self.A.P.Q, q))
    def collapse_P(self, p):
        self.setUp()
        self.A.P.Collapse(p)
        if type(p) is type:
            self.assertTrue(symbol_includes(self.A.P, p))
        if type(p) is list:
            self.assertTrue(symbol_includes_all(self.A.P, p))
    def collapse_A(self, a):
        self.setUp()
        self.A.Collapse(a)
        if type(a) is type:
            self.assertTrue(symbol_includes(self.A, a))
        if type(a) is list:
            self.assertTrue(symbol_includes_all(self.A, a))


class TestCollapse(SymbolTest):
    def test_A(self):        
        def _test_A1():
            self.collapse_A(A1)
            # P
            self.assertTrue(symbol_includes(self.A.P, P1))
            self.assertFalse(symbol_includes_any(self.A.P, [P2, P3]))
            # Q
            self.assertTrue(symbol_includes(self.A.P.Q, Q1))
            self.assertFalse(symbol_includes_any(self.A.P.Q, [Q2, Q3]))
        def _test_A2():
            self.collapse_A(A2)
            # P
            self.assertTrue(symbol_includes_all(self.A.P, [P1, P2]))
            self.assertFalse(symbol_includes(self.A.P, P3))
            # Q
            self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2]))
            self.assertFalse(symbol_includes(self.A.P.Q, Q3))
        def _test_A3():
            self.collapse_A(A3)
            # P
            self.assertTrue(symbol_includes(self.A.P, P3))
            self.assertFalse(symbol_includes_any(self.A.P, [P1, P2]))
            # Q
            self.assertTrue(symbol_includes_all(self.A.P.Q, [Q2, Q3]))
            self.assertFalse(symbol_includes(self.A.P.Q, Q1))
        _test_A1()
        _test_A2()
        _test_A3()
    def test_P(self):        
        def _test_P1():
            self.collapse_P(P1)
            # A
            self.assertTrue(symbol_includes_all(self.A, [A1, A2]))
            self.assertFalse(symbol_includes(self.A, A3))
            # Q
            self.assertTrue(symbol_includes(self.A.P.Q, Q1))
            self.assertFalse(symbol_includes_any(self.A.P.Q, [Q2, Q3]))
        def _test_P2():
            self.collapse_P(P2)
            # A
            self.assertTrue(symbol_includes(self.A, A2))
            self.assertFalse(symbol_includes_any(self.A, [A1, A3]))
            # Q
            self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2]))
            self.assertFalse(symbol_includes(self.A.P.Q, Q3))
        def _test_P3():
            self.collapse_P(P3)
            # A
            self.assertTrue(symbol_includes(self.A, A3))
            self.assertFalse(symbol_includes_any(self.A, [A1, A2]))
            # Q
            self.assertTrue(symbol_includes_all(self.A.P.Q, [Q2, Q3]))
            self.assertFalse(symbol_includes(self.A.P.Q, Q1))
        _test_P1()
        _test_P2()
        _test_P3()
    def test_Q(self):
        def _test_Q1():
            self.collapse_Q(Q1)
            # A
            self.assertTrue(symbol_includes_all(self.A, [A1, A2]))
            self.assertFalse(symbol_includes(self.A, A3))
            # P
            self.assertTrue(symbol_includes_all(self.A.P, [P1, P2]))
            self.assertFalse(symbol_includes(self.A.P, P3))
        def _test_Q2():
            self.collapse_Q(Q2)
            # A
            self.assertTrue(symbol_includes_all(self.A, [A2, A3]))
            self.assertFalse(symbol_includes(self.A, A1))
            # P
            self.assertTrue(symbol_includes_all(self.A.P, [P2, P3]))
            self.assertFalse(symbol_includes(self.A.P, P1))
        def _test_Q3():
            self.collapse_Q(Q3)
            # A
            self.assertTrue(symbol_includes(self.A, A3))
            self.assertFalse(symbol_includes_any(self.A, [A1, A2]))
            # P
            self.assertTrue(symbol_includes(self.A.P, P3))
            self.assertFalse(symbol_includes_any(self.A.P, [P1, P2]))
        _test_Q1()
        _test_Q2()
        _test_Q3()

class TestMulti(SymbolTest):
    def test_Q(self):
        self.collapse_Q([Q1, Q2])
        self.assertFalse(symbol_includes(self.A.P.Q, Q3))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P2, P3]))
        self.assertTrue(symbol_includes_all(self.A, [A1, A2, A3]))
        
        self.collapse_Q([Q1, Q3])
        self.assertFalse(symbol_includes(self.A.P.Q, Q2))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P2, P3]))
        self.assertTrue(symbol_includes_all(self.A, [A1, A2, A3]))
        
        self.collapse_Q([Q2, Q3])
        self.assertFalse(symbol_includes(self.A.P.Q, Q1))
        self.assertTrue(symbol_includes_all(self.A.P, [P2, P3]))
        self.assertFalse(symbol_includes(self.A.P, P1))
        self.assertTrue(symbol_includes_all(self.A, [A2, A3]))
        self.assertFalse(symbol_includes(self.A, A1))
        
    def test_P(self):
        self.collapse_P([P1, P2])
        self.assertFalse(symbol_includes(self.A.P, P3))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2]))
        self.assertFalse(symbol_includes(self.A.P.Q, Q3))
        self.assertTrue(symbol_includes_all(self.A, [A1, A2]))
        self.assertFalse(symbol_includes(self.A, A3))
        
        self.collapse_P([P1, P3])
        self.assertFalse(symbol_includes(self.A.P, P2))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2, Q3]))
        self.assertTrue(symbol_includes_all(self.A, [A1, A2, A3]))
        
        self.collapse_P([P2, P3])
        self.assertFalse(symbol_includes(self.A.P, P1))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2, Q3]))
        self.assertTrue(symbol_includes_all(self.A, [A2, A3]))
        self.assertFalse(symbol_includes(self.A, A1))
    
    def test_A(self):
        self.collapse_A([A1, A2])
        self.assertFalse(symbol_includes(self.A, A3))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P2]))
        self.assertFalse(symbol_includes(self.A.P, P3))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2]))
        self.assertFalse(symbol_includes(self.A.P.Q, Q3))
        
        self.collapse_A([A1, A3])
        self.assertFalse(symbol_includes(self.A, A2))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2, Q3]))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P3]))
        self.assertFalse(symbol_includes(self.A.P, P2))
        
        self.collapse_A([A2, A3])
        self.assertFalse(symbol_includes(self.A, A1))
        self.assertTrue(symbol_includes_all(self.A.P.Q, [Q1, Q2, Q3]))
        self.assertTrue(symbol_includes_all(self.A.P, [P1, P2, P3]))

class TestSimultaneous(unittest.TestCase):
    def runTest(self):
        a = Symbol(A)
        a2 = Symbol(A)
        a2.Collapse([A2, A3])
        self.assertTrue(symbol_includes_all(a2, [A2, A3]))
        self.assertFalse(symbol_includes(a2, A1))
        a2.P.Q.Collapse(Q2)
        self.assertTrue(symbol_includes_all(a2.P, [P2, P3]))
        self.assertFalse(symbol_includes(a2.P, P1))
        self.assertTrue(symbol_includes(a2.P.Q, Q2))
        self.assertFalse(symbol_includes_any(a2.P.Q, [Q1, Q3]))
        a.Collapse(a2)
        # a2.P should restrict a.P
        self.assertFalse(symbol_includes(a.P, P1))
        # a2.P.Q should restrict a.P.Q
        self.assertFalse(symbol_includes_any(a.P.Q, [Q1, Q3]))

if __name__ == '__main__':
  unittest.main()
