from unittest import TestCase

from duplyaml import *

testnodes = [YAMLScalarNode(TAG_NULL_CAN, "!!null"),
    YAMLScalarNode(TAG_FALSE_CAN, "!!bool"),
    YAMLScalarNode(TAG_TRUE_CAN, "!!bool"),
    YAMLScalarNode("", "!!str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
               ]
testresults = [None, False, True, "", 0, 0.0]

testexceptionnode = YAMLScalarNode("A", "!!int")

yconstructthing = YAMLConstructor()


class TestConstruct(TestCase):
    def test_scalar_construct(self):
        testlen = len(testnodes)
        for i in range(testlen):
            self.assertEqual(yconstructthing.construct(testnodes[i]), testresults[i])

        self.assertRaises(YAMLConstructException, yconstructthing.construct, testexceptionnode)