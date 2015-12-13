#!/usr/bin/env python
# The duplyaml YAML processor.
# The ycompose.py file.
# Used for creating YAMLGraphs from event streams

from .yconst import *
from .yevent import YAMLEvent
from .yexcept import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph

# These variables are useful for setting a stack of things to do.

COMPOSESTACK_STREAM = 0
COMPOSESTACK_DOC = 1
COMPOSESTACK_SEQ = 2
COMPOSESTACK_MAP = 3
COMPOSESTACK_MAPKEY = 3

class YAMLComposer(YAMLEvent):
    """ Makes YAML graphs out of events. """
    def __init__(self):
        self.anchormap = {}
        self.yamlgraph = None
        self.streamstarted = False
        self.streamended = False
        self.stackstate = []
        self.nodestack = []

    def start_stream(self, src):
        self.yamlgraph = YAMLGraph(src)
        self.streamstarted = True
        self.streamended = False
        self.stackstate = []
        self.stackstate.push(COMPOSESTACK_STREAM)
        self.nodestack = []

    def end_stream(self):
        self.streamstarted = False
        self.streamended = True

    def start_document(self, directives):
        self.anchormap = {}
        pass

    def end_document(self):
        pass

    def start_seq(self, anchor, tag):
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourseqnode = YAMLSeqNode([], tag, self.yamlgraph)
        self.anchormap[anchor] = ourseqnode

    def end_seq(self):
        pass

    def start_map(self, anchor, tag):
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourmapnode = YAMLMapNode([], [], tag, self.yamlgraph)
        self.anchormap[anchor] = ourmapnode

    def end_map(self):
        pass

    def scalar(self, anchor, tag, canvalue):
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourscalarnode = YAMLScalarNode(canvalue, tag, self.yamlgraph)
        self.anchormap[anchor] = ourscalarnode
        return ourscalarnode # ?? Returning - or add to containing thang!



    def alias(self, aliasval):
        if aliasval not in self.anchormap:
            raise YAMLAliasLacksAnchorException(
                "Alias '%s' declared without corresponding anchor" % aliasval)
        return self.anchormap[aliasval] # ?? Returning - or add to containing thang!



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