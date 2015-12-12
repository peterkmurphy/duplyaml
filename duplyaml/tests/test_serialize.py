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
Yase = YAMLSerializer(ygapher)
Yase.serializestream()
