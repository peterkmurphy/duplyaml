#!/usr/bin/env python
# The duplyaml YAML processor.
# The yrepresent.py file.
# Used for the "represent" phase of YAML processing - creating YAML nodes
# from Python objects.

import numbers
import base64

from .yconst import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

# Nice hack for Python 2 and 3, based on:

# http://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility

# Comments on this file:
# It is possible to overthing this problem.




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
            return YAMLScalarNode(CAN_NULL, TAG_NULL)
        if isinstance(item, bool):
            if item == True:
                return YAMLScalarNode(CAN_TRUE, TAG_BOOL)
            if item == False:
                return YAMLScalarNode(CAN_FALSE, TAG_BOOL)
        if isinstance(item, basestring):
            return YAMLScalarNode(item, TAG_STR)
        if isinstance(item, numbers.Integral):
            return YAMLScalarNode(str(item), TAG_INT)
#        if isinstance(item, numbers.Rational):
#            return YAMLScalarNode(str(item), TAG_FRACTION)
#        if isinstance(item, numbers.Complex):
#            return YAMLScalarNode(str(item), TAG_COMPLEX)

        if isinstance(item, numbers.Number):
            return YAMLScalarNode(str(item), TAG_FLOAT)
        if isinstance(item, (bytes, bytearray,)):
            return YAMLScalarNode(base64.b64encode(item), TAG_BINARY)
        if item.id in self.idmap:
            return self.idmap[item.id]


