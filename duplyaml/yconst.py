#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yconst.py file.
# Common constants used in YAML.

# These are the constants used to define the Node kinds used with YAML nodes

YAMLNODE_DEF = 0 # Used with the YAMLNode class by default.
YAMLNODE_SCA = 1 # Used with scalar nodes.
YAMLNODE_SEQ = 2 # Used with sequence nodes.
YAMLNODE_MAP = 3 # Used with mapping nodes.

# Special statuses for maps

YAMLMAP_STATUS_KEYREADY = 0
YAMLMAP_STATUS_VALREADY = 1

# YAML namespace prefix:

YAML_NAME_PREFIX = "tag:yaml.org,2002:"

# For converting nodes in YAML name prefix into !!tag formats

C_SECONDARY_TAG_HANDLE = "!!"

# Tag constants

TAG_MAP = "!!map" # Unordered set of key: value pairs without duplicates.
TAG_OMAP = "!!omap" # Ordered sequence of key: value pairs without duplicates.
TAG_PAIRS = "!!pairs" # Ordered sequence of key: value pairs allowing duplicates.
TAG_SET = "!!set" # Unordered set of non-equal values.
TAG_SEQ = "!!seq" # Sequence of arbitrary values.
TAG_BINARY = "!!binary" # A sequence of zero or more octets (8 bit values).
TAG_BOOL = "!!bool" # Mathematical Booleans.
TAG_FLOAT = "!!float" # Floating-point approximation to real numbers.
TAG_INT = "!!int" # Mathematical integers.
TAG_MERGE = "!!merge" # Specify one or more mappings to be merged with the current one.
TAG_NULL = "!!null" # Devoid of value.
TAG_STR = "!!str" # A sequence of zero or more Unicode characters.
TAG_TIMESTAMP = "!!timestamp" # A point in time.
TAG_VALUE = "!!value" # Specify the default value of a mapping.
TAG_YAML = "!!yaml" # Keys for encoding YAML in YAML.

# Extra ones that seems to be of use:

TAG_COMPLEX = "!!complex" # Represents complex numbers of form a+bj
TAG_FRACTION = "!!fraction" # Represents complex numbers of form a+bj
TAG_TIMEDELTA = "!!timedelta" # Represents time intervals

# The !!null and the !!bool tags are limited to a certain range of values.

TAG_NULL_VALUES = ["", "null", "Null", "NULL", "~"]

# There is an issue with !!bool. The YAML 1.2 standard has accepts a certain
# set of values for true and false. However, the Boolean Language-Independent
# Type for YAML Version 1.1 standard accepts more values for true and false.
# So we give the programmer the option of choosing one or the other.

TAG_TRUE_VALUES = ["true", "True", "TRUE"]
TAG_FALSE_VALUES = ["false", "False", "FALSE"]
TAG_FALSE_EXT_VALUES =  ["n", "N", "no", "No", "NO", "off", "Off", "OFF"]\
    +TAG_FALSE_VALUES
TAG_TRUE_EXT_VALUES = ["y", "Y", "yes", "Yes", "YES", "on", "On", "ON"]\
    +TAG_TRUE_VALUES

# Specific canonical values for particular types - from version 1.2

TAG_NULL_CAN = "null"
TAG_FALSE_CAN = "false"
TAG_TRUE_CAN = "true"

