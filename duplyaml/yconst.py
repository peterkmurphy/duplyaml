#!/usr/bin/env python
# The duplyaml YAML processor.
# The yconst.py file.
# Common constants used in YAML.

# These are the constants used to define the Node kinds used with YAML nodes

YAMLNODE_DEF = 0 # Used with the YAMLNode class by default.
YAMLNODE_SCA = 1 # Used with scalar nodes.
YAMLNODE_SEQ = 2 # Used with sequence nodes.
YAMLNODE_MAP = 3 # Used with mapping nodes.

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

# Specific canonical values for particular types - from version 1.2

CAN_NULL = "null"
CAN_FALSE = "false"
CAN_TRUE = "true"

# y|Y|yes|Yes|YES|n|N|no|No|NO
#|true|True|TRUE|false|False|FALSE
#|on|On|ON|off|Off|OFF