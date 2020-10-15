#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    pass

def tamper(payload, **kwargs):
    line = None
    if sys.version_info >= (3, 0, 0):
        line = payload.encode().hex()

    else:
        line = payload.encode("hex")

    groups = [line[i:i+2] for i in range(0, len(line), 2)]
    return "".join(r"\u00" + x for x in groups)
