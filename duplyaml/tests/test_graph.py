from unittest import TestCase

from duplyaml import *

yn0 = YAMLNode("!!null")
yn1 = YAMLNode("!!null")
yn2 = YAMLNode("!!str")
yn3 = YAMLNode("!!seq")
yn4 = YAMLNode("!!map")
sn0 = YAMLScalarNode("null", "!!null")
sn1 = YAMLScalarNode("null", "!!null")
sn2 = YAMLScalarNode("", "!!str")
sn3 = YAMLScalarNode("Test", "!!str")
sn4 = YAMLScalarNode("test", "!!str")
yncol = [yn0, yn1, yn2, yn3, yn4]
sncol = [sn0, sn1, sn2, sn3, sn4]
ln0 = YAMLSeqNode([], "!!seq")
ln1 = YAMLSeqNode([], "!!seq")
ln2 = YAMLSeqNode([], "!!seq")
ln2.addnode(sn0)
ln3 = YAMLSeqNode([], "!!seq")
ln3.addnode(sn1)
ln4 = YAMLSeqNode([], "!!seq")
ln4.addnode(sn2)
ln5 = YAMLSeqNode([], "!!seq")
ln5.addnode(sn3)
ln6 = YAMLSeqNode([], "!!seq")
ln6.addnode(sn4)
ln7 = YAMLSeqNode([], "!!omap")
ln8 = YAMLSeqNode([], "!!seq")
ln8.addnode(ln8)
ln9 = YAMLSeqNode([], "!!seq")
ln9.addnode(ln9)
ln10 = YAMLSeqNode([], "!!seq")
ln11 = YAMLSeqNode([], "!!seq")
ln10.addnode(ln11)
ln11.addnode(sn1)
ln12 = YAMLSeqNode([], "!!seq")
ln11.addnode(ln12)
ln12.addnode(ln10)
ln13 = YAMLSeqNode([], "!!seq")
ln14 = YAMLSeqNode([], "!!seq")
ln13.addnode(ln14)
ln14.addnode(sn1)
ln15 = YAMLSeqNode([], "!!seq")
ln14.addnode(ln15)
ln15.addnode(ln13)
ln16 = YAMLSeqNode([], "!!seq")
ln17 = YAMLSeqNode([], "!!seq")
ln16.addnode(ln17)
ln18 = YAMLSeqNode([], "!!seq")
ln17.addnode(ln18)
ln17.addnode(sn1)
ln18.addnode(ln16)

lncol = [ln0, ln1, ln2, ln3, ln4, ln5, ln6, ln7, ln8, ln9, ln10, ln13, ln16]
lnlen = len(lncol)

mn0 = YAMLMapNode([], [], "!!map")
mn1 = YAMLMapNode([], [], "!!map")
mn2 = YAMLMapNode([], [], "!!set")
mn3 = YAMLMapNode([], [], "!!set")
mn4 = YAMLMapNode([sn2], [sn0], "!!map")
mn5 = YAMLMapNode([sn2], [sn1], "!!map")
mn6 = YAMLMapNode([sn2], [sn0], "!!set")
mn7 = YAMLMapNode([sn2], [sn1], "!!set")
mn8 = YAMLMapNode([sn3], [sn0], "!!set")
mn9 = YAMLMapNode([sn3], [sn1], "!!set")
mn10 = YAMLMapNode([sn4], [sn0], "!!set")
mn11 = YAMLMapNode([sn4], [sn1], "!!set")

mn12 = YAMLMapNode([sn2, mn4], [sn0, sn1], "!!map")
mn13 = YAMLMapNode([sn2, mn5], [sn1, sn0], "!!map")
mn14 = YAMLMapNode([sn2, mn6], [sn0, sn1], "!!set")
mn15 = YAMLMapNode([sn2, mn7], [sn1, sn0], "!!set")
mn16 = YAMLMapNode([sn3, mn8], [sn0, sn1], "!!set")
mn17 = YAMLMapNode([sn3, mn9], [sn1, sn0], "!!set")
mn18 = YAMLMapNode([sn4, mn10], [sn0, sn1], "!!set")
mn19 = YAMLMapNode([sn4, mn11], [sn1, sn0], "!!set")

