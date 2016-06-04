#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The duplyaml/tests/__init__.py file.
# Used to initialise testing.

from __future__ import absolute_import
import unittest
import duplyaml
import doctest
import sys
import os

# This builds a binary sequence of bytes

ALL_BYTES = bytes([i for i in range(256)])
#print ALL_BYTES
#print len(ALL_BYTES)
#print isinstance(ALL_BYTES, bytes)

# This gets a list of all Unicode character on the current platform

UNICODE_PLAT_CHARS = [unichr(i) for i in range(sys.maxunicode + 1)]


def extender(baseitems, charstoextend):
    """ This goes through all items all the items in

    :param baseitems: a sequence of strings
    :param charstoextend: a string consisting of the extension characters
    :return: A sequence of strings.
    """
    ourextension = [baseitem+extending for baseitem in baseitems for extending in charstoextend]
    return ourextension

def buildseqstrings(charstoproduce, ilenmax = 0):
    returnval = [""]
    cumulativeval = [""]
    while ilenmax > 0:
        ilenmax -= 1
        cumulativeval = extender(cumulativeval, charstoproduce)
        returnval.extend(cumulativeval)
    return returnval


def buildseqbytes(bytestoproduce, ilenmax = 0):
    returnval = [bytes()]
    cumulativeval = [bytes()]
    while ilenmax > 0:
        ilenmax -= 1
        cumulativeval = extender(cumulativeval, bytestoproduce)
        returnval.extend(cumulativeval)
    return returnval

#print buildseqstrings("DEF", 0)
#print buildseqstrings("DEF", 1)
#print buildseqstrings("DEF", 2)
#print buildseqstrings(bytearray("\x00\x01\x02"), 0)
#print buildseqstrings(bytearray("\x00\x01\x02"), 1)
#print buildseqstrings(bytearray("\x00\x01\x02"), 2)

#print extender([bytes()], bytes("\x00\x01\x02"))
#print extender(extender([bytes()], bytes("\x00\x01\x02")), bytes("\x00\x01\x02"))


def additional_tests(suite=None):
    if suite is None:
        suite = unittest.TestSuite()
    return suite

def all_tests_suite():
    def get_suite():
        return additional_tests(
            unittest.TestLoader().loadTestsFromNames(['duplyaml.tests.'+f[:-3]
                for f in os.listdir('duplyaml/tests') if f[-3:] == '.py'
                and f[:5] == 'test_']))
    suite = get_suite()
    return suite

def main():
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
    suite = all_tests_suite()
    raise SystemExit(not runner.run(suite).wasSuccessful())

if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))))
    main()
