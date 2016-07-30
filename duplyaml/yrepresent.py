#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yrepresent.py file.
# Used for the "represent" phase of YAML processing - creating YAML nodes
# from Python objects.

import numbers
import base64
import math
import decimal
from datetime import datetime, date, time, timedelta, tzinfo
from collections import Counter, OrderedDict

from .yconst import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph
from .yexcept import *

# To be done
# (A) - Decompose YAMLRepresenter into strings / bin/ numbers / datetime [Tick]
# (B) - Test all (leave binary to last)
# (C) - Unsafe extension

# To be done
# Make !!python/!!str/!!namespace - NY
# Support all extra types in search bar - everything except pairs
# Testing. (Leave binary to last)
# How to treat binary and text - to be tested
# Unsafe extension
# Make sure the graph works - to be tested
# Integers - Different cases
# Map equality

# Nice hack for Python 2 and 3, based on:
# http://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility

try:
  basestring
except NameError:
  basestring = str

class YAMLRepresenter:
    """ Makes YAML nodes and graphs out of Python. """
    def __init__(self, **kwargs):
        self.idmap = {}
        self.graphout = None
        self.represent_lity_pref = kwargs.get("represent_lity_full", "")
        self.nulldeflt = kwargs.get("nulldeflt", NULL_CAN)
        self.falsedeflt = kwargs.get("falsedeflt", FALSE_CAN)
        self.truedeflt = kwargs.get("truedeflt", TRUE_CAN)
        self.elldeflt = kwargs.get("elldeflt", ELL_CAN)
        self.notimpdeflt = kwargs.get("notimpdeflt", NOTIMP_CAN)
        self.infdeflt = kwargs.get("infdeflt", INF_CAN)
        self.ninfldeflt = kwargs.get("ninfldeflt", NINF_CAN)
        self.nandeflt = kwargs.get("nandeflt", NAN_CAN)
        self.reptuple = kwargs.get("reptuple", False)
        self.repfrozenset = kwargs.get("repfrozenset", False)
        self.treatstrasbin2 = kwargs.get("treatstrasbin2", False)
        self.treatdateasdatetime = kwargs.get("treatdateasdatetime", False)

    def creategraph(self, graphdata):
        self.idmap = {}
        self.graphout = YAMLGraph(self)
        for item in graphdata:
            self.graphout.add_doc(self.createnode(item), self.idmap)
        return self.graphout

    def genscalarnode(self, value, tag, islity = True):
        return YAMLScalarNode(value, self.rendertag(tag, islity), self.graphout)

    def genemptyseq(self, tag, islity = True):
        return YAMLSeqNode([], self.rendertag(tag, islity), self.graphout)

    def genemptymap(self, tag, islity = True):
        return YAMLMapNode([],[], self.rendertag(tag, islity), self.graphout)

