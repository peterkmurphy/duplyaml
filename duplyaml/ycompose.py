#!/usr/bin/env python
# The duplyaml YAML processor.
# The ycompose.py file.
# Used for creating YAMLGraphs from event streams

from .yconst import *
from .yevent import YAMLEvent
from .yexcept import *
from .ygraph import YAMLNode, YAMLScalarNode, YAMLSeqNode, YAMLMapNode, YAMLGraph


class YAMLComposer(YAMLEvent):
    """ Makes YAML graphs out of events. """
    def __init__(self, src):
        self.anchormap = {}
        self.yamlgraph = None
        self.nodestack = []
        YAMLEvent.__init__(self, src)

    def clearstack(self):
        while self.nodestack:
            nodepop = self.nodestack.pop()
            if (nodepop.kind == YAMLNODE_MAP and nodepop.status == YAMLMAP_STATUS_VALREADY):
                nodepop.addnode(YAMLScalarNode("null", "!null"))

    def checkstreamstarted(self):
        if self.yamlgraph is None:
            raise YAMLComposeException("Stream yet to start")

    def start_stream(self, pos=None):
        if not self.yamlgraph:
            self.yamlgraph = YAMLGraph(self.src, pos)
            self.nodestack = []
        else:
            raise YAMLComposeException("Stream %s already started" % self.src)

    def end_stream(self, pos=None):
        self.checkstreamstarted()
        self.clearstack()
        self.yamlgraph.finishgraph(pos)

    def start_document(self, directives, pos=None):
        self.checkstreamstarted()
        self.anchormap = {}
        self.yamlgraph.createcativy(pos)

    def end_document(self, pos=None):
        self.checkstreamstarted()
        self.clearstack()
        self.yamlgraph.readynextdoc(pos)

    def start_seq(self, anchor, tag, pos=None):
        self.checkstreamstarted()
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourseqnode = YAMLSeqNode([], tag, self.yamlgraph, pos)
        self.anchormap[anchor] = ourseqnode
        self.addcontainingthang(ourseqnode)
        self.nodestack.append(ourseqnode)

    def end_seq(self, pos=None):
        self.checkstreamstarted()
        while self.nodestack:
            nodepop = self.nodestack.pop()
            if nodepop.kind == YAMLNODE_SEQ:
                nodepop.setfinalpos(pos)
                return

    def start_map(self, anchor, tag, pos=None):
        self.checkstreamstarted()
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourmapnode = YAMLMapNode([], [], tag, self.yamlgraph, pos)
        self.anchormap[anchor] = ourmapnode
        self.addcontainingthang(ourmapnode)
        self.nodestack.append(ourmapnode)

    def end_map(self, pos=None):
        self.checkstreamstarted()
        while self.nodestack:
            nodepop = self.nodestack.pop()
            if nodepop.kind == YAMLNODE_MAP:
                if nodepop.status == YAMLMAP_STATUS_VALREADY:
                    nodepop.addnode(YAMLScalarNode("null", "!null"))
                nodepop.setfinalpos(pos)
                return

    def scalar(self, anchor, tag, scalarval, startpos=None, endpos=None):
        self.checkstreamstarted()
        if anchor in self.anchormap:
            raise YAMLDuplicateAnchorException(
                "Anchor '%s' already declared" % anchor)
        ourscalarnode = YAMLScalarNode(scalarval, tag, self.yamlgraph, startpos, endpos)
        self.anchormap[anchor] = ourscalarnode
        self.addcontainingthang(ourscalarnode)

    def alias(self, aliasval, startpos=None, endpos=None):
        self.checkstreamstarted()
        if aliasval not in self.anchormap:
            raise YAMLAliasLacksAnchorException(
                "Alias '%s' declared without corresponding anchor" % aliasval)
        self.addcontainingthang(self.anchormap[aliasval])

    def addcontainingthang(self, node):
        if self.nodestack:
            nodetop = self.nodestack[-1]
            nodetop.addnode(node)
        else:
            canaddnewdoc = self.yamlgraph.fillcavity(node)
            if not canaddnewdoc:
                raise YAMLComposeException("Duplicate document node")

