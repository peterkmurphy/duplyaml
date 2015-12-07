from unittest import TestCase

from duplyaml import *

class TestGraph(TestCase):
    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))

class TestNodeEq(TestCase):
    def __init(self):
        yn = YAMLNode("!!null")
        sn = YAMLScalarNode("~", "!null")
        ln = YAMLSeqNode([], "!!seq")
        mn = YAMLMapNode([], [], "!!map")
        self.assertEquals(yn, yn)
        self.assertTrue(yn == yn)
        self.assertFalse(yn != yn)
        self.assertEquals(sn, sn)
        self.assertTrue(sn == sn)
        self.assertFalse(sn != sn)
        self.assertNotEquals(yn, sn)
        self.assertNotEquals(sn, yn)

    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))
        self.assertTrue(True)

