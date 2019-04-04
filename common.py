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
