# -*- coding: utf-8 -*-
import inspect
import random
from collections import defaultdict

PRIMITIVE_TYPES = [str, int, float]

class Symbol(object):
    def __init__(self, values):
        self.parent = None
        self.children = {}
        self.InitVals(values)
        self.CalcAttributes()
        
    def InitVals(self, values):
        if inspect.isclass(values):
            self.values = []
            def _append_subclass_instances(t):
                subclasses = t.__subclasses__()
                for subclass in subclasses:
                    _append_subclass_instances(subclass)
                if len(subclasses) == 0:
                    self.values.append(t())
            _append_subclass_instances(values)
        else:
            if type(values) is Symbol:
                self.values = values.values
            elif type(values) is list:
                self.values = values
            else:
                self.values = [values]
        if len(self.values) == 1:
            self._value = self.values[0]
        else:
            self._value = None
        
    def __repr__(self):
        return str(self.val)
    
    def __getattr__(self, attr):
        if attr == 'val':
            if self._value:
                return self._value
            else:
                if len(self.values) == 1:
                    return self.values[0]
                else:
                    return self.values
        raise AttributeError("{} object has no attribute {}".format(self.__class__, attr))
    
    def CalcAttributes(self):
        # TODO: drop deprecated attributes
        for key in self.children:
            delattr(self, key)
        self.children = {}
        attribute_values = defaultdict(list)
        for value in self.values:
            if type(value) in PRIMITIVE_TYPES:
                continue
            for key, val in AttributesDict(value).items():
                if isinstance(val, Symbol):
                    attribute_values[key].extend(val.values)
                elif type(val) is list:
                    attribute_values[key].extend(val)
                else:
                    attribute_values[key].append(val)
        for key, vals in attribute_values.items():
            # implies recursion!
            symbol = Symbol(vals)
            symbol.parent = self
            symbol.attribute_name = key
            self.children[key] = symbol
            setattr(self, key, symbol)
    
    def Observe(self):
        if self._value:
            return self._value
        else:
            return self.Collapse(None)
    
    def Collapse(self, symbol, upward=True):
        if symbol is None:
            return self.Collapse(Symbol([random.choice(self.values)]))
        # TODO: reject if intersection is 0? some basic rejection 
        
        if type(symbol) not in [Symbol, type]:
            symbol = Symbol(symbol)

        # adopt new values
        self.InitVals(Subset(self, symbol))

        # recalculate my attributes
        self.CalcAttributes()
        
        # ensure that my calculated attributes correspond to symbol's
        if type(symbol) is not type:
            for key in self.children and symbol.children:
                self.children[key].Collapse(symbol.children[key], upward=False)

        # restrict my values to only those whose attributes are also consistent with symbol
        if self.parent is not None and upward is True:
            # self.parent.Collapse(self.parent)
            self.parent.Restrict(self, self.attribute_name)

        return self
    
    def Restrict(self, child, attribute_name, upward=True):
        def _attributes_match(value):
            value_attributes = AttributesDict(value)
            if attribute_name in value_attributes:
                # v.p -> v.p ∩ child
                value_attribute = value_attributes[attribute_name]
                intersection = Subset(value_attribute, child)
                if intersection is None:
                    return False
                else:
                    setattr(value, attribute_name, intersection)
                    return True
            else:
                # child has not p
                return False

        new_vals = []
        for value in self.values:
            if _attributes_match(value):
                new_vals.append(value)
        if len(new_vals) == 0:
            raise Exception('empty restriction!')
        self.InitVals(new_vals)

        if self.parent is not None and upward is True:
            self.parent.Restrict(self, self.attribute_name)

def AttributesDict(obj):
    filters = [
        lambda key, value: key[0] != '_',
        lambda key, value: not callable(value),
        lambda key, value: key != 'parent' and key != 'values' and key != 'val'
    ]
    attributes = {i: obj.__getattribute__(i) for i in dir(obj) if i[0] != '_'}
    for fn in filters:
        attributes = {k: v for k, v in attributes.items() if fn(k, v)}
    return attributes

def Subset(value, target, depth=0):
    '''Return the subset of value that spans target. If no
    such subset exists, return None
    '''

    #######################
    ## VALUE IS ITERABLE ##
    #######################

    if type(value) is Symbol:
        subset = Subset(value.values, target, depth=depth+1)
        if subset is not None:
            return Symbol(subset)
        else:
            return None

    # TODO: explain why this works
    if type(value) is list:
        results = [Subset(element, target, depth=depth+1) for element in value]
        results = [result for result in results if result is not None]
        if len(results) == 0:
            return None
        if len(results) == 1:
            return results[0]
        return results
    
    ########################
    ## TARGET IS ITERABLE ##
    ########################

    if type(target) is Symbol:
        return Subset(value, target.values, depth=depth+1)

    # TODO: explain why this works
    if type(target) is list:
        for element in target:
            result = Subset(value, element, depth=depth+1)
            if result is not None:
                return result
        return None
    
    ###################
    # CONCRETE VALUES #
    ###################
    
    if value == target:
        return value
    if type(target) is type:
        if type(value) == target:
            return value
        if type(value) in target.__subclasses__():
            return value

    if type(value) not in PRIMITIVE_TYPES:
        if type(value) == type(target):
            return value
        if type(target) in type(value).__subclasses__():
            # TODO: (subclass)Value promotion
            # just take all attributes and methods
            return value

    # print('\t'*depth, is_subset)
    return None

def symbol_includes(symbol, object_type):
    types = [type(value) for value in symbol.values]
    return object_type in types

def symbol_includes_all(symbol, types):
    return all([symbol_includes(symbol, t) for t in types])

def symbol_includes_any(symbol, types):
    return any([symbol_includes(symbol, t) for t in types])

# class Symbolic(object):
#     def __init__(self):
#         self.symbols = WeakKeyDictionary()
 
#     def __get__(self, instance_obj, objtype):
#         if instance_obj is None:
#             return self
#         # if instance_obj in self.symbols:
#         return self.symbols[instance_obj]
#         # else:
#         #     # import ipdb; ipdb.set_trace()
#         #     return None
 
#     def __set__(self, instance, values):
#         self.symbols[instance] = Symbol(values)
 
#     def __delete__(self, instance):
#         del self.symbols[instance]
