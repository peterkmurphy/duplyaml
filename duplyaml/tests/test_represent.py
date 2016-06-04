#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from duplyaml import *
from duplyaml.tests import buildseqstrings, UNICODE_PLAT_CHARS
import fractions
import decimal

# We are going to test two representers - one with the defaults, and one
# with a lot of alternative settings.

yrepresent_def = YAMLRepresenter()
yrepresent_alt = YAMLRepresenter(represent_lity_full = YAML_NAME_PREFIX,
        nulldeflt = "~", falsedeflt = "OFF", truedeflt = "ON",
        elldeflt = "...", notimpdeflt = "undefined", infdeflt = ".INF",
        ninfldeflt = "-.INF", nandeflt = ".NAN", reptuple = True,
        repfrozenset = True)

# We are testing the "canonical" representation of scalars. We start by tesing
# built in values like NotImplemented, Ellipses, and Nulls and Booleans.

buildinvalues_def = (None, False, True, Ellipsis, NotImplemented, NAN_PY,
    INF_PY, NINF_PY,)

buildinvalues_res = [YAMLScalarNode(NULL_CAN, "!!null"),
    YAMLScalarNode(FALSE_CAN, "!!bool"),
    YAMLScalarNode(TRUE_CAN, "!!bool"),
    YAMLScalarNode("Ellipses", "!!python/ellipsis"),
    YAMLScalarNode("Not Implemented", "!!python/notimp"),
    YAMLScalarNode(NAN_CAN, "!!float"),
    YAMLScalarNode(INF_CAN, "!!float"),
    YAMLScalarNode(NINF_CAN, "!!float")]

# This is an alternative representation which could be produced.

buildinvalues_alt = [YAMLScalarNode("~", "tag:yaml.org,2002:null"),
    YAMLScalarNode("OFF", "tag:yaml.org,2002:bool"),
    YAMLScalarNode("ON", "tag:yaml.org,2002:bool"),
    YAMLScalarNode("...", "!!python/ellipsis"),
    YAMLScalarNode("undefined", "!!python/notimp"),
    YAMLScalarNode(".NAN", "tag:yaml.org,2002:float"),
    YAMLScalarNode(".INF", "tag:yaml.org,2002:float"),
    YAMLScalarNode("-.INF", "tag:yaml.org,2002:float")]

class TestRepresent(TestCase):

    def checkfloats(self, formednode, expectednode):
        formednodeval = float(formednode.scalarval)
        expectednodeval = float(expectednode.scalarval)
        if formednodeval == 0.0 and expectednodeval == 0.0:
            return
        if formednodeval/expectednodeval == 1.0:
            return
        self.assertEqual(formednode, expectednode)

    def test_buildinvalues_represents(self):
        testlen = len(buildinvalues_def)
        for i in range(testlen):
            self.assertEqual(yrepresent_def.createnode(buildinvalues_def[i]),
                buildinvalues_res[i])
            self.assertEqual(yrepresent_alt.createnode(buildinvalues_def[i]),
                     buildinvalues_alt[i])

    def test_intvalues_represents(self):

# This does the simple stuff - testing from -10 to 10.

        for i in range(-10, 11):
            self.assertEqual(yrepresent_def.createnode(i),
                YAMLScalarNode(str(i), "!!int"))
            self.assertEqual(yrepresent_alt.createnode(i),
                YAMLScalarNode(str(i), "tag:yaml.org,2002:int"))

# This does the more complicated stuff - this handles the sequence -2^i + i
# for i from 2 to 120

        for i in [((-2)**i)+i for i in range(2, 120)]:
            self.assertEqual(yrepresent_def.createnode(i),
                YAMLScalarNode(str(i), "!!int"))
            self.assertEqual(yrepresent_alt.createnode(i),
                YAMLScalarNode(str(i), "tag:yaml.org,2002:int"))

    def test_fracvalues_represents(self):
        # This does the simple stuff - testing from a/b for -20 <= a < 20,
        # 1 <= b < 10.

        for i in range(-20, 20):
            for j in range(1, 10):
                ourfraction = fractions.Fraction(i, j)
                self.assertEqual(yrepresent_def.createnode(ourfraction),
                     YAMLScalarNode(str(ourfraction), "!!python/fraction"))

    def test_compvalues_represents(self):
        # This does the simple stuff - testing from a+bi for -20 <= a < 20,
        # -20 <= b < 20.

        for i in range(-20, 20):
            for j in range(-20, 20):
                ourcomplex = complex(i, j)
                self.assertEqual(yrepresent_def.createnode(ourcomplex),
                                 YAMLScalarNode(str(ourcomplex), "!!python/complex"))

    def test_decimalvalues_represents(self):
        # This does the simple stuff - testing from a+bi for -20 <= a < 20,
        # -20 <= b < 20.

        for i in range(10):
            for j in range(10):
                for k in range(2):
                    ourdecimal = decimal.Decimal(k, [i, j])
                    self.assertEqual(yrepresent_def.createnode(ourdecimal),
                                 YAMLScalarNode(str(ourdecimal), "!!python/decimal"))

    def test_floatvalues_represents(self):

        # This does the simple stuff - testing from -10 to 10.

        for i in range(-10, 11):
            self.checkfloats(yrepresent_def.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "!!float"))
            self.checkfloats(yrepresent_alt.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "tag:yaml.org,2002:float"))

        # Now it is -10/3, -9/3, -8/3 ... to 10/3

        for i in range(-10, 11):
            self.checkfloats(yrepresent_def.createnode(i/3.0),
                             YAMLScalarNode(str(i/3.0), "!!float"))
            self.checkfloats(yrepresent_alt.createnode(i/3.0),
                             YAMLScalarNode(str(i/3.0), "tag:yaml.org,2002:float"))


        # This does the more complicated stuff - this handles the sequence -2^i + i
        # for i from 2 to 120

        for i in [((-2) ** i) + i for i in range(2, 120)]:
            self.checkfloats(yrepresent_def.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "!!float"))
            self.checkfloats(yrepresent_alt.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "tag:yaml.org,2002:float"))

        # This does the more complicated stuff - this handles the sequence -2^i + i/3
        # for i from 2 to 120

        for i in [((-2) ** i) + i/3.0 for i in range(2, 120)]:
            self.checkfloats(yrepresent_def.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "!!float"))
            self.checkfloats(yrepresent_alt.createnode(float(i)),
                             YAMLScalarNode(str(float(i)), "tag:yaml.org,2002:float"))


    def test_str_represents(self):
        ourunicodecombo = buildseqstrings(UNICODE_PLAT_CHARS, 0)
        for stritem in ourunicodecombo:
            self.assertEqual(yrepresent_def.createnode(stritem),
                YAMLScalarNode(stritem, "!!str"))
        for stritem in ourunicodecombo:
            self.assertEqual(yrepresent_alt.createnode(stritem),
                YAMLScalarNode(stritem, "tag:yaml.org,2002:str"))

    def test_list_represents(self):
        self.assertEqual(yrepresent_def.createnode(buildinvalues_def),
              YAMLSeqNode(buildinvalues_res, "!!seq"))
        self.assertEqual(yrepresent_alt.createnode(buildinvalues_def),
              YAMLSeqNode(buildinvalues_alt, "!!python/tuple"))
       # print YAMLSeqNode([], "!!python/tuple")