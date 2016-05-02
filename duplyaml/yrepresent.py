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




try:
  basestring
except NameError:
  basestring = str

class YAMLRepresenter:
    """ Makes YAML nodes and graphs out of Python. """
    def __init__(self):
        self.idmap = {}

    def creategraph(self, graphdata):
        self.idmap = {}
        graphout = YAMLGraph(self)
        for item in graphdata:
            graphout.add_doc(self.createnode(item), self.idmap)
        return graphout

    def createnode(self, item, theidmap = {}):
        if item is None:
            return YAMLScalarNode(NULL_CAN, TAG_NULL)
        if isinstance(item, bool):
            if item == True:
                return YAMLScalarNode(TRUE_CAN, TAG_BOOL)
            if item == False:
                return YAMLScalarNode(FALSE_CAN, TAG_BOOL)
        if item is Ellipsis:
            return YAMLScalarNode(ELL_CAN, TAG_ELLIPSIS)
        if item is NotImplemented:
            return YAMLScalarNode(NOTIMP_CAN, TAG_NOTIMP)

        if isinstance(item, basestring):
            return YAMLScalarNode(item, TAG_STR)
        if isinstance(item, numbers.Integral):
            return YAMLScalarNode(str(item), TAG_INT)
        if isinstance(item, numbers.Number):
            if item == INF_PY:
                return YAMLScalarNode(INF_CAN, TAG_FLOAT)
            elif item == NINF_PY:
                return YAMLScalarNode(NINF_CAN, TAG_FLOAT)
            elif math.isnan(item):
                return YAMLScalarNode(NAN_CAN, TAG_FLOAT)
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
        if isinstance(item, (list, tuple,)):
            if isinstance(item, list):
                ourseqnode = YAMLSeqNode([], TAG_SEQ)
            else:
                ourseqnode = YAMLSeqNode([], TAG_TUPLE)
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
        if isinstance(item, set):
            oursetnode = YAMLMapNode([],[],TAG_SET)
            for i in item:
                oursetnode.addkvpair(self.createnode(i),
                    YAMLScalarNode(NULL_CAN, TAG_NULL))
            self.idmap[item.id] = oursetnode
            return oursetnode

# Add unresolvable error

        raise YAMLRepresentException("cannot resolve %(item)s as YAML"
                % {"item": item})