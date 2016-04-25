#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yload.py file.
# Used for loading YAML streams.

from .yevent import YAMLEvent

class YAMLPos:
    """ Represents a position in a YAML stream.
    """
    def __init__(self, charpos, linepos, colpos):
        """
        :param charpos: the character position in the stream (starts at 0).
        :param linepos: the line position in the stream (starts at 1).
        :param colpos: the column position in the stream (starts at 0).
        """
        self.charpos = charpos
        self.linepos = linepos
        self.colpos = colpos


class YAMLLoad:
    """ The YAMLLoad class loads YAML data from a stream and attempts to
    serialize it as a series of YAML events. These events can then be used
    to
    """

    def __init__(self, yamlfile, src, yamleventer=YAMLEvent(None)):
        """ Initialises the class.
        :param yamlfile: a .read()-supporting file-like object with YAML in it.
        :param src: an identifier of the src of the YAML data (e.g. file name).
        :param yamleventer: A YAMLEvent with serialization methods inside.
        """
        self.yamlfile = yamlfile
        self.src = src
        self.yamleventer = yamleventer

# These contain position markers.

        self.charpos = None
        self.linepos = None
        self.colpos = None

# This contains the current line buffer.

        self.buffer = None

    def getpos(self):
        """
        :return: Returns the current position in the stream.
        """
        return YAMLPos(self.charpos, self.linepos, self.colpos)

    def parse(self):
        """ Parses the stream.
        :return:True.
        """
        self.charpos = 0
        self.linepos = 1
        self.colpos = 0
        self.buffer = ""

# The main production for this method is:
# [211] l-yaml-stream ::= l-document-prefix* l-any-document?
# ( l-document-suffix+ l-document-prefix* l-any-document?
# | l-document-prefix* l-explicit-document? )*

# But we need to work with:



        self.yamleventer.start_stream(self.getpos())



# After all is said and done, everything ends with.

        self.yamleventer.end_stream(self.getpos())
        return True
