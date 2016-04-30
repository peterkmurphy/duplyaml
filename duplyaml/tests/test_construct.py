#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from unittest import TestCase

from duplyaml import *

testnodes = [YAMLScalarNode(NULL_CAN, "!!null"),
    YAMLScalarNode(FALSE_CAN, "!!bool"),
    YAMLScalarNode(TRUE_CAN, "!!bool"),
    YAMLScalarNode("", "tag:yaml.org,2002:str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("685230", "!!int"),
    YAMLScalarNode("+685_230", "!!int"),
    YAMLScalarNode("0o2472256", "!!int"),
    YAMLScalarNode("0x_0A_74_AE", "!!int"),
    YAMLScalarNode("0b1010_0111_0100_1010_1110", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
    YAMLScalarNode(NAN_CAN, "!!float"),
    YAMLScalarNode(INF_CAN, "!!float"),
    YAMLScalarNode(NINF_CAN, "!!float"),
]

# print int_sex_regexp.match("190:20:30")


testresults = [None, False, True, "", 0, 685230, 685230, 685230, 685230, 685230, 0.0, NAN_PY, INF_PY, NINF_PY]

testexceptionnode = YAMLScalarNode("A", "!!int")

yconstructthing = YAMLConstructor()


class TestConstruct(TestCase):
    def test_scalar_construct(self):
        testlen = len(testnodes)
        for i in range(testlen):
            if isinstance(testresults[i], float) and math.isnan(testresults[i]):
                self.assertTrue(math.isnan(yconstructthing.construct(testnodes[i])))
            else:
                self.assertEqual(yconstructthing.construct(testnodes[i]), testresults[i])

#        self.assertRaises(YAMLConstructException, yconstructthing.construct, testexceptionnode)