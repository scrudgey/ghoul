# -*- coding: utf-8 -*-

"""Top-level package for ghoul."""

__author__ = """Ryan Foltz"""
__email__ = 'scrudgey@gmail.com'
__version__ = '0.1.0'

from ghoul import *

def symbol_includes(symbol, object_type):
    types = [type(value) for value in symbol.values]
    return object_type in types

def symbol_includes_all(symbol, types):
    return all([symbol_includes(symbol, t) for t in types])

def symbol_includes_any(symbol, types):
    return any([symbol_includes(symbol, t) for t in types])