# This code really needs to be examined closely.

    def rendertag(self, tag, islity):
        if islity and self.represent_lity_pref:
            return self.represent_lity_pref + tag[2:]
        else:
            return tag

    def createsimplenode(self, item, theidmap = {}):
        if item is None:
            return self.genscalarnode(self.nulldeflt, TAG_NULL)
        if isinstance(item, bool):
            if item == True:
                return self.genscalarnode(self.truedeflt, TAG_BOOL)
            if item == False:
                return self.genscalarnode(self.falsedeflt, TAG_BOOL)
        if item is Ellipsis:
            return self.genscalarnode(self.elldeflt, TAG_ELLIPSIS, False)
        if item is NotImplemented:
            return self.genscalarnode(self.notimpdeflt, TAG_NOTIMP, False)

    def createstrorbinnode(self, item, theidmap = {}):
        if self.treatstrasbin2 and PY_VER == 2 and isinstance(item, str):
            return self.genscalarnode(base64.b64encode(item), TAG_BINARY)
        if isinstance(item, basestring):
            return self.genscalarnode(item, TAG_STR)
        if isinstance(item, (bytes, bytearray,)):
            return self.genscalarnode(base64.b64encode(item), TAG_BINARY)

    def createnumericalnode(self, item, theidmap = {}):
        if isinstance(item, decimal.Decimal):
            return self.genscalarnode(str(item), TAG_DECIMAL)
        if isinstance(item, numbers.Integral):
            return self.genscalarnode(str(item), TAG_INT)
        if isinstance(item, numbers.Rational):
            return self.genscalarnode(str(item), TAG_FRACTION, False)
        if isinstance(item, numbers.Real):
            if item == INF_PY:
                return self.genscalarnode(self.infdeflt, TAG_FLOAT)
            elif item == NINF_PY:
                return self.genscalarnode(self.ninfldeflt, TAG_FLOAT)
            elif math.isnan(item):
                return self.genscalarnode(self.nandeflt, TAG_FLOAT)
            else:
                return self.genscalarnode(str(item), TAG_FLOAT)
        if isinstance(item, numbers.Complex):
            return self.genscalarnode(str(item), TAG_COMPLEX, False)


    def createtemporalnode(self, item, theidmap = {}):
        if isinstance(item, datetime):
            return self.genscalarnode(item.isoformat(), TAG_TIMESTAMP)
        if isinstance(item, date):
            if self.treatdateasdatetime:
                return self.genscalarnode(item.strftime("%Y-%m-%d")+"T00:00:00",
                    TAG_TIMESTAMP)
            else:
                return self.genscalarnode(item.strftime("%Y-%m-%d"), TAG_DATE)
        if isinstance(item, time):
            return self.genscalarnode(item.isoformat(), TAG_TIME)
        if isinstance(item, timedelta):
            seconds = item.seconds
            minutes, seconds = divmod(seconds, 60)
            hours, minutes = divmod(minutes, 60)
            microseconds = item.microseconds
            return YAMLScalarNode(
                'P%(days)iT%(hours)iH%(mins)iM%(secs)i.%(micro)iS' %
                {"days": item.days, "hours": hours, "mins": minutes,
                "secs": seconds, "micro": microseconds}, TAG_TIMEDELTA)

    def createseqnode(self, item, theidmap = {}):
        if isinstance(item, tuple) and self.reptuple:
            ourseqnode = self.genemptyseq(TAG_TUPLE, False)
        else:
            ourseqnode = self.genemptyseq(TAG_SEQ)
        for i in item:
            ourseqnode.addnode(self.createnode(i))
        self.idmap[id(item)] = ourseqnode
        return ourseqnode

    def createmapnode(self, item, theidmap = {}):
        if isinstance(item, Counter):
            ourmapnode = self.genemptymap(TAG_BAG)
        elif isinstance(item, OrderedDict):
            ourmapnode = self.genemptymap(TAG_OMAP)
        elif isinstance(item, dict):
            ourmapnode = self.genemptymap(TAG_MAP)
        elif isinstance(item, frozenset) and self.repfrozenset:
            ourmapnode = self.genemptymap(TAG_FROZENSET, False)
        else: # A bare set
            ourmapnode = self.genemptymap(TAG_SET)
        if isinstance(item, (set, frozenset)):
            for i in item:
                ourmapnode.addkvpair(self.createnode(i),
                     YAMLScalarNode(NULL_CAN, TAG_NULL))
        else:
            for k, v in item:
                ourmapnode.addkvpair(self.createnode(k),
                    self.createnode(v))
        self.idmap[id(item)] = ourmapnode
        return ourmapnode

    def createnode(self, item, theidmap = {}):
        if id(item) in self.idmap:
            return self.idmap[id(item)]
        if item in [None, Ellipsis, NotImplemented] or isinstance(item, bool):
            return self.createsimplenode(item, theidmap)

        if isinstance(item, (bytes, bytearray, basestring)):
            return self.createstrorbinnode(item, theidmap)

        if isinstance(item, (decimal.Decimal, numbers.Number,)):
            return self.createnumericalnode(item, theidmap)

        if isinstance(item, (datetime, date, time, timedelta)):
            return self.createtemporalnode(item, theidmap)

        if isinstance(item, (list, tuple,)):
            return self.createseqnode(item, theidmap)

        if isinstance(item, (Counter, OrderedDict, dict, set, frozenset)):
            return self.createmapnode(item, theidmap)

# Add unresolvable error

        raise YAMLRepresentException("cannot resolve %(item)s as YAML"
                % {"item": item})




class YAMLClassRepresenter(YAMLRepresenter):
    pass
