from unittest import TestCase

from duplyaml import YAMLGraph

class TestGraph(TestCase):
    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))

class TestGraph2(TestCase):
    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))
