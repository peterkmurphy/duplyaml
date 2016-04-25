#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase

from duplyaml import *
import os
import sys
from duplyaml.tests.globaltestdata import *

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

