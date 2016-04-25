#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The duplyaml YAML processor.
# The yexcept.py file.
# Used for YAMLExceptions

class YAMLException(Exception):
    pass

class YAMLConstructException(YAMLException):
    pass

class YAMLComposeException(YAMLException):
    pass

class YAMLAliasLacksAnchorException(YAMLComposeException):
    pass

class YAMLDuplicateAnchorException(YAMLComposeException):
    pass