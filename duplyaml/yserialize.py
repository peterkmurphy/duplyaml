#!/usr/bin/env python
# The duplyaml YAML processor.
# The yserialise.py file.
# Used for serializing YAML graphs

from .yconst import *
from .yevent import YAMLEvent


def genintstr():
    """ This method generates integers as strings starting from 0 increasing.
    It is the default anchor generator for YAMLSerializer

    :return: the next integer (as a string).
    """
    anchorout = 0
    while True:
        yield str(anchorout)
        anchorout += 1


class YAMLSerializer:
    """ The YAMLSerializer class is present to serialize a YAMLGraph as YAML
    events. It takes an instance of a YAMLEvent (or a descendant), and
    call methods inside it (such as start_doc and end_seq) as necessary to
    serialize the YAMLGraph to some destination. One common case is when it
    the serialise events are used to dump YAML to a file.
    """

    def __init__(self, yamlgraph, yamleventer=YAMLEvent(None),
                 makeanchor=genintstr):
        """ Initialises the class.
        :param yamlgraph: The YAMLGraph (and its nodes) for serialisation.
        :param yamleventer: A YAMLEvent with serialization methods inside.
        :param makeanchor: generator method for creating unique anchors.
        """
        self.anchormap = {}
        self.yamlgraph = yamlgraph
        self.yamleventer = yamleventer
        self.makeanchor = makeanchor

    def serializestream(self):
        """ Call this method to start serializing the source graph. """
        self.yamleventer.start_stream()
        for doc in self.yamlgraph.children:
            self.serializedoc(doc)
        self.yamleventer.end_stream()

    def serializedoc(self, doc):
        """ Called for each document node in the source YAMLGraph
        :param doc: A document node - one of the children of the YAMLGraph.
        """
        self.anchormap = {}
        self.yamleventer.start_document({})
        self.serializenode(doc)
        self.yamleventer.end_document()

    def serializenode(self, node):
        """ Called for each individual node in the source YAMLGraph
        :param node: A YAMLNode of interest.
        """

        if (id(node)) in self.anchormap:
            self.yamleventer.alias(self.anchormap[id(node)])
        else:
            ouranchor = self.makeanchor()
            self.anchormap[id(node)] = ouranchor
            if node.kind == YAMLNODE_SCA:
                self.yamleventer.scalar(ouranchor, node.tag, node.scalarval)
            if node.kind == YAMLNODE_SEQ:
                self.yamleventer.start_seq(ouranchor, node.tag)
                for subnode in node.nodeseq:
                    self.serializenode(subnode)
                self.yamleventer.end_seq()
            if node.kind == YAMLNODE_MAP:
                self.yamleventer.start_map(ouranchor, node.tag)
                maplen = len(node.keyseq)
                for i in range(maplen):
                    self.serializenode(node.keyseq[i])
                    self.serializenode(node.valseq[i])
                self.yamleventer.end_map()
