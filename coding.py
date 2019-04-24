#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 Artem Yamshanov, me [at] anticode.ninja

from common import *
from interleaving import *
from hamming import *

def parse_bptc_32_11(data, out):
    deinterleave(data, EMB_RC_BPTC_INTERLEAVING)

    out(2)
    for i in range(2):
        out(2, ''.join(data[i * 16 + j] for j in range(16)))
    out(2)


    error_count = 0

    for i in range(1):
        temp = [data[i * 16 + j] for j in range(16)]

        with out.context('BPTC R {}'.format(i)) as out:
            if not hamming(temp, HAMMING_16_11_4_H, out):
                error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(2):
            result ^= data[i + 16 * j]

        if result != 0:
            out(0, 'BPTC C {}: crc failed'.format(i))
            error_count += 1

    out(0 if error_count > 0 else 1, 'BPTC ERRORS:', error_count)


    result = data[0:12]

    out(1, 'DATA', len(result), squash_bits(result))
    out(2)
    for i in range(1):
        out(2, squash_bits((result[i * 12 + j] for j in range(12)), False))
    out(2)

    return result


def parse_bptc_128_72(data, level):
    deinterleave(data, EMB_LC_BPTC_INTERLEAVING)

    out(2)
    for i in range(8):
        out(2, ''.join(data[i * 16 + j] for j in range(16)))
    out(2)


    error_count = 0

    for i in range(4):
        temp = [data[i * 16 + j] for j in range(16)]

        with out.context('BPTC R {}'.format(i)) as out:
            if not hamming(temp, HAMMING_16_11_4_H, out):
                error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(8):
            result ^= data[i + 16 * j]

        if result != 0:
            out(0, 'BPTC C {}: crc failed'.format(i))
            error_count += 1

    out(0 if error_count > 0 else 1, 'BPTC ERRORS:', error_count)


    result = []
    for i in range(2):
        result.extend(data[i * 16:i * 16 + 11])
    for i in range(2, 7):
        result.extend(data[i * 16:i * 16 + 10])
    for i in range(2, 7):
        result.append(data[i * 16 + 10])

    out(1, 'DATA', len(result), squash_bits(result))

    return result


def parse_bptc_68_38(data, out):
    deinterleave(data, CACH_BPTC_INTERLEAVING)

    out(2)
    for i in range(4):
        out(2, squash_bits((data[i * 17 + j] for j in range(17)), False))
    out(2)


    error_count = 0

    for i in range(4):
        temp = [data[i * 17 + j] for j in range(17)]

        with out.context('BPTC R {}'.format(i)) as out:
            if not hamming(temp, HAMMING_17_12_3_H, out):
                error_count += 1

        for j in range(17):
            data[i * 17 + j] = temp[j]

    for i in range(17):
        result = 0
        for j in range(4):
            result ^= data[i + 17 * j]

        if result != 0:
            out(0, 'BPTC C {}: crc failed'.format(i))
            error_count += 1

    out(0 if error_count > 0 else 1, 'BPTC ERRORS:', error_count)


    result = []
    for i in range(3):
        result.extend(data[i * 17:i * 17 + 12])

    out(1, 'DATA', len(result), squash_bits(result))
    out(2)
    for i in range(3):
        out(2, squash_bits((result[i * 12 + j] for j in range(12)), False))
    out(2)

    return result


def parse_bptc_128_72(data, level):
    deinterleave(data, EMB_LC_BPTC_INTERLEAVING)

    out(2)
    for i in range(8):
        out(2, ''.join(data[i * 16 + j] for j in range(16)))
    out(2)


    error_count = 0

    for i in range(4):
        temp = [data[i * 16 + j] for j in range(16)]

        with out.context('BPTC R {}'.format(i)) as out:
            if not hamming(temp, HAMMING_16_11_4_H, out):
                error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(8):
            result ^= data[i + 16 * j]

        if result != 0:
            out(0, 'BPTC C {}: crc failed'.format(i))
            error_count += 1

    out(0 if error_count > 0 else 1, 'BPTC ERRORS:', error_count)


    result = []
    for i in range(2):
        result.extend(data[i * 16:i * 16 + 11])
    for i in range(2, 7):
        result.extend(data[i * 16:i * 16 + 10])
    for i in range(2, 7):
        result.append(data[i * 16 + 10])

    out(1, 'DATA', len(result), squash_bits(result))

    return result


def parse_bptc_196_96(data, out):
    deinterleave(data, BPTC_INTERLEAVING)

    out(2)
    for i in range(13):
        out(2, squash_bits((data[1 + i * 15 + j] for j in range(15)), False))
    out(2)


    error_count = 0

    for i in range(15):
        temp = [data[1 + i + 15 * j] for j in range(13)]

        with out.context('BPTC C {}'.format(i)) as out:
            if not hamming(temp, HAMMING_13_9_3_H, out):
                error_count += 1

        for j in range(13):
            data[1 + i + 15 * j] = temp[j]

    for i in range(13):
        temp = [data[1 + i * 15 + j] for j in range(15)]

        with out.context('BPTC R {}'.format(i)) as out:
            if not hamming(temp, HAMMING_15_11_3_H, out):
                error_count += 1

        for j in range(15):
            data[1 + i * 15 + j] = temp[j]

    out(0 if error_count > 0 else 1, 'BPTC ERRORS:', error_count)


    result = data[4:12]
    for i in range(1,9):
        result.extend(data[i * 15 + 1:i * 15 + 12])

    out(1, 'DATA', len(result), squash_bits(result))
    out(2)
    for i in range(9):
        out(2, squash_bits((result[1 + i * 8 + j] for j in range(8)), False))
    out(2)

    return result

