#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 Artem Yamshanov, me [at] anticode.ninja

BPTC_INTERLEAVING = [x * 181 % 196 for x in range(196)]
CACH_INTERLEAVING = [0, 4, 8, 12, 14, 18, 22, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 15, 16, 17, 19, 20, 21, 23]
CACH_BPTC_INTERLEAVING = [(x * 4 % 68) + (x * 4 // 68) for x in range(68)]
EMB_LC_BPTC_INTERLEAVING = [(x * 8 % 128) + (x * 8 // 128) for x in range(128)]
EMB_RC_BPTC_INTERLEAVING = [x * 17 % 32 for x in range(128)]

def interleave(bits, interleaving):
    t = [x for x in bits]
    for i in range(len(bits)):
        bits[interleaving[i]] = t[i]

def deinterleave(bits, interleaving):
    t = [x for x in bits]
    for i in range(len(bits)):
        bits[i] = t[interleaving[i]]
