#!/usr/bin/env python
# The duplyaml YAML processor.
# The yrepresent.py file.
# Used for the "represent" phase of YAML processing - creating YAML nodes
# from Python objects.

import numbers
import base64

from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

# Tag constants

TAG_MAP = "!!map" # Unordered set of key: value pairs without duplicates.
TAG_OMAP = "!!omap" # Ordered sequence of key: value pairs without duplicates.
TAG_PAIRS = "!!pairs" # Ordered sequence of key: value pairs allowing duplicates.
TAG_SET = "!!set" # Unordered set of non-equal values.
TAG_SEQ = "!!seq" # Sequence of arbitrary values.
TAG_BINARY = "!!binary" # A sequence of zero or more octets (8 bit values).
TAG_BOOL = "!!bool" # Mathematical Booleans.
TAG_FLOAT = "!!float" # Floating-point approximation to real numbers.
TAG_INT = "!!int" # Mathematical integers.
TAG_MERGE = "!!merge" # Specify one or more mappings to be merged with the current one.
TAG_NULL = "!!null" # Devoid of value.
TAG_STR = "!!str" # A sequence of zero or more Unicode characters.
TAG_TIMESTAMP = "!!timestamp" # A point in time.
TAG_VALUE = "!!value" # Specify the default value of a mapping.
TAG_YAML = "!!yaml" # Keys for encoding YAML in YAML.

# Extra ones that seems to be of use:

TAG_COMPLEX = "!!complex" # Represents complex numbers of form a+bj
TAG_FRACTION = "!!fraction" # Represents complex numbers of form a+bj
TAG_TIMEDELTA = "!!timedelta" # Represents time intervals

# Nice hack for Python 2 and 3, based on:

# http://stackoverflow.com/questions/11301138/how-to-check-if-variable-is-string-with-python-2-and-3-compatibility

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
            graphout.add_doc(self.createnode(item))
        return graphout

    def createnode(self, item):
        if item.id in self.idmap:
            return self.idmap[item.id]
        if item is None:
            return YAMLScalarNode("~", TAG_NULL)
        if item == True:
            return YAMLScalarNode("y", TAG_BOOL)
        if item == False:
            return YAMLScalarNode("n", TAG_BOOL)
        if isinstance(item, basestring):
            return YAMLScalarNode(item, TAG_STR)
        if isinstance(item, numbers.Integral):
            return YAMLScalarNode(str(item), TAG_INT)
        if isinstance(item, numbers.Rational):
            return YAMLScalarNode(str(item), TAG_FRACTION)
        if isinstance(item, numbers.Complex):
            return YAMLScalarNode(str(item), TAG_COMPLEX)
        if isinstance(item, numbers.Number):
            return YAMLScalarNode(str(item), TAG_FLOAT)
        if isinstance(item, (bytes, bytearray,)):
            return YAMLScalarNode(base64.b64encode(item), TAG_BINARY)



