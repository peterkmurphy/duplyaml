from unittest import TestCase

from duplyaml import YAMLGraph

class TestGraph(TestCase):
    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertFalse(isinstance(yg.src, basestring))