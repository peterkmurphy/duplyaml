from unittest import TestCase

from duplyaml import *

testscalars = [None, False, True, "", 0, 0.0]
testresults = [YAMLScalarNode(CAN_NULL, "!!null"),
    YAMLScalarNode(CAN_FALSE, "!!bool"),
    YAMLScalarNode(CAN_TRUE, "!!bool"),
    YAMLScalarNode("", "!!str"),
    YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
               ]
yrepresentthing = YAMLRepresenter()


class TestRepresent(TestCase):
    def test_scalar_represents(self):
        testlen = len(testscalars)
        for i in range(testlen):
            self.assertEqual(yrepresentthing.createnode(testscalars[i]), testresults[i])
