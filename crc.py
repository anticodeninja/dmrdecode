#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 Artem Yamshanov, me [at] anticode.ninja

CRC_8 = (0b111, 8, 0, 0)

def crc(bits, config):
    polynome, polynome_len, initial, inversion = config
    bit_mask = 1 << (polynome_len - 1)
    crc_mask = (1 << polynome_len) - 1

    crc = initial
    for bit in bits:
        op = (crc & bit_mask) ^ (bit * bit_mask)
        crc = (crc << 1) & crc_mask
        if op: crc ^= polynome
    crc = crc ^ inversion

    return [crc >> (polynome_len - i - 1) & 1 for i in range(polynome_len)]
