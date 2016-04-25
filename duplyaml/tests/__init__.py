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