mn20 = YAMLMapNode([sn2], [sn0], "!!map")
mn20.addkvpair(mn20, sn0)
mn21 = YAMLMapNode([sn2], [sn1], "!!map")
mn21.addkvpair(mn21, sn1)

mn22 = YAMLMapNode([], [], "!!map")
mn22.addkvpair(mn20, sn0)
mn22.addkvpair(sn2, ln10)

mn23 = YAMLMapNode([], [], "!!map")
mn23.addkvpair(mn21, sn1)
mn23.addkvpair(sn2, ln13)

mncol = [mn0, mn1, mn2, mn3, mn4, mn5, mn6, mn7, mn8, mn9, mn10, mn11,
         mn12, mn13, mn14, mn15, mn16, mn17, mn18, mn19, mn20, mn21, mn22, mn23]
mnlen = len(mncol)

class TestGraph(TestCase):
    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))

class TestNodeEq(TestCase):
    def test_node_equal(self):
        for yn in yncol:
            self.assertTrue(yn == yn)
            self.assertFalse(yn != yn)
        self.assertTrue(yn0, yn1)
        for yn in [yn2, yn3, yn4]:
            self.assertTrue(yn0 != yn)
        self.assertFalse(yn2 == yn3)
        self.assertFalse(yn3 == yn4)
        self.assertFalse(yn4 == yn2)

        for sn in sncol:
            self.assertTrue(sn == sn)
            self.assertFalse(sn != sn)
        self.assertTrue(sn0, sn1)
        for sn in [sn2, sn3, sn4]:
            self.assertTrue(sn0 != sn)
        self.assertFalse(sn2 == sn3)
        self.assertFalse(sn3 == sn4)
        self.assertFalse(sn4 == sn2)

        for yn in yncol:
            for sn in sncol:
                self.assertNotEqual(yn, sn)
                self.assertNotEqual(sn, yn)
                self.assertTrue(yn != sn)
                self.assertFalse(yn == sn)

        for ln in lncol:
            for sn in sncol:
                self.assertNotEqual(ln, sn)
                self.assertNotEqual(ln, sn)
                self.assertTrue(ln != sn)
                self.assertFalse(ln == sn)
            for yn in yncol:
                self.assertNotEqual(ln, yn)
                self.assertNotEqual(ln, yn)
                self.assertTrue(ln != yn)
                self.assertFalse(ln == yn)

        for i in range(lnlen):
            for j in range(lnlen):
                if i == j or set([i, j]) in [set([0, 1]), set([2, 3]), set([8, 9]), set([10, 11])]:
                    self.assertTrue(lncol[i] == lncol[j])
                    self.assertFalse(lncol[i] != lncol[j])
                else:
                    self.assertTrue(lncol[i] != lncol[j])
                    self.assertFalse(lncol[i] == lncol[j])

        for i in range(mnlen):
            for j in range(mnlen):
                if i == j or set([i, j]) in [set([0, 1]), set([2, 3]), set([4, 5]), set([6, 7]),
                        set([8, 9]), set([10, 11]), set([12, 13]), set([14, 15]),
                        set([16, 17]), set([18, 19]), set([20, 21]), set([22, 23])]:
                    self.assertTrue(mncol[i] == mncol[j])
                    self.assertFalse(mncol[i] != mncol[j])
                else:
                    self.assertTrue(mncol[i] != mncol[j])
                    self.assertFalse(mncol[i] == mncol[j])



    def test_is_graph(self):
        yg = YAMLGraph("test")
        self.assertTrue(isinstance(yg.src, basestring))
        self.assertTrue(True)

