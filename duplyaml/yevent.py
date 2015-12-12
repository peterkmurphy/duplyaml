#!/usr/bin/env python
# The duplyaml YAML processor.
# The yevent.py file.
# Represents YAML Events - used for serializing and composing.


class YAMLEvent:

# This is an interface for classes for composing or serializing.

    def __init__(self):
        pass

    def start_stream(self):
        pass

    def end_stream(self):
        pass

    def start_document(self, directives):
        pass

    def end_document(self):
        pass

    def start_seq(self, anchor, tag):
        pass

    def end_seq(self):
        pass

    def start_map(self, anchor, tag):
        pass

    def end_map(self):
        pass

    def scalar(self, anchor, tag, canvalue):
        pass

    def alias(self, aliasval):
        pass

    def comment(self, commentval):
        pass