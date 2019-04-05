from common import *
from interleaving import *
from hamming import *

def parse_bptc_32_11(data, level):
    deinterleave(data, EMB_RC_BPTC_INTERLEAVING)

    if level >= 2:
        print()
        for i in range(2):
            for j in range(16):
                print(data[i * 16 + j], end='')
            print()
        print()

    error_count = 0

    for i in range(1):
        temp = [data[i * 16 + j] for j in range(16)]

        result = hamming(temp, HAMMING_16_11_4_H)
        if result != 'correct':
            print('BPTC R', i, result)
            error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(2):
            result ^= data[i + 16 * j]

        if result != 0:
            print('BPTC C', i, result)
            error_count += 1


    if error_count > 0 or level >= 1:
        print('BPTC ERRORS:', error_count)

    if error_count > 0:
        return None

    result = data[0:12]

    if level >= 1:
        print('DATA', len(result), squash_bits(result))

    if level >= 2:
        print()
        for i in range(1):
            for j in range(12):
                print(result[i * 12 + j], end='')
            print()
        print()

    return result


def parse_bptc_128_72(data, level):
    deinterleave(data, EMB_LC_BPTC_INTERLEAVING)

    if level >= 2:
        print()
        for i in range(8):
            for j in range(16):
                print(data[i * 16 + j], end='')
            print()
        print()

    error_count = 0

    for i in range(4):
        temp = [data[i * 16 + j] for j in range(16)]

        result = hamming(temp, HAMMING_16_11_4_H)
        if result != 'correct':
            print('BPTC R', i, result)
            error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(8):
            result ^= data[i + 16 * j]

        if result != 0:
            print('BPTC C', i, result)
            error_count += 1


    if error_count > 0 or level >= 1:
        print('BPTC ERRORS:', error_count)

    if error_count > 0:
        return None

    result = []
    for i in range(2):
        result.extend(data[i * 16:i * 16 + 11])
    for i in range(2, 7):
        result.extend(data[i * 16:i * 16 + 10])
    for i in range(2, 7):
        result.append(data[i * 16 + 10])

    if level >= 1:
        print('DATA', len(result), squash_bits(result))

    return result

def parse_bptc_68_38(data, level):
    deinterleave(data, CACH_BPTC_INTERLEAVING)

    if level >= 2:
        print()
        for i in range(4):
            for j in range(17):
                print(data[i * 17 + j], end='')
            print()
        print()

    error_count = 0

    for i in range(4):
        temp = [data[i * 17 + j] for j in range(17)]

        result = hamming(temp, HAMMING_17_12_3_H)
        if result != 'correct':
            print('BPTC R', i, result)
            error_count += 1

        for j in range(17):
            data[i * 17 + j] = temp[j]

    for i in range(17):
        result = 0
        for j in range(4):
            result ^= data[i + 17 * j]

        if result != 0:
            print('BPTC C', i, result)
            error_count += 1


    if error_count > 0 or level >= 1:
        print('BPTC ERRORS:', error_count)

    if error_count > 0:
        return None

    result = []
    for i in range(3):
        result.extend(data[i * 17:i * 17 + 12])

    if level >= 1:
        print('DATA', len(result), squash_bits(result))

    if level >= 2:
        print()
        for i in range(3):
            for j in range(12):
                print(result[i * 12 + j], end='')
            print()
        print()

    return result


def parse_bptc_128_72(data, level):
    deinterleave(data, EMB_LC_BPTC_INTERLEAVING)

    if level >= 2:
        print()
        for i in range(8):
            for j in range(16):
                print(data[i * 16 + j], end='')
            print()
        print()

    error_count = 0

    for i in range(4):
        temp = [data[i * 16 + j] for j in range(16)]

        result = hamming(temp, HAMMING_16_11_4_H)
        if result != 'correct':
            print('BPTC R', i, result)
            error_count += 1

        for j in range(16):
            data[i * 16 + j] = temp[j]

    for i in range(16):
        result = 0
        for j in range(8):
            result ^= data[i + 16 * j]

        if result != 0:
            print('BPTC C', i, result)
            error_count += 1


    if error_count > 0 or level >= 1:
        print('BPTC ERRORS:', error_count)

    if error_count > 0:
        return None

    result = []
    for i in range(2):
        result.extend(data[i * 16:i * 16 + 11])
    for i in range(2, 7):
        result.extend(data[i * 16:i * 16 + 10])
    for i in range(2, 7):
        result.append(data[i * 16 + 10])

    if level >= 1:
        print('DATA', len(result), squash_bits(result))

    return result



def parse_bptc_196_96(data, level):
    deinterleave(data, BPTC_INTERLEAVING)

    if level >= 2:
        print()
        for i in range(13):
            for j in range(15):
                print(data[1 + i * 15 + j], end='')
            print()
        print()

    error_count = 0

    for i in range(15):
        temp = [data[1 + i + 15 * j] for j in range(13)]

        result = hamming(temp, HAMMING_13_9_3_H)
        if result != 'correct':
            print('BPTC C', i, result)
            error_count += 1

        for j in range(13):
            data[1 + i + 15 * j] = temp[j]

    for i in range(13):
        temp = [data[1 + i * 15 + j] for j in range(15)]

        result = hamming(temp, HAMMING_15_11_3_H)
        if result != 'correct':
            print('BPTC R', i, result)
            error_count += 1

        for j in range(15):
            data[1 + i * 15 + j] = temp[j]

    if error_count > 0 or level >= 1:
        print('BPTC ERRORS:', error_count)

    if error_count > 0:
        return None

    result = data[4:12]
    for i in range(1,9):
        result.extend(data[i * 15 + 1:i * 15 + 12])

    if level >= 1:
        print('DATA', len(result), squash_bits(result))

    if level >= 2:
        print()
        for i in range(9):
            for j in range(8):
                print(result[1 + i * 8 + j], end='')
            print()
        print()

    return result

