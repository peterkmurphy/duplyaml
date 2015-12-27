#!/usr/bin/env python
# The duplyaml YAML processor.
# The yconstruct.py file.
# Used for the "construct" phase of YAML processing - turning YAML nodes
# into Python objects.

import numbers
import base64

from .yconst import *
from .yexcept import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

try:
  basestring
except NameError:
  basestring = str

class YAMLConstructor:
    """ Makes native data out of YAML graph. """
    def __init__(self):
        self.idmap = {}

    def createdata(self, yamlgraph):
        self.idmap = {}
        dataout = []
        for item in yamlgraph.children:
            self.construct(item, self.idmap)
        return dataout

    def construct(self, item, theidmap = {}):
        gettag = item.tag
        try:
            if gettag == TAG_NULL:
                return None
            if gettag == TAG_BOOL:
                if item.scalarval in ["true"]:
                    return True
                else:
                    return False
            if gettag == TAG_STR:
                return item.scalarval
            if gettag == TAG_INT:
                return int(item.scalarval)
            if gettag == TAG_FLOAT:
                return float(item.scalarval)
            if gettag == TAG_BINARY:
                return base64.b64decode(item.scalarval)
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
