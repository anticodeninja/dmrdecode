#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the
# Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright 2019 Artem Yamshanov, me [at] anticode.ninja

import ctypes
import sys
from common import *
from dmr import *

context = DmrContext(0)
input_file = open(sys.argv[1], 'rb')
counter = 1

while True:
    data = input_file.read(36)
    if not data:
        break

    print('=' * 20 + ' {:5} '.format(counter) + '=' * 20)
    context.set_source('file')
    context.parse_cach(get_bits(data[:3]))
    context.parse_burst(get_bits(data[3:]))
    context.out.print()
    counter += 1

