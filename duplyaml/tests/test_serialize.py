from unittest import TestCase

from duplyaml import *



sn0 = YAMLScalarNode("null", "!!null")
sn1 = YAMLScalarNode("null", "!!null")
sn2 = YAMLScalarNode("", "!!str")
sn3 = YAMLScalarNode("Test", "!!str")
sn4 = YAMLScalarNode("test", "!!str")
sncol = [sn0, sn1, sn2, sn3, sn4]
mn = YAMLMapNode(sncol, sncol, "!!map")
sncol.append(mn)
listicle = YAMLSeqNode(sncol, "!!seq")
ygapher = YAMLGraph("l")
ygapher.add_doc(listicle)
ygapher.add_doc(sn0)
ygapher.add_doc(sn1)
ygapher.add_doc(sn2)
ygapher.add_doc(sn3)
ygapher.add_doc(sn4)
ygapher.add_doc(mn)
Yase = YAMLSerializer(ygapher, YAMLComposer(None))
Yase.serializestream()

import StringIO

YAdumpit = YAMLSerializer(ygapher,YAMLDump(StringIO.StringIO()))
YAdumpit.serializestream()

class TestSerialise(TestCase):
    def test_serialisation(self):
        testlen = len(ygapher.children)
        for i in range(testlen):
            self.assertEqual(ygapher.children[i], Yase.yamlgraph.children[i])