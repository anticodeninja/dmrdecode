from common import *
from interleaving import *
from crc import *
from reedsolomon import *
from hamming import *
from golay import *
from coding import *

IDLE_BLOCK = bits('111111111000001111011111000101110011001000001001010011101101000111100111110011011000101010010001')

SYNC_PATTERNS = {}
SYNC_PATTERNS[bits('0111 0101 0101 1111 1101 0111 1101 1111 0111 0101 1111 0111')] = 'BS SOURCED VOICE'
SYNC_PATTERNS[bits('1101 1111 1111 0101 0111 1101 0111 0101 1101 1111 0101 1101')] = 'BS SOURCED DATA'
SYNC_PATTERNS[bits('0111 1111 0111 1101 0101 1101 1101 0101 0111 1101 1111 1101')] = 'MS SOURCED VOICE'
SYNC_PATTERNS[bits('1101 0101 1101 0111 1111 0111 0111 1111 1101 0111 0101 0111')] = 'MS SOURCED DATA'
SYNC_PATTERNS[bits('0111 0111 1101 0101 0101 1111 0111 1101 1111 1101 0111 0111')] = 'MS SOURCED RC'
SYNC_PATTERNS[bits('0101 1101 0101 0111 0111 1111 0111 0111 0101 0111 1111 1111')] = 'TDMA1 VOICE'
SYNC_PATTERNS[bits('1111 0111 1111 1101 1101 0101 1101 1101 1111 1101 0101 0101')] = 'TDMA1 DATA'
SYNC_PATTERNS[bits('0111 1101 1111 1111 1101 0101 1111 0101 0101 1101 0101 1111')] = 'TDMA2 VOICE'
SYNC_PATTERNS[bits('1101 0111 0101 0101 0111 1111 0101 1111 1111 0111 1111 0101')] = 'TDMA2 DATA'
SYNC_PATTERNS[bits('1101 1101 0111 1111 1111 0101 1101 0111 0101 0111 1101 1101')] = 'RESERVED'

DATA_TYPES = {}
DATA_TYPES[bits('0000')] = ('PI HEADER', None, 0x6969)
DATA_TYPES[bits('0001')] = ('VOICE HEADER', parse_bptc_196_96, 0x969696)
DATA_TYPES[bits('0010')] = ('VOICE TERMINATOR', parse_bptc_196_96, 0x999999)
DATA_TYPES[bits('0011')] = ('CSBK', None, 0xA5A5)
DATA_TYPES[bits('0100')] = ('MBC HEADER', None, 0xAAAA)
DATA_TYPES[bits('0101')] = ('MBC CONTINUATION', None, None)
DATA_TYPES[bits('0110')] = ('DATA HEADER', None, 0xCCCC)
DATA_TYPES[bits('0111')] = ('RATE 1/2 DATA', None, 0x0F0)
DATA_TYPES[bits('1000')] = ('RATE 3/4 DATA', None, 0x1FF)
DATA_TYPES[bits('1001')] = ('IDLE', parse_bptc_196_96, 0x000000)
DATA_TYPES[bits('1010')] = ('RATE 1/1 DATA', None, 0x10F)
DATA_TYPES[bits('1011')] = ('RESERVED', None)
DATA_TYPES[bits('1100')] = ('RESERVED', None)
DATA_TYPES[bits('1101')] = ('RESERVED', None)
DATA_TYPES[bits('1110')] = ('RESERVED', None)
DATA_TYPES[bits('1111')] = ('RESERVED', None)

LCSS = {}
LCSS[bits('00')] = 'SINGLE'
LCSS[bits('01')] = 'FIRST'
LCSS[bits('10')] = 'LAST'
LCSS[bits('11')] = 'CONTINUATION'

FLCOS = {}
DATA_TYPES[bits('111111')] = 'IDLE'

SLCO = {}
SLCO[bits('0000')] = 'IDLE'
SLCO[bits('0001')] = 'ACTIVITY'

SLCA = {}
SLCA[bits('0000')] = 'No activity on BS'
SLCA[bits('0001')] = 'Reserved'
SLCA[bits('0010')] = 'Group CSBK activity on BS'
SLCA[bits('0011')] = 'Individual CSBK activity on BS'
SLCA[bits('0100')] = 'Reserved'
SLCA[bits('0101')] = 'Reserved'
SLCA[bits('0110')] = 'Reserved'
SLCA[bits('0111')] = 'Reserved'
SLCA[bits('1000')] = 'Group voice activity on BS'
SLCA[bits('1001')] = 'Individual voice activity on BS'
SLCA[bits('1010')] = 'Individual data activity on BS'
SLCA[bits('1011')] = 'Group data activity on BS'
SLCA[bits('1100')] = 'Emergency group voice activity on BS'
SLCA[bits('1101')] = 'Emergency individual voice activity on BS'
SLCA[bits('1110')] = 'Reserved'
SLCA[bits('1111')] = 'Reserved'

