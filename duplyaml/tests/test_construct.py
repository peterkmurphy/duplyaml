#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from duplyaml import *

testnodes = [YAMLScalarNode(TAG_NULL_CAN, "!!null"),
    YAMLScalarNode(TAG_FALSE_CAN, "!!bool"),
    YAMLScalarNode(TAG_TRUE_CAN, "!!bool"),
    YAMLScalarNode("", "tag:yaml.org,2002:str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("685230", "!!int"),
    YAMLScalarNode("+685_230", "!!int"),
    YAMLScalarNode("0o2472256", "!!int"),
    YAMLScalarNode("0x_0A_74_AE", "!!int"),
    YAMLScalarNode("0b1010_0111_0100_1010_1110", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
]

# print int_sex_regexp.match("190:20:30")


testresults = [None, False, True, "", 0, 685230, 685230, 685230, 685230, 685230, 0.0]

testexceptionnode = YAMLScalarNode("A", "!!int")

yconstructthing = YAMLConstructor()


class TestConstruct(TestCase):
    def test_scalar_construct(self):
        testlen = len(testnodes)
        for i in range(testlen):
            self.assertEqual(yconstructthing.construct(testnodes[i]), testresults[i])

#        self.assertRaises(YAMLConstructException, yconstructthing.construct, testexceptionnode)