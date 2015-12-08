#!/usr/bin/env python
# The duplyaml YAML processor.
# The duplyaml/ygraph.py file.
# Represents the YAML Representation Graph.


# These are the constants used to define the Node kinds used with YAML nodes

YAMLNODE_DEF = 0 # Used with the YAMLNode class by default.
YAMLNODE_SCA = 1 # Used with scalar nodes.
YAMLNODE_SEQ = 2 # Used with sequence nodes.
YAMLNODE_MAP = 3 # Used with mapping nodes.


# The yappystgraph represents a YAML stream: "a sequence of disjoint directed graphs, each with a root node."
# We treat this object differently from normal nodes.

class YAMLGraph:
    """Represents a YAML representation graph."""

    def __init__(self, src):
        """ Initializes a YAML representation graph
        :param src: The source of the data. This is implementation dependent.
        """
        self.src = src
        self.children = []

    def add_doc(self, node):
        """ Adds a node as a new document to the representation graph.
        :param node: The node to add.
        """
        self.children.extend(node)
        node.graph = self

    def __len__(self):
        return len(self.children)


class YAMLNode:
    """ Represents a node in a YAML document. """

    def __init__(self, tag, anchor=None, graph=None, kind=YAMLNODE_DEF):
        """ Initialises a new YAML node
        :param tag: Indicates the types of data - string, integer, etc.
        :param anchor: Indicates the anchor used for the node, if any.
        :param graph: Indicates the YAML representation graph containing it, if any.
        :param kind: The kind - scalar, sequence or mapping.
        """
        self.tag = tag
        self.anchor = anchor
        self.graph = graph
        self.kind = kind

    def __eq__(self, other):
        return self.tag == other.tag and self.kind == other.kind

    def checkeq(self, other, dchecks={}):
        return YAMLNode.__eq__(self, other)

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class YAMLScalarNode(YAMLNode):
    """ Represents YAML nodes for scalar data: strings, integers, floats, etc. """
    def __init__(self, canvalue, tag, anchor=None, graph=None, kind=YAMLNODE_SCA):
        """ Initialise a new YAML scalar node
        :param canvalue: This is the canonical value (and should be a string).
        """
        YAMLNode.__init__(self, tag, anchor, graph, kind)
        self.canvalue = canvalue

    def __eq__(self, other):
        return YAMLNode.__eq__(self, other) and self.canvalue == other.canvalue


class YAMLSeqNode(YAMLNode):
    """ Represents YAML nodes for sequences: """
    def __init__(self, nodeseq, tag, anchor=None, graph=None, kind=YAMLNODE_SEQ):
        """ Initialise a new YAML sequence node
        :param nodeseq: A sequence of nodes).
        """
        YAMLNode.__init__(self, tag, anchor, graph, kind)
        self.nodeseq = nodeseq

    def addnode(self, node):
        """ Add a new node to the sequence.
        :param node: The node to be added.
        """
        self.nodeseq.append(node)
        node.graph = self.graph

    def checkeq(self, other, dchecks={}):
        idtuple = (id(self), id(other),)
        if idtuple in dchecks:
            return True
        dchecks[idtuple] = False
        if not YAMLNode.__eq__(self, other):
            dchecks[idtuple] = True
            return False
        selflen = len(self.nodeseq)
        if selflen != len(other.nodeseq):
            dchecks[idtuple] = True
            return False
        for i in range(selflen):
            if not (self.nodeseq[i].checkeq(other.nodeseq[i], dchecks)):
                dchecks[idtuple] = True
                return False
        dchecks[idtuple] = True
        return True

    def __eq__(self, other):
        return self.checkeq(other, {})

    def __repr__(self):
        return "%s(%r)" % (self.__class__, dict(self.__dict__).pop("nodeseq"))


class YAMLMapNode(YAMLNode):
    """ Represents YAML nodes for mappings: """
    def __init__(self, keyseq, valseq, tag, anchor=None, graph=None, kind=YAMLNODE_MAP):
        """ Initialise a new YAML mapping node
        :param keyseq: A sequence of nodes representing keys.
        :param valseq: A sequence of nodes representing matching values.
        """
        YAMLNode.__init__(self, tag, anchor, graph, kind)
        self.keyseq = keyseq
        self.valseq = valseq

    def addkvpair(self, nodekey, nodeval):
        """ Add a new node to the sequence.
        :param nodekey: The key to be added.
        :param nodeval: The value to be added.
        """
        self.keyseq.append(nodekey)
        nodekey.graph = self.graph
        self.valseq.append(nodeval)
        nodeval.graph = self.graph


    def checkeq(self, other, dchecks={}):
        idtuple = (id(self), id(other),)
        if (idtuple) in dchecks:
            return True
        dchecks[idtuple] = False
        if not YAMLNode.__eq__(self, other):
            dchecks[idtuple] = True
            return False
        selflen = len(self.keyseq)
        if selflen != len(other.keyseq):
            dchecks[idtuple] = True
            return False
        for i in range(selflen):
            if not (self.keyseq[i].checkeq(other.keyseq[i], dchecks)):
                dchecks[idtuple] = True
                return False
        for i in range(selflen):
            if not (self.valseq[i].checkeq(other.valseq[i], dchecks)):
                dchecks[idtuple] = True
                return False
        dchecks[idtuple] = True
        return True

    def __eq__(self, other):
        return self.checkeq(other, {})


    def __repr__(self):
        return "%s(%r)" % (self.__class__,
            {key: self.__dict__[key] for key in self.__dict__ if key not in ["keyseq", "valueseq"]})





