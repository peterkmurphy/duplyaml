#!/usr/bin/env python
# The duplyaml YAML processor.
# The yserialise.py file.
# Used for serializing YAMLGraph

from .yevent import YAMLEvent
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

def genanchors():
    anchorout = 0
    while True:
        yield str(anchorout)
        anchorout += 1

class YAMLSerializer:
    """ Makes native data out of YAML graph. """
    def __init__(self, yamlgraph, yamleventer = YAMLEvent(), makeanchor = genanchors()):
        self.anchormap = {}
        self.yamlgraph = yamlgraph
        self.yamleventer = yamleventer
        self.makeanchor = makeanchor

    def serializestream(self):
        self.yamleventer.start_stream()
        for item in self.yamlgraph.children:
            self.serializedoc(self, item)
        self.yamleventer.end_stream()

    def serializedoc(self, item):
        self.anchormap = {}
        self.yamleventer.start_document({})

        self.yamleventer.end_document()