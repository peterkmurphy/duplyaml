#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from duplyaml import *
from duplyaml.tests import buildseqstrings, UNICODE_PLAT_CHARS

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

buildinvalues_def = [None, False, True, Ellipsis, NotImplemented, NAN_PY,
    INF_PY, NINF_PY]

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



#    None, False, True, Ellipsis, NotImplemented, NAN_PY,
#    INF_PY, NINF_PY]



# We are testing the "canonical" representation of scalars. We start by tesing
# built in values like NotImplemented, Ellipses, and Nulls and Booleans.

testscalars = [None, False, True, Ellipsis, NotImplemented]

testscalars += [0, 0.0, NAN_PY, INF_PY, NINF_PY]
testresults = [YAMLScalarNode(NULL_CAN, "!!null"),
    YAMLScalarNode(FALSE_CAN, "!!bool"),
    YAMLScalarNode(TRUE_CAN, "!!bool"),
    YAMLScalarNode("Ellipses", "!!python/ellipsis"),
    YAMLScalarNode("Not Implemented", "!!python/notimp")]

testresults += [YAMLScalarNode("0", "!!int"),
    YAMLScalarNode("0.0", "!!float"),
    YAMLScalarNode(NAN_CAN, "!!float"),
    YAMLScalarNode(INF_CAN, "!!float"),
    YAMLScalarNode(NINF_CAN, "!!float"),
               ]



class TestRepresent(TestCase):
    def test_buildinvalues_represents(self):
        testlen = len(buildinvalues_def)
        for i in range(testlen):
            self.assertEqual(yrepresent_def.createnode(buildinvalues_def[i]),
                buildinvalues_res[i])
            self.assertEqual(yrepresent_alt.createnode(buildinvalues_def[i]),
                     buildinvalues_alt[i])



    def test_str_represents(self):
        ourunicodecombo = buildseqstrings(UNICODE_PLAT_CHARS, 0)
        for stritem in ourunicodecombo:
            self.assertEqual(yrepresent_def.createnode(stritem), YAMLScalarNode(stritem, "!!str"))


    def test_scalar_represents(self):
        testlen = len(testscalars)
        for i in range(testlen):
            self.assertEqual(yrepresent_def.createnode(testscalars[i]), testresults[i])
