#!/usr/bin/env python
# The duplyaml YAML processor.
# The yevent.py file.
# Contains the class YAMLEvent - the base for all classes that are the target
# of YAML serialisation events.


class YAMLEvent:
    """ The YAMLEvent class is an interface for all classes that process YAML
    serialisation events. An instant of a YAMLEvent/YAMLEvent descendant is
    passed to another class instance - the sender - and each method inside
    the YAMLEvent instance represents a YAML serialization event. The sender
    calls methods in the YAMLEvent instance to "send" events to it.

    By itself, YAMLEvent does nothing - is is just an interface. The
    implementations are more interesting, such as:

    - YAMLCompose: takes serialisation events and forms a YAMLGraph.
    - YAMLDump: takes serialisations events and creates a YAML stream.
    """

    def __init__(self, src):
        """ Initialises the class.
        :param src: Any "source" of the events - such as a YAML file, a YAML
        URL or (by convention) None when the YAML data comes from native data.
        """
        self.src = src

    def start_stream(self, pos=None):
        """ Called when starting the stream.
        :param pos: The starting position of the stream
        """
        pass

    def end_stream(self, pos=None):
        """ Called when ending the stream.
        :param pos: The ending position of the stream
        """
        pass

    def start_document(self, directives, pos=None):
        """ Called when starting a document.
        :param directives: a dictionary; the YAML directives for the document
        :param pos: The starting position of the document
        """
        pass

    def end_document(self, pos=None):
        """ Called when ending a document.
        :param pos: The ending position of the document
        """
        pass

    def start_seq(self, anchor, tag, pos=None):
        """ Called when starting a sequence.
        :param anchor: the anchor value for the sequence, or "" if not present.
        :param tag: the tag for the sequence, or "" if not present.
        :param pos: The starting position of the sequence
        """
        pass

    def end_seq(self, pos=None):
        """ Called when ending a sequence.
        :param pos: The ending position of the sequence
        """
        pass

    def start_map(self, anchor, tag, pos=None):
        """ Called when starting a mapping.
        :param anchor: the anchor value for the mapping, or "" if not present.
        :param tag: the tag for the mapping, or "" if not present.
        :param pos: The starting position of the mapping
        """
        pass

    def end_map(self, pos=None):
        """ Called when ending a map.
        :param pos: The ending position of the map
        """
        pass

    def scalar(self, anchor, tag, scalarval, startpos=None, endpos=None):
        """ Called when delivering a scalar.
        :param anchor: the anchor value for the scalar, or "" if not present.
        :param tag: the tag for the scalar, or "" if not present.
        :param scalarval: the value of the scalar
        :param startpos: the starting position of the scalar
        :param endpos: the ending position of the scalar
        """
        pass

    def alias(self, aliasval, startpos=None, endpos=None):
        """ Called when delivering an alias.
        :param aliasval: the value of the alias
        :param startpos: the starting position of the alias
        :param endpos: the ending position of the alias
        """
        pass

