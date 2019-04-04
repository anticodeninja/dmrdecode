BPTC_INTERLEAVING = [x * 181 % 196 for x in range(196)]
CACH_INTERLEAVING = [0, 4, 8, 12, 14, 18, 22, 1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 15, 16, 17, 19, 20, 21, 23]
CACH_BPTC_INTERLEAVING = [(x * 4 % 68) + (x * 4 // 68) for x in range(68)]

def interleave(bits, interleaving):
    t = [x for x in bits]
    for i in range(len(bits)):
        bits[interleaving[i]] = t[i]

def deinterleave(bits, interleaving):
    t = [x for x in bits]
    for i in range(len(bits)):
        bits[i] = t[interleaving[i]]
