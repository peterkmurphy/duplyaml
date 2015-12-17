#!/usr/bin/env python
# The duplyaml YAML processor.
# The duplyaml/tests/__init__.py file.
# Used to initialise testing.

from __future__ import absolute_import
import unittest
import doctest
import sys

# Idea from https://github.com/simplejson/simplejson/blob/master/setup.py

#class NoExtensionTestSuite(unittest.TestSuite):
#    def run(self, result):
#        import simplejson
#        simplejson._toggle_speedups(False)
#        result = unittest.TestSuite.run(self, result)
#        simplejson._toggle_speedups(True)
#        return result


class TestMissingSpeedups(unittest.TestCase):
    def runTest(self):
        if hasattr(sys, 'pypy_translation_info'):
            "PyPy doesn't need speedups! :)"
        elif hasattr(self, 'skipTest'):
            self.skipTest('_speedups.so is missing!')


def additional_tests(suite=None):
    import duplyaml
    if suite is None:
        suite = unittest.TestSuite()
#    for mod in (duplyaml,):
#        suite.addTest(doctest.DocTestSuite(mod))
#    suite.addTest(doctest.DocFileSuite('../../index.rst'))
    return suite


def all_tests_suite():
    def get_suite():
        return additional_tests(
            unittest.TestLoader().loadTestsFromNames([
                'duplyaml.tests.test_graph',
                'duplyaml.tests.test_represent',
                'duplyaml.tests.test_construct',
                'duplyaml.tests.test_serialize',
            ]))
    suite = get_suite()
#    import simplejson
#    if simplejson._import_c_make_encoder() is None:
#        suite.addTest(TestMissingSpeedups())
#    else:
#        suite = unittest.TestSuite([
#            suite,
#            NoExtensionTestSuite([get_suite()]),
#        ])
    return suite


def main():
    runner = unittest.TextTestRunner(verbosity=1 + sys.argv.count('-v'))
    suite = all_tests_suite()
    raise SystemExit(not runner.run(suite).wasSuccessful())


if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    main()
