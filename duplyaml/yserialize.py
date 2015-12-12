#!/usr/bin/env python
# The duplyaml YAML processor.
# The yserialise.py file.
# Used for serializing YAMLGraph

from .yconst import *
from .yevent import YAMLEvent
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

def genanchors():
    anchorout = 0
    while True:
        yield str(anchorout)
        anchorout += 1

class YAMLSerializer:
    """ Makes native data out of YAML graph. """
    def __init__(self, yamlgraph, yamleventer = YAMLEvent(), makeanchor = genanchors):
        self.anchormap = {}
        self.yamlgraph = yamlgraph
        self.yamleventer = yamleventer
        self.makeanchor = makeanchor

    def serializestream(self):
        self.yamleventer.start_stream()
        for item in self.yamlgraph.children:
            self.serializedoc(item)
        self.yamleventer.end_stream()

    def serializedoc(self, item):
        self.anchormap = {}
        self.yamleventer.start_document({})
        self.serializenode(item);
        self.yamleventer.end_document()

    def serializenode(self,item):
        if (id(item)) in self.anchormap:
            self.yamleventer.alias(self.anchormap[id(item)])
        else:
            ouranchor = self.makeanchor()
            self.anchormap[id(item)] = ouranchor
            if item.kind == YAMLNODE_SCA:
                self.yamleventer.scalar(ouranchor, item.tag, item.canvalue)
            if item.kind == YAMLNODE_SEQ:
                self.yamleventer.start_seq(ouranchor, item.tag)
                for subnode in item.nodeseq:
                    self.serializenode(subnode)
                self.yamleventer.end_seq()
            if item.kind == YAMLNODE_MAP:
                self.yamleventer.start_map(ouranchor, item.tag)
                maplen = len(item.keyseq)
                for i in range(maplen):
                    self.serializenode(item.keyseq[i])
                    self.serializenode(item.valseq[i])
                self.yamleventer.end_map()