class DmrContext:

    def __init__(self, level):
        self.stream = None
        self.level = level
        self.caches = {}

    def parse_service(self, service):
        print('SERVICE:', service)
        print('  EMERGENCY:', service[0])
        print('  PRIVACY:', service[1])
        print('  RESERVED:', service[2:4])
        print('  BROADCAST:', service[4])
        print('  OVCM:', service[5])
        print('  PRIORITY:', get_value(service[6:8]))

    def parse_cach_lc(self, cach_lc):
        if self.level >= 1:
            print('CACH LC:', cach_lc)

        cach_lc_data = parse_bptc_68_38(cach_lc, self.level)
        if not cach_lc_data:
            print('CANNOT DECODE CACH LC')
            return

        slco = SLCO[tuple(cach_lc_data[0:4])]
        print('ShortLC Opcode:', slco)
        crc_check = cach_lc_data[28:36] == crc(cach_lc_data[:28], CRC_8)
        if not crc_check or self.level >= 1:
            print('CRC CHECK:', crc_check)

        if slco == 'IDLE':
            print('BITS CHECK:', 'CORRECT' if max(cach_lc_data[4:]) == 0 else 'INCORRECT')
        elif slco == 'ACTIVITY':
            print('SLOT 1', SLCA[tuple(cach_lc_data[4:8])])
            print('SLOT 2', SLCA[tuple(cach_lc_data[8:12])])
            print('SLOT 1 HASH ID', get_value(cach_lc_data[12:20]))
            print('SLOT 2 HASH ID', get_value(cach_lc_data[20:28]))
        else:
            print('UNKNOWN SLCO********************')

    def parse_cach(self, cach):
        if self.level >= 1:
            print('CACH', squash_bits(cach))

        deinterleave(cach, CACH_INTERLEAVING)

        result = hamming(cach[:7], HAMMING_7_4_3_H)
        if result != 'correct' or self.level >= 1:
            print('CACH_HEADER check:', result)

        lcss = LCSS[tuple(cach[2:4])]
        print('ACCESS TYPE:', cach[0])
        print('TDMA CHANNEL:', cach[1])
        print('LCSS:', get_value(cach[2:4]), lcss)

        cach_lc = self.caches.setdefault(self.stream, [])
        if lcss == 'FIRST':
            cach_lc[:] = cach[7:]
        elif lcss == 'CONTINUATION':
            cach_lc.extend(cach[7:])
        elif lcss == 'LAST':
            cach_lc.extend(cach[7:])
            if len(cach_lc) == 68:
                self.parse_cach_lc(cach_lc)
            else:
                print('INCORRECT CACH LC LEN')
        else:
            print('CACH UNKNOWN********************')

    def parse_voice_burst(self, burst):
        pass

    def parse_voice_header(self, info_data):
        flco = get_value(info_data[0:6])
        print('PF (Protect Flag):', info_data[6])
        print('R (Reserved = 0):', info_data[7])
        print('FLCO (Full LC Opcode):', flco, '', end='')

        if flco == 0x00:
            print('Group Voice Channel User LC PDU')
            print('FID (Feature ID):', get_value(info_data[8:16]))
            self.parse_service(info_data[16:24])
            print('Target Id:', get_value(info_data[24:48]))
            print('Source Id:', get_value(info_data[48:72]))
        else:
            print('FLCO UNKNOWN********************')

    def parse_idle(self, info_data):
        print('CORRECT' if tuple(info_data) == IDLE_BLOCK else 'INCORRECT')

        # TODO Add reedsolomon error correction
        # temp = [get_value(info_data[i:i+8]) for i in range(0, 72, 8)]
        # temp2 = mul(temp, SOLOMON_12_9, gf_add, gf_mul)
        # temp3 = [get_value(info_data[i:i+8]) for i in range(0, 96, 8)]
        # temp3[9:12] = [0x96 ^ x for x in temp3[9:12]]
        # print(temp, temp2, temp3, hex(temp2[9] ^ temp3[9]), hex(temp2[10] ^ temp3[10]), hex(temp2[11] ^ temp3[11]))
        # print(rs_calc_syndromes(temp3, 3))

    def parse_data_burst(self, burst):
        info = burst[:98] + burst[166:]
        slot_type = burst[98:108] + burst[156:166]

        if self.level >= 1:
            print('SLOT_TYPE', len(slot_type), squash_bits(slot_type))
            print('INFO', len(info), squash_bits(info))

        result = golay(slot_type, GOLAY_20_8_G)
        if result != 'correct' or self.level >= 1:
            print('SLOT_TYPE check:', result)

        data_type, parser, *args = DATA_TYPES[tuple(slot_type[4:8])]
        print('COLOR CODE:', get_value(slot_type[0:4]))
        print('DATA TYPE:', data_type)

        if parser:
            data = parser(info, self.level, *args)

        if data_type == 'VOICE HEADER':
            self.parse_voice_header(data)
        elif data_type == 'IDLE':
            self.parse_idle(data)
        else:
            print('DATA TYPE UNKNOWN********************')


    def parse_burst(self, burst):
        sync = burst[108:156]

        if self.level >= 1:
            print('SYNC', len(sync), squash_bits(sync))

        sync_pattern = SYNC_PATTERNS.get(tuple(sync), None)
        if sync_pattern:
            print('SYNC PATTERN', sync_pattern)
        else:
            print('UNKNOWN SYNC PATTERN********************')

        if sync_pattern == 'BS SOURCED DATA':
            self.parse_data_burst(burst)
        else:
            print('UNKNOWN********************')

