#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yrepresent.py file.
# Used for the "represent" phase of YAML processing - creating YAML nodes
# from Python objects.

import numbers
import base64
import math
from datetime import datetime, date, time, timedelta
from collections import Counter, OrderedDict

from .yconst import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph
from .yexcept import *

# Nice hack for Python 2 and 3, based on:

# http://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility

# Comments on this file:
# It is possible to overthing this problem.

#        if isinstance(item, numbers.Rational):
#            return YAMLScalarNode(str(item), TAG_FRACTION)
#        if isinstance(item, numbers.Complex):
#            return YAMLScalarNode(str(item), TAG_COMPLEX)

# Types to check
# None
# Boolean
# Int
# Float
# Binary
# Timestamp
# Timedelta
# String
# List
# Set
# Map

#(#Omap)
#(#pairs)
# Tuple

# Make !!python/!!str/!!namespace
# Support all extra types in search bar
# Testing. (Leave binary to last)
# How to treat binary and text
# Unsafe extension


try:
  basestring
except NameError:
  basestring = str

class YAMLRepresenter:
    """ Makes YAML nodes and graphs out of Python. """
    def __init__(self, **kwargs):
        self.idmap = {}
        self.nulldeflt = kwargs.get("nulldeflt", NULL_CAN)
        self.falsedeflt = kwargs.get("falsedeflt", FALSE_CAN)
        self.truedeflt = kwargs.get("truedeflt", TRUE_CAN)
        self.elldeflt = kwargs.get("elldeflt", ELL_CAN)
        self.notimpdeflt = kwargs.get("notimpdeflt", NOTIMP_CAN)
        self.infdeflt = kwargs.get("infdeflt", INF_CAN)
        self.ninfldeflt = kwargs.get("ninfldeflt", NINF_CAN)
        self.nandeflt = kwargs.get("nandeflt", NAN_CAN)
        self.reptuple = kwargs.get("reptuple", True)
        self.repfrozenset = kwargs.get("repfrozenset", True)

    def creategraph(self, graphdata):
        self.idmap = {}
        graphout = YAMLGraph(self)
        for item in graphdata:
            graphout.add_doc(self.createnode(item), self.idmap)
        return graphout

    def createnode(self, item, theidmap = {}):
        if item is None:
            return YAMLScalarNode(self.nulldeflt, TAG_NULL)
        if isinstance(item, bool):
            if item == True:
                return YAMLScalarNode(self.truedeflt, TAG_BOOL)
            if item == False:
                return YAMLScalarNode(self.falsedeflt, TAG_BOOL)
        if item is Ellipsis:
            return YAMLScalarNode(self.elldeflt, TAG_ELLIPSIS)
        if item is NotImplemented:
            return YAMLScalarNode(self.notimpdeflt, TAG_NOTIMP)

        if isinstance(item, basestring):
            return YAMLScalarNode(item, TAG_STR)
        if isinstance(item, numbers.Integral):
            return YAMLScalarNode(str(item), TAG_INT)
        if isinstance(item, numbers.Number):
            if item == INF_PY:
                return YAMLScalarNode(self.infdeflt, TAG_FLOAT)
            elif item == NINF_PY:
                return YAMLScalarNode(self.ninfldeflt, TAG_FLOAT)
            elif math.isnan(item):
                return YAMLScalarNode(self.nandeflt, TAG_FLOAT)
            else:
                return YAMLScalarNode(str(item), TAG_FLOAT)
        if isinstance(item, (bytes, bytearray,)):
            return YAMLScalarNode(base64.b64encode(item), TAG_BINARY)
        if isinstance(item, datetime):
            pass
        if isinstance(item, date):
            pass
        if isinstance(item, time):
            pass
        if isinstance(item, timedelta):
            pass

        if item.id in self.idmap:
            return self.idmap[item.id]
        if isinstance(item, Counter):
            ourmapnode = YAMLMapNode([],[],TAG_BAG)
            for k,v in item:
                ourmapnode.addkvpair(self.createnode(k),
                    self.createnode(v))
            self.idmap[item.id] = ourmapnode
        if isinstance(item, OrderedDict):
            ourmapnode = YAMLMapNode([],[],TAG_OMAP)
            for k,v in item:
                ourmapnode.addkvpair(self.createnode(k),
                    self.createnode(v))
            self.idmap[item.id] = ourmapnode
        if isinstance(item, (list, tuple,)):
            if isinstance(item, tuple) and self.reptuple:
                ourseqnode = YAMLSeqNode([], TAG_TUPLE)
            else:
                ourseqnode = YAMLSeqNode([], TAG_SEQ)
            for i in item:
                ourseqnode.addnode(self.createnode(i))
            self.idmap[item.id] = ourseqnode
            return ourseqnode
        if isinstance(item, dict):
            ourmapnode = YAMLMapNode([],[],TAG_MAP)
            for k,v in item:
                ourmapnode.addkvpair(self.createnode(k),
                    self.createnode(v))
            self.idmap[item.id] = ourmapnode
            return ourmapnode
        if isinstance(item, (set, frozenset)):
            if isinstance(item, frozenset) and self.repfrozenset:
                oursetnode = YAMLMapNode([],[],TAG_FROZENSET)
            else:
                oursetnode = YAMLMapNode([],[],TAG_SET)
            for i in item:
                oursetnode.addkvpair(self.createnode(i),
                    YAMLScalarNode(NULL_CAN, TAG_NULL))
            self.idmap[item.id] = oursetnode
            return oursetnode

# Add unresolvable error

        raise YAMLRepresentException("cannot resolve %(item)s as YAML"
                % {"item": item})

class YAMLClassRepresenter(YAMLRepresenter):
    pass
