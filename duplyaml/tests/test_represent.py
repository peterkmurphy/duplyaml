#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from duplyaml import *

testscalars = [None, False, True, "", 0, 0.0, NAN_PY, INF_PY, NINF_PY]
testresults = [YAMLScalarNode(NULL_CAN, "!!null"),
    YAMLScalarNode(FALSE_CAN, "!!bool"),
    YAMLScalarNode(TRUE_CAN, "!!bool"),
    YAMLScalarNode("", "!!str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
    YAMLScalarNode(NAN_CAN, "!!float"),
    YAMLScalarNode(INF_CAN, "!!float"),
    YAMLScalarNode(NINF_CAN, "!!float"),
               ]
yrepresentthing = YAMLRepresenter()


class TestRepresent(TestCase):
    def test_scalar_represents(self):
        testlen = len(testscalars)
        for i in range(testlen):
            self.assertEqual(yrepresentthing.createnode(testscalars[i]), testresults[i])
