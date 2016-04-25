#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yconstruct.py file.
# Used for the "construct" phase of YAML processing - turning YAML nodes
# into Python objects.

import numbers
import base64
import re

from .yconst import *
from .yexcept import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

try:
  basestring
except NameError:
  basestring = str

# Work out schema
# Exclamation
# Question Mark
# Tags

class YAMLConstructor:
    """ This class makes native data out of a YAML graph. """

    int_bin_regexp = re.compile("^[-+]?0b[0-1_]+$")
    int_oct_regexp = re.compile("^[-+]?0o[0-7_]+$")
    int_dec_regexp = re.compile("^[-+]?(0|[1-9][0-9_]*)$")
    int_hex_regexp = re.compile("^[-+]?0x[0-9a-fA-F_]+$")
    int_sex_regexp = re.compile("^[-+]?[1-9][0-9_]*(:[0-5]?[0-9])+$")

    def __init__(self, bext = False):
        self.idmap = {}
        self.bext = bext

    @classmethod
    def isnullstring(cls, strin):
        return (strin in TAG_NULL_VALUES)

    @classmethod
    def isfalsestring(cls, strin, bext = False):
        if bext:
            return (strin in TAG_FALSE_EXT_VALUES)
        else:
            return (strin in TAG_FALSE_VALUES)

    @classmethod
    def istruestring(cls, strin, bext = False):
        if bext:
            return (strin in TAG_TRUE_EXT_VALUES)
        else:
            return (strin in TAG_TRUE_VALUES)

# Haven't done the base 60 thing

    @classmethod
    def getintfromstring(cls, strin):
        strinwoutund = strin.replace("_", "")
        try:
            if cls.int_dec_regexp.match(strin):
                return int(strinwoutund)
            elif cls.int_oct_regexp.match(strin):
                return int(strinwoutund.replace("o", ""), 8)

            elif cls.int_hex_regexp.match(strin):
                return int(strinwoutund.replace("x", ""), 16)

            elif cls.int_bin_regexp.match(strin):
               return int(strinwoutund.replace("b", ""), 2)
            else:
                return None

        except:
            return None

    @classmethod
    def getfloatstring(cls, strin):
        pass;


    @classmethod
    def raisecoerceexc(cls, node):
        raise YAMLConstructException(
            "attempting to coerce '%(can)s' into an %(tag)s" %
            {"can": node.scalarval, "tag": node.tag})

    # Come back later to work out details of exception.

    def createdata(self, yamlgraph):
        self.idmap = {}
        dataout = []
        for item in yamlgraph.children:
            self.construct(item, self.idmap)
        return dataout

    def construct(self, item, theidmap = {}):
        gettag = item.tag

# For YAML. there is no effective difference between !!tag and
# "tag:yaml.org,2002:tag, so we convert to the former format.

        if gettag.find(YAML_NAME_PREFIX) == 0:
            gettag = C_SECONDARY_TAG_HANDLE+ gettag[len(YAML_NAME_PREFIX):]
            print (gettag)
        try:

 # We now do scalar elements in the YAML name space.


            if gettag == TAG_NULL:
                if YAMLConstructor.isnullstring(item.scalarval):
                    return None
                else:
                    YAMLConstructor.raisecoerceexc(item)

            if gettag == TAG_BOOL:
                if YAMLConstructor.istruestring(item.scalarval, self.bext):
                    return True
                elif YAMLConstructor.isfalsestring(item.scalarval, self.bext):
                    return False
                else:
                    YAMLConstructor.raisecoerceexc(item)

            if gettag == TAG_INT:
                return YAMLConstructor.getintfromstring(item.scalarval)
            if gettag == TAG_FLOAT:
                return float(item.scalarval)
            if gettag == TAG_BINARY:
                return base64.b64decode(item.scalarval)
            if gettag == TAG_STR:
                    return item.scalarval


#        if isinstance(item, numbers.Rational):
#            return YAMLScalarNode(str(item), TAG_FRACTION)
#        if isinstance(item, numbers.Complex):
#            return YAMLScalarNode(str(item), TAG_COMPLEX)
        except ValueError, e:
            raise YAMLConstructException(
                "attempting to coerce '%(can)s' into an %(tag)s" %
                { "can":item.scalarval, "tag":item.tag})

        if item.id in self.idmap:
            return self.idmap[item.id]
