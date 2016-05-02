#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from duplyaml import *
from duplyaml.tests import buildseqstrings, UNICODE_PLAT_CHARS

# We are testing the "canonical" representation of scalars. We start by tesing
# built in values like NotImplemented, Ellipses, and Nulls and Booleans.

testscalars = [None, False, True, Ellipsis, NotImplemented]

testscalars += [0, 0.0, NAN_PY, INF_PY, NINF_PY]
testresults = [YAMLScalarNode(NULL_CAN, "!!null"),
    YAMLScalarNode(FALSE_CAN, "!!bool"),
    YAMLScalarNode(TRUE_CAN, "!!bool"),
    YAMLScalarNode("Ellipses", "!!ellipsis"),
    YAMLScalarNode("Not Implemented", "!!notimp")]

testresults += [YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
    YAMLScalarNode(NAN_CAN, "!!float"),
    YAMLScalarNode(INF_CAN, "!!float"),
    YAMLScalarNode(NINF_CAN, "!!float"),
               ]
yrepresentthing = YAMLRepresenter()


class TestRepresent(TestCase):
    def test_str_represents(self):
        ourunicodecombo = buildseqstrings(UNICODE_PLAT_CHARS, 0)
        for stritem in ourunicodecombo:
            self.assertEqual(yrepresentthing.createnode(stritem), YAMLScalarNode(stritem, "!!str"))


    def test_scalar_represents(self):
        testlen = len(testscalars)
        for i in range(testlen):
            self.assertEqual(yrepresentthing.createnode(testscalars[i]), testresults[i])
