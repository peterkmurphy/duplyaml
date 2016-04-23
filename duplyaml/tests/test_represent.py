from unittest import TestCase

from duplyaml import *

testscalars = [None, False, True, "", 0, 0.0, float("nan")]
testresults = [YAMLScalarNode(TAG_NULL_CAN, "!!null"),
    YAMLScalarNode(TAG_FALSE_CAN, "!!bool"),
    YAMLScalarNode(TAG_TRUE_CAN, "!!bool"),
    YAMLScalarNode("", "!!str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
    YAMLScalarNode("nan", "!!float"),

               ]
yrepresentthing = YAMLRepresenter()


class TestRepresent(TestCase):
    def test_scalar_represents(self):
        testlen = len(testscalars)
        for i in range(testlen):
            self.assertEqual(yrepresentthing.createnode(testscalars[i]), testresults[i])
