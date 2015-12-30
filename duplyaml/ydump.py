#!/usr/bin/env python
# The duplyaml YAML processor.
# The ydump.py file.
# Used for dumping YAML streams.

from .yevent import YAMLEvent

DUMPSTACK_STATE_SEQ = 1
DUMPSTACK_STATE_MAPKEY = 2
DUMPSTACK_STATE_MAPVAL = 3


class YAMLDump(YAMLEvent):
    """ The YAMLDump class dumps YAML data to a stream, based on serialization
    events (which are delivered by calls to its routines).

    By default, the YAMLDump (first version) prints stuff in "canonical" form.
    """

    def __init__(self, yamlfile, indentsize = 4):
        """ Initialises the class.
        :param yamlfile: a .write()-supporting file-like object for YAML.
        :param indentsize: by how many characters should text be indented?
        """
        self.yamlfile = yamlfile
        self.indentsize = indentsize
        self.currentindent = 0
        self.stackstate = []

    def start_stream(self, pos=None):
        self.currentindent = 0

    def end_stream(self, pos=None):
        self.currentindent = 0

    def writelinesep(self, strin):
        self.yamlfile.write(strin)
        self.yamlfile.write("\n")

    def start_document(self, directives, pos=None):
        for direc in directives:
            self.yamlfile.writeline("%"+direc+ " "+directives[direc])
        self.writelinesep("---")
        self.currentindent = 0

    def end_document(self, pos=None):
        self.writelinesep("...")
        self.currentindent = 0

    def indent(self):
        self.yamlfile.write(" " * self.currentindent)

    def writeanchorandtag(self, anchor, tag):
        if anchor:
            self.yamlfile.write("&"+anchor+" ")
        if tag:
            self.yamlfile.write(tag+" ")

    def writeprecursor(self):
        if self.stackstate:
            if self.stackstate[-1] == DUMPSTACK_STATE_MAPKEY:
                self.yamlfile.write("? ")
                self.stackstate[-1] = DUMPSTACK_STATE_MAPVAL
            if self.stackstate[-1] == DUMPSTACK_STATE_MAPVAL:
                self.yamlfile.write(": ")
                self.stackstate[-1] = DUMPSTACK_STATE_MAPKEY

    def writesuccessor(self):
        if self.stackstate:
            if self.stackstate[-1] in [DUMPSTACK_STATE_MAPVAL,
                                       DUMPSTACK_STATE_SEQ]:
                self.yamlfile.write(",")
        self.writelinesep("")


    def start_seq(self, anchor, tag, pos=None):
        self.indent()
        self.writeprecursor()
        self.writeanchorandtag(anchor, tag)
        self.writelinesep("[")
        self.currentindent += self.indentsize
        self.stackstate.append(DUMPSTACK_STATE_SEQ)

    def end_seq(self, pos=None):
        self.stackstate.pop()
        self.currentindent -= self.indentsize
        self.indent()
        self.yamlfile.write("]")
        self.writesuccessor()


    def start_map(self, anchor, tag, pos=None):
        self.indent()
        self.writeprecursor()
        self.writeanchorandtag(anchor, tag)
        self.writelinesep("{")
        self.currentindent += self.indentsize
        self.stackstate.append(DUMPSTACK_STATE_MAPKEY)

    def end_map(self, pos=None):
        self.stackstate.pop()
        self.currentindent -= self.indentsize
        self.indent()
        self.yamlfile.write("}")
        self.writesuccessor()

    def scalar(self, anchor, tag, scalarval, startpos=None, endpos=None):
        self.indent()
        self.writeprecursor()
        self.writeanchorandtag(anchor, tag)
        self.yamlfile.write("\"")
        self.yamlfile.write(scalarval)
        self.yamlfile.write("\"")
        self.writesuccessor()

    def alias(self, aliasval, startpos=None, endpos=None):
        self.indent()
        self.writeprecursor()
        self.yamlfile.write("*"+aliasval)
        self.writesuccessor()

