#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 Artem Yamshanov, me [at] anticode.ninja


class OutputContext:

    def __init__(self, parent, prefix):
        self.parent = parent
        self.prefix = prefix

    def __call__(self, level, *args):
        self.parent(level, self.prefix, *args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def context(self, prefix):
        return OutputContext(self, prefix)


class Output:

    def __init__(self, level):
        self.level = level
        self.output = []
        self.chunk = None
        self.pins = []

    def __call__(self, level, *args):
        if self.level >= level:
            self.output.append(' '.join(str(x) for x in args))

    def clear(self):
        self.output.clear()
        self.pins.clear()

    def print(self):
        for line in self.output:
            print(line)

    def context(self, prefix):
        return OutputContext(self, prefix)

    def pin(self):
        self.pins.append(len(self.output))

    def droppin(self):
        if len(self.pins) > 1:
            del self.output[self.pins[-2]:self.pins[-1]]
            self.pins.pop()
        else:
            del self.output[:self.pins.pop()]


def xor_add(a, b):
    return a ^ b


def xor_mul(a, b):
    return a & b


def bits(string):
    return tuple(int(x) for x in string if x >= '0' and x <= '1')


def get_bits(data):
    temp = []

    for byte in data:
        for j in range(8):
            temp.append((byte >> j) & 1)

    return temp


def get_value(bits):
    power = len(bits) - 1
    return sum((1 << (power - i)) * b for i, b in enumerate(bits))


def squash_bits(bits, reverted=True):
    if reverted:
        bits = reversed(bits)
    return ''.join(str(x) for x in bits)


def mul(v, m, add=xor_add, mul=xor_mul):
    h, w = len(m), len(m[0])
    r = [0] * w
    for i in range(w):
        for j in range(h):
            r[i] = add(r[i], mul(v[j], m[j][i]))
    return r
